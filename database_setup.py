import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'creation_date': self.creation_date
        }

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    description = Column(String(250))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'creation_date': self.creation_date,
            'description': self.description
        }

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
