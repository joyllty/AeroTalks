'''
centraliza extensoes do flask
'''
import os
import redis

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# URL do Redis vinda do .env
REDIS_URL = os.getenv("REDIS_URL")

# cliente Redis para salvar dados temporários, como usuários online
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# SocketIO usando Redis como fila de mensagens
# isso permite que duas instâncias Flask troquem eventos entre si
socketio = SocketIO(async_mode="threading", message_queue=REDIS_URL)