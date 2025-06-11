from flask import Flask
from app.config import Config
from app.extensions import db, migrate, socketio
from dotenv import load_dotenv


def create_app():
    
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app import sockets  # Registrar eventos del socket

    return app
