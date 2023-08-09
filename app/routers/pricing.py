"""
Router pricing
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from fastapi import UploadFile,File,APIRouter,Depends,status,HTTPException,Response,Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional, Text,List

from ..database import get_db
from .. import database,schemas,models,utils,oauth2

router = APIRouter(
    prefix="/pricing",
    tags=['Pricing']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_pricing(pricing:schemas.Pricing,db: Session = Depends(get_db)):
    new_pricing = models.Pricing(**pricing)
    db.add(new_pricing)
    db.commit()
    db.refresh(new_pricing)

    return {"msg":"Create Success"}

@router.get('/getAll',response_model=List[schemas.PricingOut])
async def get_all_Pricing(db:Session = Depends(get_db)):
    pricing = db.query(models.Pricing).all()
    return pricing

@router.get('/get/{id}', response_model=schemas.PricingOut)
async def get_pricing(id: int, db:Session=Depends(get_db)):
    pricing = db.query(models.Pricing).filter(models.Pricing.id==id).first()
    if not pricing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pricing does not exist")
    return pricing
