"""Database models for the Sophia application."""

from datetime import datetime
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login.
    Reloads the user object from the user ID stored in the session.
    """
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    """Represents a user in the database."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(256))

    snippets = db.relationship('Snippet', backref='author', lazy='dynamic')
    collections = db.relationship('Collection', backref='owner', lazy='dynamic')

    __table_args__ = (
        db.Index('ix_user_username', 'username', unique=True),
        db.Index('ix_user_email', 'email', unique=True),
    )

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the user's hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """String representation of the User object."""
        return f'<User {self.username}>'


class Collection(db.Model):
    """Represents a user-defined collection for organizing snippets."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    snippets = db.relationship('Snippet', backref='collection', lazy='dynamic')

    __table_args__ = (
        db.Index('ix_collection_timestamp', 'timestamp'),
        db.Index('ix_collection_user_id', 'user_id'),
    )

    def __repr__(self):
        """String representation of the Collection object."""
        return f'<Collection {self.name}>'


class Snippet(db.Model):
    """Represents a code snippet in the database."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    code = db.Column(db.Text)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.Column(db.String(200), nullable=True)
    embedding = db.Column(db.JSON, nullable=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=True)
    language = db.Column(db.String(50), nullable=False, default='python')

    __table_args__ = (
        db.Index('ix_snippet_timestamp', 'timestamp'),
        db.Index('ix_snippet_user_id', 'user_id'),
    )

    def generate_and_set_embedding(self):
        """Generates and saves a vector embedding for the snippet's content."""
        # Import locally to avoid circular dependencies at startup
        from app import ai_services

        # Combine the most important text fields for a rich embedding
        text_to_embed = f"Title: {self.title}\nDescription: {self.description}\nCode: {self.code}"
        self.embedding = ai_services.generate_embedding(
            text_to_embed, task_type="RETRIEVAL_DOCUMENT")

    def __repr__(self):
        """String representation of the Snippet object."""
        return f'<Snippet {self.title}>'