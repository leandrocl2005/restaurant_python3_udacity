import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from config import DATABASE_URL
 
Base = declarative_base()
 
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
 
class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(5500))
    price = Column(String(8))
    course = Column(String(5500))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    #We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):
        return {
                'name': self.name,
                'description': self.description,
                'id': self.id,
                'price': self.price,
                'course': self.course,
               }

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)