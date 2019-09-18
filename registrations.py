from forms import  RegistrationForm
from dbm import db
from flask import Flask,Blueprint, request, render_template, redirect, g, flash, url_for, session,jsonify

registrations_pages = Blueprint('registrations',
                        __name__,
                        template_folder='templates')

@registrations_pages.route('/signup', methods=["GET"])
def new():
    form = RegistrationForm()
    return render_template('registrations/new.html', title="New registration", form=form)

@registrations_pages.route('/signup', methods=["POST"])
def create():
    form = RegistrationForm()
    if form.validate_on_submit() and form.password.data == form.password_confirmation.data:
        db.add_user(form.name.data, form.email.data, form.password.data)
        flash(u'The new user has been added successfully', "success")
        return redirect(url_for("categories.index"))
    else:
        flash(u'Failed to add new user', "danger")
        return redirect(url_for("registrationsCreate"))
