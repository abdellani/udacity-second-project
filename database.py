from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,String,Integer,ForeignKey

Base = declarative_base()

class Categorie(Base):
  __tablename__= 'categories'
  id = Column(Integer, primary_key=True)
  name=Column(String)
  description= Column(String)
  def __init__ (self,name,description=""):
    self.name=name
    self.description=description

if __name__ == '__main__':
  engine = create_engine("sqlite:///database.sqlite")
  Base.metadata.create_all(engine)
  