import os
import random
from flask import Flask, request, render_template, redirect, \
    g, flash, url_for, session, jsonify
from flask_login import LoginManager, login_user, logout_user, \
    login_required, current_user
# forms
from flask_wtf.csrf import CSRFProtect
from forms import Form, RegistrationForm, LoginForm
# databases
from database import Base, Categorie, Item, User
from dbm import db
# Login
from flask_github import GitHub
# Env variable
from dotenv import load_dotenv
from loginmanager import login_manager
from categories import categories_pages
from items import items_pages
from registrations import registrations_pages
from sessions import sessions_pages

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['GITHUB_CLIENT_ID'] = os.getenv('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.getenv('GITHUB_CLIENT_SECRET')

login_manager.init_app(app)
csrf = CSRFProtect(app)
github = GitHub(app)

app.register_blueprint(categories_pages)
app.register_blueprint(items_pages)
app.register_blueprint(registrations_pages)
app.register_blueprint(sessions_pages)


@app.before_request
def load_categories():
    if request.method == 'GET':
        g.categories = db.get_categories()


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def errorhandler(e):
    flash(u'Ops, some wrong happened during your last request !', "danger")
    return redirect("/")


@app.route('/login/github')
def loginGithub():
    return github.authorize(scope="user")


@app.route("/github-callback")
@github.authorized_handler
def authorized(oauth_token):
    if oauth_token is None:
        flash(u'Login failed', "danger")
        return redirect(url_for("sessions.create"))
    g.github_access_token = oauth_token
    github_user = github.get('/user')
    user = db.get_user_by_login(github_user['login'])
    if user is None:
        random_password = ''.join(random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
            for i in range(48))
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


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
