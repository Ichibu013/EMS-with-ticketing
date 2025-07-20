from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,FloatField,IntegerField,DateTimeLocalField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User


class \
        RegistrationFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    start_date = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Event Location', validators=[DataRequired(), Length(min=2, max=100)])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    ticket_price = FloatField('Ticket Price', validators=[DataRequired()])

    submit = SubmitField('Create Event')