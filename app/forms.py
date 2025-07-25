"""Defines the forms used in the Sophia application."""

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                   TextAreaField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from app import db
from app.models import User


class RegistrationForm(FlaskForm):
    """Form for new user registration."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Checks if the username is already taken."""
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Checks if the email is already in use."""
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SnippetForm(FlaskForm):
    """Form for creating and editing a code snippet."""
    title = StringField('Title', validators=[
                        DataRequired(), Length(min=1, max=140)])
    collection = SelectField('Collection (Optional)', coerce=int)
    language = SelectField('Language', choices=[
        ('bash', 'Bash/Shell'),
        ('c', 'C'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('css', 'CSS'),
        ('dart', 'Dart'),
        ('go', 'Go'),
        ('html', 'HTML'),
        ('java', 'Java'),
        ('javascript', 'JavaScript'),
        ('json', 'JSON'),
        ('kotlin', 'Kotlin'),
        ('markdown', 'Markdown'),
        ('php', 'PHP'),
        ('python', 'Python'),
        ('ruby', 'Ruby'),
        ('rust', 'Rust'),
        ('sql', 'SQL'),
        ('swift', 'Swift'),
        ('typescript', 'TypeScript'),
        ('yaml', 'YAML')
    ])
    description = TextAreaField('Description (Optional)')
    code = TextAreaField('Code', validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)',
                       validators=[Length(max=200)])
    submit = SubmitField('Save Snippet')


class AIGenerationForm(FlaskForm):
    """Form for submitting a prompt to the AI for code generation."""
    prompt = TextAreaField(
        'Describe the code you want to generate',
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    submit = SubmitField('Generate Code')


class CollectionForm(FlaskForm):
    """Form for creating or renaming a collection."""
    name = StringField('Collection Name', validators=[
                       DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Create Collection')

