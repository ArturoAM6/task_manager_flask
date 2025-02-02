# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from .models import PriorityEnum
import re

def validate_username(form, field):
    if not re.match(r'^\w+$', field.data):
        raise ValidationError('Username can only contain letters, numbers and underscores and not whitespaces.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150), validate_username])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=150)])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=150), validate_username])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=150)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='The passwords must be the same.')])

class BaseTaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[Length(max=300)])
    priority = SelectField('Priority', choices=[(p.name, p.value) for p in PriorityEnum], validators=[InputRequired()])

class AddTaskForm(BaseTaskForm):
    pass

class EditTaskForm(BaseTaskForm):
    pass
