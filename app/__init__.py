from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, socketio

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    from app.routes.test_routes import health_bp
    app.register_blueprint(health_bp)

    return app