from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.room import Room
from app.models.message import Message
import time

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/api/salas", methods=["GET"])
def listar_salas():
    salas = Room.query.all()
    return jsonify([sala.name for sala in salas]), 200

@chat_bp.route("/api/salas", methods=["POST"])
def criar_sala():
    data = request.get_json()
    nome = data.get("nome")

    if not nome:
        return jsonify({"erro": "Nome obrigatório"}), 400

    if not Room.query.filter_by(name=nome).first():
        nova_sala = Room(name=nome)
        db.session.add(nova_sala)
        db.session.commit()
        return jsonify({"mensagem": "Sala criada"}), 201

    return jsonify({"mensagem": "Sala já existe"}), 200

@chat_bp.route("/api/mensagens", methods=["GET"])
def listar_mensagens():
    nome_sala = request.args.get("sala")
    sala = Room.query.filter_by(name=nome_sala).first()

    if not sala:
        return jsonify([]), 200

    agora = int(time.time() * 1000)
    mensagens = Message.query.filter(Message.room_id == sala.id, Message.expires_at > agora).all()

    return jsonify([{"usuario": m.username, "texto": m.content, "expiraEm": m.expires_at} for m in mensagens]), 200

@chat_bp.route("/api/mensagens", methods=["POST"])
def enviar_mensagem():
    data = request.get_json()
    sala = Room.query.filter_by(name=data.get("sala")).first()
    
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404

    nova_msg = Message(room_id=sala.id, username=data.get("usuario"), content=data.get("texto"), expires_at=data.get("expiraEm"))
    db.session.add(nova_msg)
    db.session.commit()

    return jsonify({"mensagem": "Mensagem salva"}), 201

@chat_bp.route("/api/usuarios", methods=["GET"])
def listar_usuarios():
    nome_sala = request.args.get("sala")
    sala = Room.query.filter_by(name=nome_sala).first()
    
    if not sala:
        return jsonify([]), 200
        
    agora = int(time.time() * 1000)
    mensagens = Message.query.filter(Message.room_id == sala.id, Message.expires_at > agora).all()
    
    return jsonify(list(set([m.username for m in mensagens]))), 200