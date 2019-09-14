from flask import Flask,request,render_template, redirect,g,flash
#forms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
#databases
from database import Base,Categorie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Env variable
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
  def __init__(self):
    self.engine = create_engine("sqlite:///database.sqlite")
    self.Session = sessionmaker(self.engine)
    self.session= self.Session()
  def add_categorie (self,name,description=""):    
    self.session.add(Categorie(name,description=description))
    self.session.commit()
  def get_categories(self):
    return self.session.query(Categorie).all()

class CategoriesForm(FlaskForm):
  name=StringField("Name",validators=[DataRequired()])
  description=StringField("Description")
  def __init__(self):
    super(CategoriesForm,self).__init__(csrf_enabled=True)

app = Flask(__name__)
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
db=Database()

@app.before_request
def load_categories():
  g.categories=db.get_categories()

"""
Resource : Categories
"""
@app.route('/')
@app.route('/categories',methods=["GET"])
def categoriesIndex():
  return render_template("categories/index.html",title="Index")

@app.route('/categories/<int:id>',methods=["GET"])
def categoriesShow():
  return render_template("categories/show.html")

@app.route('/categories/new',methods=["GET"])
def categoriesNew():
  form=CategoriesForm()
  return render_template("categories/new.html",form=form)

@app.route('/categories/<int:id>/edit',methods=["GET"])
def categoriesEdit():
  return render_template("categories/edit.html")

@app.route('/categories',methods=["POST"])
def categoriesCreate():
  form=CategoriesForm()
  if form.validate_on_submit(): 
    db.add_categorie(form.name.data,form.description.data)
    flash(u'The new catergorie has been added successfully',"success")
    return redirect("/")
  else:
    flash(u'Failed to add new categorie',"danger")
    return redirect("/")

@app.route('/categories/<int:id>/edit',methods=["POST"])
def categoriesUpdate():
  return 

@app.route('/categories/<int:id>/delete',methods=["POST"])
def categoriesDestroy():
  return 

"""
Resource: Items
"""
@app.route('/categories/<int:id>/items',methods=["GET"])
def itemsIndex():
  return render_template("items/index.html")
@app.route('/categories/<int:id>/items/new',methods=["GET"])
def itemsNew():
  return render_template("items/new.html",title="Add new item")
@app.route('/categories/<int:id>/items/<int:item_id>',methods=["GET"])
def itemsShow():
  return render_template("items/show.html")
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["GET"])
def itemsEdit():
  return render_template("items/edit.html")

@app.route('/categories/<int:id>/items',methods=["POST"])
def itemsCreate():
  return
@app.route('/categories/<int:id>/items/<int:item_id>/edit',methods=["POST"])
def itemsUpdate():
  return
@app.route('/categories/<int:id>/items/<int:item_id>/delete',methods=["POST"])
def itemsDestroy():
  return 

if __name__=="__main__":
  app.run(host="localhost",port=8000,debug= True)
