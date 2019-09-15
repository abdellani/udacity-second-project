from flask import Flask, request, render_template, redirect, g, flash, url_for
# forms
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect
# databases
from database import Base, Categorie, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Env variable
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///database.sqlite", connect_args={'check_same_thread': False})
        self.Session = sessionmaker(self.engine)
        self.session = self.Session()

    def add_categorie(self, name, description=""):
        self.session.add(Categorie(name, description=description))
        self.session.commit()

    def update_categorie(self, id, name, description):
        categorie = self.get_categorie(id)
        categorie.name = name
        categorie.description = description
        self.session.add(categorie)
        self.session.commit()

    def get_categories(self):
        return self.session.query(Categorie).all()

    def get_categorie(self, id=0):
        return self.session.query(Categorie).get(id)

    def delete_categorie(self, id):
        self.session.delete(self.get_categorie(id))
        self.session.commit()

    def add_item(self, cat_id, name, description):
        self.session.add(Item(cat_id, name, description))
        self.session.commit()

    def update_item(self, id, name, description):
        item = self.get_item(id)
        item.name = name
        item.description = description
        self.session.add(item)
        self.session.commit()

    def get_item(self, id):
        return self.session.query(Item).get(id)

    def delete_item(self, id):
        self.session.delete(self.get_item(id))
        self.session.commit()

    def add_user(self,name,email,password_hash):
        self.session.add(User(name,email,password_hash))
        self.session.commit()


class Form(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])

    def __init__(self):
        super(Form, self).__init__(csrf_enabled=True)


class RegistrationForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    email = EmailField('Email address:', validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    password_confirmation = PasswordField(
        "Password confirmation:", validators=[DataRequired()])

    def __init__(self):
        super(RegistrationForm, self).__init__(csrf_enabled=True)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)
db = Database()


@app.before_request
def load_categories():
    if request.method == 'GET':
        g.categories = db.get_categories()


"""
Resource : Categories
"""
@app.route('/')
@app.route('/categories', methods=["GET"])
def categoriesIndex():
    return render_template("categories/index.html", title="Index")


@app.route('/categories/new', methods=["GET"])
def categoriesNew():
    form = Form()
    return render_template("categories/new.html", title="Add new category", form=form)


@app.route('/categories/<int:id>/edit', methods=["GET"])
def categoriesEdit(id):
    form = Form()
    categorie = db.get_categorie(id)
    form.name.data = categorie.name
    form.description.data = categorie.description
    return render_template("categories/edit.html", form=form, categorie=categorie)


@app.route('/categories', methods=["POST"])
def categoriesCreate():
    form = Form()
    if form.validate_on_submit():
        db.add_categorie(form.name.data, form.description.data)
        flash(u'The new catergorie has been added successfully', "success")
    else:
        flash(u'Failed to add new categorie', "danger")
    return redirect(url_for("categoriesIndex"))


@app.route('/categories/<int:id>/edit', methods=["POST"])
def categoriesUpdate(id):
    form = Form()
    if form.validate_on_submit():
        db.update_categorie(id, form.name.data, form.description.data)
        flash(u'The catergorie has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("categoriesIndex"))


@app.route('/categories/<int:id>/delete', methods=["POST"])
def categoriesDestroy(id):
    db.delete_categorie(id)
    flash(u'The catergorie was deleted successfully', "success")
    return redirect(url_for("categoriesIndex"))


"""
Resource: Items
"""
@app.route('/categories/<int:cat_id>/items', methods=["GET"])
def itemsIndex(cat_id):
    categorie = db.get_categorie(cat_id)
    return render_template("items/index.html", categorie=categorie)


@app.route('/categories/<int:cat_id>/items/new', methods=["GET"])
def itemsNew(cat_id):
    form = Form()
    categorie = db.get_categorie(cat_id)
    return render_template("items/new.html", title="Add new item", categorie=categorie, form=form)


@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=["GET"])
def itemsShow(cat_id, item_id):
    categorie = db.get_categorie(cat_id)
    item = db.get_item(item_id)
    return render_template("items/show.html", title="item details", categorie=categorie, item=item)


@app.route('/categories/<int:cat_id>/items/<int:item_id>/edit', methods=["GET"])
def itemsEdit(cat_id, item_id):
    categorie = db.get_categorie(cat_id)
    item = db.get_item(item_id)
    form = Form()
    form.name.data = item.name
    form.description.data = item.description
    return render_template("items/edit.html", title="Edit item", categorie=categorie, item=item, form=form)


@app.route('/categories/<int:cat_id>/items', methods=["POST"])
def itemsCreate(cat_id):
    form = Form()
    if form.validate_on_submit():
        db.add_item(cat_id, form.name.data, form.description.data)
        flash(u'The new item has been added successfully', "success")
    else:
        flash(u'Failed to add item', "danger")
    return redirect(url_for("itemsIndex", cat_id=cat_id))


@app.route('/categories/<int:cat_id>/items/<int:item_id>/edit', methods=["POST"])
def itemsUpdate(cat_id, item_id):
    form = Form()
    if form.validate_on_submit():
        db.update_item(item_id, form.name.data, form.description.data)
        flash(u'The catergorie has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("itemsIndex", cat_id=cat_id))


@app.route('/categories/<int:cat_id>/items/<int:item_id>/delete', methods=["POST"])
def itemsDestroy(cat_id, item_id):
    db.delete_item(item_id)
    flash(u'The item has been deleted successfully', "success")
    return redirect(url_for("itemsIndex", cat_id=cat_id))


"""
Resource: User
"""
@app.route('/signup', methods=["GET"])
def registrationNew():
    form = RegistrationForm()
    return render_template('registrations/new.html', title="New registration", form=form)


@app.route('/signup', methods=["POST"])
def registrationCreate():
    form = RegistrationForm()
    if form.validate_on_submit() and form.password.data == form.password_confirmation.data  :
        db.add_user(form.name.data,form.email.data,form.password.data)
        flash(u'The new user has been added successfully', "success")
        return redirect(url_for("categoriesIndex"))
    else:
        flash(u'Failed to add new user', "danger")
        return redirect(url_for("registrationCreate"))

"""
Resource :sessions
"""
@app.route('/login',methods=["GET"])
def sessionNew():
    return

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
