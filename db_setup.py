import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


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

        
class Lineage(Base):
    __tablename__ = 'lineage'

    
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('categories.id'))
    child_id = Column(Integer, ForeignKey('items.id'))
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'parentid': self.parent_id,
            'childid': self.child_id
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
            'catid':categories.id
        }


engine = create_engine('sqlite:///itemCatalog.db')


Base.metadata.create_all(engine)
