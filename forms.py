from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

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


class LoginForm(FlaskForm):
    email = EmailField('Email address:', validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])

    def __init__(self):
        super(LoginForm, self).__init__(csrf_enabled=True)
