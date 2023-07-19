"""
Router films
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from fastapi import UploadFile,File,APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db

from .. import database,schemas,models,utils,oauth2

router = APIRouter(
    prefix="/films",
    tags=['Films']
)