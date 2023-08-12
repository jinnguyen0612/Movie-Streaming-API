"""
Router films
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from fastapi import UploadFile,File,APIRouter,Depends,status,HTTPException,Response,Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, Text,List
from sqlalchemy.sql import text
from sqlalchemy import func


from ..database import get_db
from .. import database,schemas,models,utils,oauth2

router = APIRouter(
    prefix="/films",
    tags=['Films']
)

#POST
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_film(film:schemas.FilmBase,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    film_check = db.query(models.Film).filter(models.Film.title == film.title)
    if film_check!= None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Film title conflict")
    new_film = models.Film(**film.dict())
    db.add(new_film)
    db.commit()
    db.refresh(new_film)
    return {"msg":"Create success"}

@router.post("/addActors/{film_id}",status_code=status.HTTP_201_CREATED)
def add_actors_to_film(film_id: int, actor_ids: List[int], db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    film = db.query(models.Film).get(film_id)
    
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    
    for actor_id in actor_ids:
        actor = db.query(models.Actor).get(actor_id)
        if not actor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Actor with id {actor_id} not found")
        
        film_actor = models.Film_Actor(film_id=film_id, actor_id=actor_id)
        db.add(film_actor)
    
    db.commit()
    db.refresh(film)
    
    return {"msg":"Add actors to film success"}

@router.post("/addFavoriteFilm/{film_id}", status_code=status.HTTP_201_CREATED)
def add_favorite_film(film_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    film = db.query(models.Film).get(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

    favorite_film = models.Favorite_Film(user_id=current_user.id, film_id=film_id)
    db.add(favorite_film)
    db.commit()

    return {"msg": "Film added to favorites"}

@router.post("/addVote/{film_id}", status_code=status.HTTP_201_CREATED)
def vote_film(film_id: int, vote: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    film = db.query(models.Film).get(film_id)
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

    # Assuming vote should be between 1 and 5
    if vote < 1 or vote > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote value")

    film_vote = models.Rating_Film(user_id=current_user.id, film_id=film_id, rate=vote)
    db.add(film_vote)
    db.commit()

    return {"msg": "Film voted successfully"}
#END POST

#GET
@router.get('/getAll',response_model=List[schemas.FilmDetailOut])
async def get_all_films(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    films = db.query(models.Film).all()
    film_details = []
    for film in films:
        film_detail = schemas.FilmDetailOut(
            **film.__dict__,
            genre=schemas.GenreOut(**film.genre.__dict__)  # Chắc chắn cung cấp giá trị cho trường genre
        )
        film_details.append(film_detail)
    return film_details

@router.get('/getActive',response_model=List[schemas.FilmDetailOut])
async def get_active_films(db:Session = Depends(get_db)):
    films = db.query(models.Film).filter(models.Film.status==True).all()
    return films

@router.get('/get/{film_id}', response_model=schemas.FilmDetailOut)
async def get_film(film_id: int, db:Session=Depends(get_db)):
    film = db.query(models.Film).filter(models.Film.id==film_id).first()
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Film does not exist")
    return film

@router.get("/topFavoriteFilms", response_model=List[schemas.FilmDetailOut])
def get_top_favorite_films(db: Session = Depends(get_db)):
    subquery = db.query(
        models.Favorite_Film.film_id,
        func.count(models.Favorite_Film.film_id).label("count")
    ).group_by(models.Favorite_Film.film_id).order_by(text("count DESC")).limit(8).subquery()

    top_favorite_films = db.query(models.Film).join(subquery, models.Film.id == subquery.c.film_id).all()

    return top_favorite_films

from sqlalchemy import desc

@router.get("/topRatedFilms", response_model=list[dict])
async def get_top_rated_films(db: Session = Depends(get_db)):
    top_rated_films = db.query(
        models.Film,
        func.avg(models.Rating_Film.rate).label("avg_rating"),
        func.count(models.Rating_Film.film_id).label("vote_count")
    ) \
        .join(models.Rating_Film, models.Film.id == models.Rating_Film.film_id) \
        .group_by(models.Film.id) \
        .order_by(
            desc("avg_rating"),
            desc("vote_count")
        ) \
        .limit(8) \
        .all()

    film_list_with_avg_rating = []
    for film, avg_rating, vote_count in top_rated_films:
        genre_name = film.genre.name if film.genre else None
        film_data = {
            "id": film.id,
            "title": film.title,
            "length": film.length,
            "poster": film.poster,
            "production_year": film.production_year,
            "path": film.path,
            "description": film.description,
            "price": film.price,
            "genre": {"name": genre_name, "id": film.genre_id},
            "status": film.status,
            "add_at": film.add_at,
            "avg_rating": avg_rating,
            "vote_count": vote_count
        }
        film_list_with_avg_rating.append(film_data)

    return film_list_with_avg_rating




@router.get("/averageRating/{film_id}")
def get_average_rating(film_id: int, db: Session = Depends(get_db)):
    avg_rating = db.query(func.avg(models.Rating_Film.rate).label("avg_rating")).filter(models.Rating_Film.film_id == film_id).scalar()
    
    if avg_rating is None:
        avg_rating = 0.0
    
    return {"film_id": film_id, "average_rating": avg_rating}

@router.get("/getFavoriteFilms", response_model=List[schemas.FilmDetailOut])
def get_favorite_films(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    favorite_films = db.query(models.Film).join(
        models.Favorite_Film,
        models.Film.id == models.Favorite_Film.film_id
    ).filter(models.Favorite_Film.user_id == current_user.id).all()

    if not favorite_films:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no favorite films"
        )
    return favorite_films

#END GET

#PUT
@router.put('/edit/{film_id}')
async def update_film(film_id:int, edit_film: schemas.FilmBase,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    try:
        film_check = db.query(models.Film).filter(models.Film.title == edit_film.title).first()
        if film_check != None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Film title conflict")
        film_query = db.query(models.Film).filter(models.Film.id == film_id)
        film = film_query.first()
        
        if film == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Film does not exist")
        
        film_query.update(edit_film.dict(), synchronize_session=False) # type: ignore
        db.commit()
        return {"msg":"Edit film success"}
    except Exception as e:
        error_detail = str(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_detail)
    
@router.put('/edit/status/{film_id}')
async def update_film_status(film_id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    film_query = db.query(models.Film).filter(models.Film.id == film_id)
    film = film_query.first()
    
    if film is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Film does not exist")
    
    new_status = not film.status
    edit_film = {"status": new_status}
    
    film_query.update(edit_film, synchronize_session=False)
    db.commit()
    return {"msg": "Change film status success"}

#END PUT
        
        

