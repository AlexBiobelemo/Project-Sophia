# run.py

from app import create_app, db
from app.models import User, Snippet # We will create these models soon

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provides a shell context for 'flask shell' command."""
    return {'db': db, 'User': User, 'Snippet': Snippet}
