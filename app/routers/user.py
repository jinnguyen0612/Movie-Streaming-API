"""
Router User
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas,models,utils,oauth2

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    check_user = db.query(models.User).filter(models.User.email == user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/',response_model=List[schemas.UserOut])
async def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{id}',response_model=schemas.UserOut)
async def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return user
