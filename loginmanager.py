from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from dbm import db

login_manager = LoginManager()

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

