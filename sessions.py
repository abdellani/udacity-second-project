from flask_login import LoginManager, login_user, logout_user,\
    login_required, current_user
from flask import Blueprint, Flask, request, render_template,\
    redirect, g, flash, url_for, session, jsonify
from forms import Form
from dbm import db
from forms import Form, RegistrationForm, LoginForm

sessions_pages = Blueprint('sessions',
                           __name__,
                           template_folder='templates')


@sessions_pages.route('/login', methods=["GET"])
def new():
    form = LoginForm()
    return render_template('sessions/new.html', title="Login", form=form)


@sessions_pages.route('/login', methods=["POST"])
def create():
    form = LoginForm()
    res = db.check_credentials(form.email.data, form.password.data)
    if res is not None:
        login_user(res)
        flash(u'Welcome', "success")
        return redirect(url_for("categories.index"))
    else:
        flash(u'User or password are wrong !', "danger")
        return redirect(url_for("sessions.create"))


@sessions_pages.route('/logout', methods=["POST"])
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))
