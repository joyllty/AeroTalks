from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/auth/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    email = data.get("email")
    usuario = data.get("usuario")
    senha = data.get("senha")

    if User.query.filter_by(username=usuario).first() or User.query.filter_by(email=email).first():
        return jsonify({"erro": "Usuário ou email já cadastrado"}), 400

    novo_usuario = User(username=usuario, email=email)
    novo_usuario.set_password(senha)
    
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"mensagem": "Conta criada com sucesso"}), 201

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    senha = data.get("senha")

    user = User.query.filter_by(username=usuario).first()
    if user and user.check_password(senha):
        return jsonify({"mensagem": "Login aprovado"}), 200
    
    return jsonify({"erro": "Usuário ou senha incorretos"}), 401