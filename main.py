import os
import random
from flask import Flask, request, render_template, redirect, g, flash, url_for, session,jsonify
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
# forms
from flask_wtf.csrf import CSRFProtect
# from forms import Form, RegistrationForm, LoginForm
# databases
from database import Base, Categorie, Item, User
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from dbm import db
# Login
from flask_github import GitHub
# Env variable
from dotenv import load_dotenv
from loginmanager import login_manager
from categories import categories_pages
from items import items_pages

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')

login_manager.init_app(app)
csrf = CSRFProtect(app)
github = GitHub(app)


@app.before_request
def load_categories():
    if request.method == 'GET':
        g.categories = db.get_categories()



app.register_blueprint(categories_pages)
app.register_blueprint(items_pages)

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
        return redirect(url_for("categories.index"))
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
        return redirect(url_for("categories.index"))
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
    return redirect(url_for("categories.index"))


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
