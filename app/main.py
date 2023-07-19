"""
Main
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, auth
from . config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)


@app.get('/')
def root():
    return {"message": "Welcome to my API server"}


