from flask_wtf import FlaskForm 
from wtforms import StringField, TextField, PasswordField
from wtforms.validators import InputRequired, Length, Email



class RegisterUserForm(FlaskForm):
    """Register user form"""

    username = StringField('Username', validators=[InputRequired(), Length(min=1,max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=5,max=25)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])


class LoginUserForm(FlaskForm):
    """ Login form"""

    username = StringField('Username', validators=[InputRequired(),Length(min=1,max=20)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=5,max=25)])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = TextField('content', validators=[InputRequired()])