from flask import Blueprint
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, request, render_template, redirect, g, flash, url_for, session,jsonify
from forms import Form
from dbm import db

"""
Resource : Categories
"""
categories_pages = Blueprint('categories',
                           __name__,
                           template_folder='templates')

@categories_pages.route('/')
@categories_pages.route('/categories', methods=["GET"])
def index():
    return render_template("categories/index.html", title="Index")


@categories_pages.route('/categories/json', methods=["GET"])
def indexJson():
    return jsonify([categorie.serialize for categorie in g.categories])


@categories_pages.route('/categories/new', methods=["GET"])
@login_required
def new():
    if current_user.id != 1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categories.index"))
    form = Form()
    return render_template("categories/new.html", title="Add new category", form=form)


@categories_pages.route('/categories/<int:id>/edit', methods=["GET"])
@login_required
def edit(id):
    if current_user.id != 1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categories.index"))
    form = Form()
    categorie = db.get_categorie(id)
    form.name.data = categorie.name
    form.description.data = categorie.description
    return render_template("categories/edit.html", form=form, categorie=categorie)


@categories_pages.route('/categories', methods=["POST"])
@login_required
def create():
    if current_user.id != 1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categories.index"))
    form = Form()
    if form.validate_on_submit():
        db.add_categorie(form.name.data, form.description.data)
        flash(u'The new catergorie has been added successfully', "success")
    else:
        flash(u'Failed to add new categorie', "danger")
    return redirect(url_for("categories.index"))


@categories_pages.route('/categories/<int:id>/edit', methods=["POST"])
@login_required
def update(id):
    if current_user.id != 1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categories.index"))
    form = Form()
    if form.validate_on_submit():
        db.update_categorie(id, form.name.data, form.description.data)
        flash(u'The catergorie has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("categories.index"))


@categories_pages.route('/categories/<int:id>/delete', methods=["POST"])
@login_required
def destroy(id):
    if current_user.id != 1:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("categories.index"))
    db.delete_categorie(id)
    flash(u'The catergorie was deleted successfully', "success")
    return redirect(url_for("categories.index"))
