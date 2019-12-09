from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_artist = BooleanField('Check if Artist')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class NewBandForm(FlaskForm):
    bandName = StringField('Artist Name', validators=[DataRequired()])
    bio = TextAreaField("Description", validators=[DataRequired()])
    image = StringField('Image (Test for now)', validators=[DataRequired()])
    link = StringField('Upload a link to one of your songs')
    address = StringField('Address of your porch', validators=[DataRequired()])
    time = TimeField('Time of performance', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class EditBandForm(FlaskForm):
    bio = TextAreaField("Description", validators=[DataRequired()])
    image = StringField('Image (Test for now)', validators=[DataRequired()])
    link = StringField('Upload a link to one of your songs')
    address = StringField('Address of your porch', validators=[DataRequired()])
    time = TimeField('Time of performance', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

