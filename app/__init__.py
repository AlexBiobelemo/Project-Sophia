# app/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import sqlalchemy as sa # Import sqlalchemy

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # The route for the login page
login_manager.login_message_category = 'info' # Flash message category


def create_app(config_class=Config):
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Import models here to ensure they are registered with the app
    from app import models

    # Helper function for gamification
    def award_points(user, points, activity):
        point_entry = models.Point(user_id=user.id, points=points, activity=activity)
        db.session.add(point_entry)
        db.session.commit()
        # Optionally, check for badges here
        check_for_badges(user)

    def check_for_badges(user):
        all_badges = db.session.scalars(sa.select(models.Badge)).all()
        for badge in all_badges:
            criteria_parts = badge.criteria.split(':')
            if len(criteria_parts) == 2:
                criteria_type = criteria_parts[0]
                criteria_value = int(criteria_parts[1])

                if criteria_type == 'snippets_created':
                    count = user.snippets.count()
                    if count >= criteria_value:
                        award_badge(user, badge)
                elif criteria_type == 'solutions_approved':
                    count = user.leetcode_solutions.filter_by(approved=True).count()
                    if count >= criteria_value:
                        award_badge(user, badge)
                # Add more criteria types as needed

    def award_badge(user, badge):
        # Check if user already has this badge
        existing_badge = db.session.scalar(
            sa.select(models.UserBadge).where(
                models.UserBadge.user_id == user.id,
                models.UserBadge.badge_id == badge.id
            )
        )
        if not existing_badge:
            user_badge = models.UserBadge(user_id=user.id, badge_id=badge.id)
            db.session.add(user_badge)
            db.session.commit()
            # Optionally, award points for earning a badge
            award_points(user, 50, f"Earned badge: {badge.name}")
            # flash(f'Congratulations! You earned the "{badge.name}" badge!', 'success')


    app.award_points = award_points
    app.check_for_badges = check_for_badges

    return app
