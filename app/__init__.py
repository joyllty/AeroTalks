from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio

# IMPORTANTE: Importar os modelos AQUI EM CIMA para o Flask-Migrate os conseguir detetar!
from app.models.user import User
from app.models.room import Room
from app.models.message import Message

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Registando as rotas
    from app.routes.test_routes import health_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.chat_routes import chat_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    return app