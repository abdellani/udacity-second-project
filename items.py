from flask import Blueprint
from flask_login import LoginManager, login_user,\
    logout_user, login_required, current_user
from flask import Flask, request, render_template,\
    redirect, g, flash, url_for, session, jsonify
from forms import Form
from dbm import db
"""
Resource: Items
"""
items_pages = Blueprint('items',
                        __name__,
                        template_folder='templates')


@items_pages.route('/categories/<int:cat_id>/items', methods=["GET"])
def index(cat_id):
    categorie = db.get_categorie(cat_id)
    return render_template("items/index.html", categorie=categorie)


@items_pages.route('/categories/<int:cat_id>/items/json', methods=["GET"])
def indexJson(cat_id):
    categorie = db.get_categorie(cat_id)
    return jsonify(categorie.serialize)


@items_pages.route('/categories/<int:cat_id>/items/new', methods=["GET"])
@login_required
def new(cat_id):
    form = Form()
    categorie = db.get_categorie(cat_id)
    return render_template("items/new.html",
                           title="Add new item",
                           categorie=categorie,
                           form=form)


@items_pages.route('/categories/<int:cat_id>/items/<int:item_id>',
                   methods=["GET"])
def show(cat_id, item_id):
    categorie = db.get_categorie(cat_id)
    item = db.get_item(item_id)
    return render_template("items/show.html",
                           title="item details",
                           categorie=categorie,
                           item=item)


@items_pages.route('/categories/<int:cat_id>/items/<int:item_id>/json',
                   methods=["GET"])
def showJson(cat_id, item_id):
    item = db.get_item(item_id)
    return jsonify(item.serialize)


@items_pages.route('/categories/<int:cat_id>/items/<int:item_id>/edit',
                   methods=["GET"])
@login_required
def edit(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id != item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("items.index", cat_id=cat_id))
    categorie = db.get_categorie(cat_id)
    form = Form()
    form.name.data = item.name
    form.description.data = item.description
    return render_template("items/edit.html",
                           title="Edit item",
                           categorie=categorie,
                           item=item,
                           form=form)


@items_pages.route('/categories/<int:cat_id>/items', methods=["POST"])
@login_required
def create(cat_id):
    form = Form()
    if form.validate_on_submit():
        db.add_item(current_user.id, cat_id,
                    form.name.data, form.description.data)
        flash(u'The new item has been added successfully', "success")
    else:
        flash(u'Failed to add item', "danger")
    return redirect(url_for("items.index", cat_id=cat_id))


@items_pages.route('/categories/<int:cat_id>/items/<int:item_id>/edit',
                   methods=["POST"])
@login_required
def update(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id != item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("items.index", cat_id=cat_id))
    form = Form()
    if form.validate_on_submit():
        db.update_item(item_id, form.name.data, form.description.data)
        flash(u'The item has been updated successfully', "success")
    else:
        flash(u'Failed to update categorie', "danger")
    return redirect(url_for("items.index", cat_id=cat_id))


@items_pages.route('/categories/<int:cat_id>/items/<int:item_id>/delete',
                   methods=["POST"])
@login_required
def destroy(cat_id, item_id):
    item = db.get_item(item_id)
    if current_user.id != item.user_id:
        flash(u'You are not authorized !', "danger")
        return redirect(url_for("items.index", cat_id=cat_id))
    db.delete_item(item_id)
    flash(u'The item has been deleted successfully', "success")
    return redirect(url_for("items.index", cat_id=cat_id))
