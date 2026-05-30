'''
quando tiver as rotas prontas, registrar blueprints aqui!!
'''
from flask import Flask

# configuracoes do projeto
from app.config import Config

from app.extensions import db, migrate, jwt, socketio


def create_app():
    '''
    criar e configurar flask.

    esse padrão é chamado de Application Factory.
    '''

    # instancia principal do flask
    app = Flask(__name__)

    # configura as configs definidas na classe Config,
    # elas vem principalmente do .env
    app.config.from_object(Config)

    # inicializa o SQLAlchemy dentro do app flask
    db.init_app(app)

    # inicializa o Flask-Migrate, pra migracoes do banco
    migrate.init_app(app, db)

    # inicializa JWT, criar e validar tokens de autenticacao
    jwt.init_app(app)

    # inicializa o SocketIO
    # cors_allowed_origins="*" permite conexões de qualquer origem
    socketio.init_app(app, cors_allowed_origins="*")

    '''
    from app.routes.auth_routes import auth_bp
    from app.routes.room_routes import room_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    '''
    return app