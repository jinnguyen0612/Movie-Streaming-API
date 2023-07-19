"""
Create table PostgreSQL
Author: jinnguyen0612
Email: hoangha0612.work@gmail.com
"""

from sqlalchemy import Column, Integer, String, Boolean,ForeignKey,Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable= False)
    name = Column(String, nullable=False)
    role = Column(Integer, nullable=False,server_default='0')
    status = Column(Integer, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Film(Base):
    __tablename__ = "films"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    length = Column(Integer, nullable= False) #minute
    poster = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_vip = Column(Boolean, nullable=False,server_default='False')
    status = Column(Integer, nullable=False, server_default='0')
    add_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Serie(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable= False)
    poster = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    is_vip = Column(Boolean, nullable=False,server_default='False')
    status = Column(Integer, nullable=False, server_default='0')
    add_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# Episode of serie
class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True, nullable=False)
    serie_id = Column(Integer,ForeignKey("series.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable= False)
    path = Column(String, nullable=False)
    status = Column(Integer, nullable=False, server_default='0')
    add_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

#
class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)
    photo = Column(String, nullable=False)
    
class Pricing(Base):
    __tablename__ = "pricing"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable= False)
    price = Column(Numeric, nullable= False)
    days = Column(Numeric, nullable= False)
    
# Payment of a user
class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pricing_id = Column(Integer,ForeignKey("pricing.id", ondelete="CASCADE"), nullable=False)
    film_id = Column(Integer,ForeignKey("films.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)

# Table rating film/serie
class Rating_Film(Base):
    __tablename__ = "rating_film"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    film_id = Column(Integer,ForeignKey("films.id", ondelete="CASCADE"),primary_key=True)
    rate = Column(Numeric, nullable= False)    

class Rateing_Serie(Base):
    __tablename__ = "rating_serie"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    serie_id = Column(Integer,ForeignKey("series.id", ondelete="CASCADE"),primary_key=True)
    rate = Column(Numeric, nullable= False)

#Table time stamping
class Stamping_Film(Base):
    __tablename__ = "stamping_film"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    film_id = Column(Integer,ForeignKey("films.id", ondelete="CASCADE"),primary_key=True)
    time_stamping = Column(Numeric, nullable= False) 

class Stamping_Episode(Base):
    __tablename__ = "stamping_episode"
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    serie_id = Column(Integer,ForeignKey("series.id", ondelete="CASCADE"),primary_key=True)
    time_stamping = Column(Numeric, nullable= False) 
    
# Table genre of film/serie
class Film_Genre(Base):
    __tablename__ = "film_genre"
    genre_id = Column(Integer,ForeignKey("genres.id", ondelete="CASCADE"),primary_key=True)
    film_id = Column(Integer,ForeignKey("films.id", ondelete="CASCADE"),primary_key=True)

class Serie_Genre(Base):
    __tablename__ = "serie_genre"
    genre_id = Column(Integer,ForeignKey("genres.id", ondelete="CASCADE"),primary_key=True)
    serie_id = Column(Integer,ForeignKey("series.id", ondelete="CASCADE"),primary_key=True)

#Table actor in film/serie    
class Film_Actor(Base):
    __tablename__ = "film_actor"
    actor_id = Column(Integer,ForeignKey("actors.id", ondelete="CASCADE"),primary_key=True)
    film_id = Column(Integer,ForeignKey("films.id", ondelete="CASCADE"),primary_key=True)

class Serie_Genre(Base):
    __tablename__ = "serie_actor"
    actor_id = Column(Integer,ForeignKey("actors.id", ondelete="CASCADE"),primary_key=True)
    serie_id = Column(Integer,ForeignKey("series.id", ondelete="CASCADE"),primary_key=True)
    

 
    