import os
import random
from flask import Flask, request, render_template, redirect, g, flash, url_for, session,jsonify
# forms
from flask_wtf.csrf import CSRFProtect
from forms import Form, RegistrationForm, LoginForm
# databases
from database import Base, Categorie, Item, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Login
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_github import GitHub
# Env variable
from dotenv import load_dotenv

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

    def add_item(self, user_id,cat_id, name, description):
        self.session.add(Item(user_id,cat_id, name, description))
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

    def add_user(self, name, email, password_hash):
        self.session.add(User(name, email, password_hash))
        self.session.commit()

    def check_credentials(self, email, password_hash):
        return self.session.query(User).filter(
            User.email == email
        ).filter(
            User.password_hash == password_hash
        ).first()

    def get_user(self, user_id):
        return self.session.query(User).get(user_id)

    def get_user_by_login(self, user_login):
        return self.session.query(User).filter(User.name == user_login).first()


db = Database()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

login_manager = LoginManager()

login_manager.init_app(app)
csrf = CSRFProtect(app)

app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')
github = GitHub(app)

"""
LoginManager
"""
@login_manager.user_loader
def user_loader(user_id):
    return db.get_user(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    flash(u'You must login first !', "danger")
    return redirect(url_for("sessionsCreate"))


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

@app.route('/categories/json', methods=["GET"])
def categoriesIndexJson():
    return jsonify([ categorie.serialize for categorie in g.categories])

@app.route('/categories/new', methods=["GET"])
@login_required
def categoriesNew():
    if current_user.id!=1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categoriesIndex"))
    form = Form()
    return render_template("categories/new.html", title="Add new category", form=form)


@app.route('/categories/<int:id>/edit', methods=["GET"])
@login_required
def categoriesEdit(id):
    if current_user.id!=1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categoriesIndex"))
    form = Form()
    categorie = db.get_categorie(id)
    form.name.data = categorie.name
    form.description.data = categorie.description
    return render_template("categories/edit.html", form=form, categorie=categorie)


@app.route('/categories', methods=["POST"])
@login_required
def categoriesCreate():
    if current_user.id!=1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categoriesIndex"))
    form = Form()
    if form.validate_on_submit():
        db.add_categorie(form.name.data, form.description.data)
        flash(u'The new catergorie has been added successfully', "success")
    else:
        flash(u'Failed to add new categorie', "danger")
    return redirect(url_for("categoriesIndex"))


@app.route('/categories/<int:id>/edit', methods=["POST"])
@login_required
def categoriesUpdate(id):
    if current_user.id!=1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categoriesIndex"))
    form = Form()
    if form.validate_on_submit():
        db.update_categorie(id, form.name.data, form.description.data)
        flash(u'The catergorie has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("categoriesIndex"))


@app.route('/categories/<int:id>/delete', methods=["POST"])
@login_required
def categoriesDestroy(id):
    if current_user.id!=1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categoriesIndex"))
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
@login_required
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
@login_required
def itemsEdit(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id!=item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("itemsIndex",cat_id=cat_id))
    categorie = db.get_categorie(cat_id)
    form = Form()
    form.name.data = item.name
    form.description.data = item.description
    return render_template("items/edit.html", title="Edit item", categorie=categorie, item=item, form=form)


@app.route('/categories/<int:cat_id>/items', methods=["POST"])
@login_required
def itemsCreate(cat_id):
    form = Form()
    if form.validate_on_submit():
        db.add_item(current_user.id,cat_id, form.name.data, form.description.data)
        flash(u'The new item has been added successfully', "success")
    else:
        flash(u'Failed to add item', "danger")
    return redirect(url_for("itemsIndex", cat_id=cat_id))


@app.route('/categories/<int:cat_id>/items/<int:item_id>/edit', methods=["POST"])
@login_required
def itemsUpdate(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id!=item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("itemsIndex",cat_id=cat_id))
    form = Form()
    if form.validate_on_submit():
        db.update_item(item_id, form.name.data, form.description.data)
        flash(u'The item has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("itemsIndex", cat_id=cat_id))


@app.route('/categories/<int:cat_id>/items/<int:item_id>/delete', methods=["POST"])
@login_required
def itemsDestroy(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id!=item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("itemsIndex",cat_id=cat_id))

    db.delete_item(item_id)
    flash(u'The item has been deleted successfully', "success")
    return redirect(url_for("itemsIndex", cat_id=cat_id))

"""
Resource: User
"""
@app.route('/signup', methods=["GET"])
def registrationsNew():
    form = RegistrationForm()
    return render_template('registrations/new.html', title="New registration", form=form)


@app.route('/signup', methods=["POST"])
def registrationsCreate():
    form = RegistrationForm()
    if form.validate_on_submit() and form.password.data == form.password_confirmation.data:
        db.add_user(form.name.data, form.email.data, form.password.data)
        flash(u'The new user has been added successfully', "success")
        return redirect(url_for("categoriesIndex"))
    else:
        flash(u'Failed to add new user', "danger")
        return redirect(url_for("registrationsCreate"))


"""
Resource :sessions
"""
@app.route('/login', methods=["GET"])
def sessionsNew():
    form = LoginForm()
    return render_template('sessions/new.html', title="Login", form=form)


@app.route('/login', methods=["POST"])
def sessionsCreate():
    form = LoginForm()
    res = db.check_credentials(form.email.data, form.password.data)
    if res is not None:
        login_user(res)
        flash(u'Welcome', "success")
        return redirect(url_for("categoriesIndex"))
    else:
        flash(u'User or password are wrong !', "danger")
        return redirect(url_for("sessionsCreate"))


@app.route('/login/github')
def loginGithub():
    return github.authorize(scope="user")


@app.route("/github-callback")
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        flash(u'Login failed', "danger")
        return redirect(url_for("sessionsCreate"))
    g.github_access_token = oauth_token
    github_user = github.get('/user')
    user = db.get_user_by_login(github_user['login'])
    if user is None:
        random_password = ''.join(random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(48))
        db.add_user(github_user['login'],
                    github_user['email'], random_password)
        user = db.get_user_by_login(github_user['login'])

    login_user(user)
    flash(u'Welcome', "success")
    return redirect(url_for("categoriesIndex"))


@github.access_token_getter
def token_getter():
    if g.github_access_token is not None:
        return g.github_access_token


@app.route('/logout', methods=["POST"])
def sessionsDestroy():
    logout_user()
    return redirect(url_for('sessionsNew'))


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
