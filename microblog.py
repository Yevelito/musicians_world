from app import create_app, db, cli
from app.models import User, Album, Song

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Album': Album, 'Song': Song}
