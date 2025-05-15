from flask import Flask
from app.database import db, migrate
from app.config import Config
from flask_socketio import SocketIO
from dotenv import load_dotenv

socketio = SocketIO(cors_allowed_origins="*")  # SocketIO global

def create_app():
    load_dotenv()  # Carga variables de entorno del .env

    app = Flask(__name__)
    app.config.from_object(Config)  # Carga configuración desde Config

    db.init_app(app)        # Inicializa SQLAlchemy con la app
    migrate.init_app(app, db)  # Inicializa Flask-Migrate
    socketio.init_app(app)  # Inicializa SocketIO con la app

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from app import sockets  # Importa eventos SocketIO para registrar

    return app

