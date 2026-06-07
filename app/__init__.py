from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio

from app.models.user import User
from app.models.room import Room
from app.models.message import Message

from app.routes.test_routes import health_bp
from app.routes.auth_routes import auth_bp
from app.routes.chat_routes import chat_bp


from app.sockets.chat_events import registrar_eventos_socket

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    socketio.init_app(app, cors_allowed_origins="*")

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    registrar_eventos_socket(socketio)

    return app