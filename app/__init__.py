from flask import Flask
from app.database import db, migrate
from app.config import Config
from flask_socketio import SocketIO
from dotenv import load_dotenv

socketio = SocketIO(cors_allowed_origins="*")   # SocketIO global

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app import sockets  # <- Esto es suficiente para registrar eventos

    return app
