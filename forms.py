from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FightForm(FlaskForm):
    city = StringField('City')
    country = StringField('Country')
    description = StringField('Description')
    submit = SubmitField('Post')

class FighterForm(FlaskForm):
  Name = StringField('Name')
  Surname = StringField('Surname')
  weight_classes = [
        ('Flyweight', 'Flyweight (125 lb / 56.7 kg)'),
        ('Bantamweight', 'Bantamweight (135 lb / 61.2 kg)'),
        ('Featherweight', 'Featherweight (145 lb / 65.8 kg)'),
        ('Lightweight', 'Lightweight (155 lb / 70.3 kg)'),
        ('Super Lightweight', 'Super Lightweight (165 lb / 74.8 kg)'),
        ('Welterweight', 'Welterweight (170 lb / 77.1 kg)'),
        ('Super Welterweight', 'Super Welterweight (175 lb / 79.4 kg)'),
        ('Middleweight', 'Middleweight (185 lb / 83.9 kg)'),
        ('Super Middleweight', 'Super Middleweight (195 lb / 88.5 kg)'),
        ('Light Heavyweight', 'Light Heavyweight (205 lb / 93.0 kg)'),
        ('Cruiserweight', 'Cruiserweight (225 lb / 102.1 kg)'),
        ('Heavyweight', 'Heavyweight (265 lb / 120.2 kg)'),
    ]
  weight_class = SelectField('Select Weight Class:', choices=weight_classes, validators=[DataRequired()])
  Team = StringField('Team')
  Coach = StringField('Coach')
  submit = SubmitField('Add Fighter')
