from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_login import UserMixin

Base = declarative_base()


class Categorie(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    items = relationship("Item")

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'items': [
                {
                    "name": item.name,
                    "description": item.description,
                }
                for item in self.items]
        }


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    categorie_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, user_id, cat_id, name, description):
        self.user_id = user_id
        self.categorie_id = cat_id
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash


if __name__ == '__main__':
    engine = create_engine("sqlite:///database.sqlite")
    Base.metadata.create_all(engine)
