'''
eventos em tempo real do chat.
utiliza socketio para trabalhar com eventos: 
- entrar_sala
- sair_sala
- enviar_mensagem
- nova_mensagem
- usuarios_online
'''

from flask_socketio import join_room, leave_room, emit
from app.extensions import db, redis_client
from app.models.room import Room
from app.models.message import Message


def chave_usuarios_sala(nome_sala):
    '''
    Cria o nome da chave usada no Redis para guardar os usuários online de uma sala
    '''
    return f"sala:{nome_sala}:usuarios"


def registrar_eventos_socket(socketio):
    '''
    Registra todos os eventos WebSocket do chat
    '''

    @socketio.on("entrar_sala")
    def entrar_sala(data):
        '''
        Evento chamado quando o usuário entra em uma sala
        '''

        # pega os dados
        nome_sala = data.get("sala")
        usuario = data.get("usuario")

        # verifica se vieram dados
        if not nome_sala or not usuario:
            emit("erro_socket", {"erro": "Sala e usuário são obrigatórios"})
            return

        # verifica se a sala existe no banco!!
        sala = Room.query.filter_by(name=nome_sala).first()

        # se a sala nao existir
        if not sala:
            emit("erro_socket", {"erro": "Sala não encontrada"})
            return

        # estabelecendo essa conexão WebSocket à tal sala
        # Coloca este cliente dentro da room do SocketIO
        join_room(nome_sala)

        # Salva o usuário online no Redis
        chave = chave_usuarios_sala(nome_sala)
        redis_client.sadd(chave, usuario)

        # Faz a lista de chaves expirar automaticamente depois de 1 hora
        # não expulsa ninguem da sala, mas remove a lista de usuários online
        # pra caso alguem saia sem desconectar/ funciona como limpeza automatica
        redis_client.expire(chave, 3600)

        usuarios = list(redis_client.smembers(chave))

        # Envia a lista de usuários para todos na sala
        emit("usuarios_online", {
            "sala": nome_sala,
            "usuarios": usuarios
        }, to=nome_sala)

        # Avisa todos da sala que alguém entrou
        emit("usuario_entrou", {
            "sala": nome_sala,
            "usuario": usuario
        }, to=nome_sala)


    @socketio.on("sair_sala")
    def sair_sala(data):
        '''
        Evento chamado quando o usuário sai de uma sala
        '''
        # pega os dados
        nome_sala = data.get("sala")
        usuario = data.get("usuario")

        if not nome_sala or not usuario:
            return

        # tira a conexão do socket daquela sala
        leave_room(nome_sala)

        chave = chave_usuarios_sala(nome_sala)

        # Remove o usuário da lista de online no Redis
        redis_client.srem(chave, usuario)

        usuarios = list(redis_client.smembers(chave))

        # envia para todos na sala que o usuario saiu
        emit("usuario_saiu", {
            "sala": nome_sala,
            "usuario": usuario
        }, to=nome_sala)

        # envia a lista atualizada de onlines naquela sala
        emit("usuarios_online", {
            "sala": nome_sala,
            "usuarios": usuarios
        }, to=nome_sala)

    @socketio.on("enviar_mensagem")
    def enviar_mensagem(data):
        """
        Evento chamado quando o usuário envia uma mensagem
        """

        # pega os dados
        nome_sala = data.get("sala")
        usuario = data.get("usuario")
        texto = data.get("texto")
        expira_em = data.get("expiraEm")

        if not nome_sala or not usuario or not texto:
            emit("erro_socket", {"erro": "Dados incompletos"})
            return

        # verifica se a sala existe no banco!!
        sala = Room.query.filter_by(name=nome_sala).first()

        if not sala:
            emit("erro_socket", {"erro": "Sala não encontrada"})
            return

        # salva a mensagem no banco de dados
        nova_msg = Message(room_id=sala.id, username=usuario, content=texto, expires_at=expira_em)
        db.session.add(nova_msg)
        db.session.commit()

        # mostra amensagem instantaneamente pra todo mundo da sala
        emit("nova_mensagem", {
            "sala": nome_sala,
            "usuario": usuario,
            "texto": texto,
            "expiraEm": expira_em
        }, to=nome_sala)


