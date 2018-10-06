import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
	password_hash = Column(String(64))
	
	def hash_password(self,password):
		self.password_hash = pwd_context.encrypt(password)
		
	def verify_password(self,password):
		return pwd_context.verify(password, self.password_hash)

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    #parent = Column(Integer, nullable=True)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
            #,
            #'parent': self.parent
        }

        

class Items(Base):
    __tablename__ = 'items'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'categories_id':categories.id
        }

class Lineage(Base):
    __tablename__ = 'lineage'

    
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    child_id = Column(Integer, ForeignKey('categories.id'))

    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'parentid': self.parent_id,
            'childid': self.child_id
        }


engine = create_engine('sqlite:///itemCatalog.db')


Base.metadata.create_all(engine)
