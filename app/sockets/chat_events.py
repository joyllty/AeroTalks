
from flask_socketio import join_room, leave_room, emit
from app.extensions import db
from app.models.room import Room
from app.models.message import Message
import time


# Dicionário para controlar usuários online em memória
# Para um servidor Flask só, isso funciona, futuramente, pode ir pro Redis
usuarios_por_sala = {}


def registrar_eventos_socket(socketio):
    '''
    Registra todos os eventos WebSocket do chat
    '''

    @socketio.on("entrar_sala")
    def entrar_sala(data):
        '''
        Evento chamado quando o usuário entra em uma sala

        Espera receber:
        {
            "sala": "nome da sala",
            "usuario": "nome do usuário"
        }
        '''

        nome_sala = data.get("sala")
        usuario = data.get("usuario")

        if not nome_sala or not usuario:
            emit("erro_socket", {"erro": "Sala e usuário são obrigatórios"})
            return

        sala = Room.query.filter_by(name=nome_sala).first()

        if not sala:
            emit("erro_socket", {"erro": "Sala não encontrada"})
            return

        # Coloca este cliente dentro da room do SocketIO
        join_room(nome_sala)

        # Adiciona usuário na lista de online da sala
        if nome_sala not in usuarios_por_sala:
            usuarios_por_sala[nome_sala] = set()

        usuarios_por_sala[nome_sala].add(usuario)

        # Avisa todos da sala que a lista de usuários mudou
        emit("usuarios_online", {
            "sala": nome_sala,
            "usuarios": list(usuarios_por_sala[nome_sala])
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

        nome_sala = data.get("sala")
        usuario = data.get("usuario")

        if not nome_sala or not usuario:
            return

        leave_room(nome_sala)

        if nome_sala in usuarios_por_sala:
            usuarios_por_sala[nome_sala].discard(usuario)

            if len(usuarios_por_sala[nome_sala]) == 0:
                del usuarios_por_sala[nome_sala]

        emit("usuario_saiu", {
            "sala": nome_sala,
            "usuario": usuario
        }, to=nome_sala)

        emit("usuarios_online", {
            "sala": nome_sala,
            "usuarios": list(usuarios_por_sala.get(nome_sala, []))
        }, to=nome_sala)

    @socketio.on("enviar_mensagem")
    def enviar_mensagem(data):
        """
        Evento chamado quando o usuário envia uma mensagem
        """
        nome_sala = data.get("sala")
        usuario = data.get("usuario")
        texto = data.get("texto")
        expira_em = data.get("expiraEm")

        if not nome_sala or not usuario or not texto:
            return

        sala = Room.query.filter_by(name=nome_sala).first()
        if not sala:
            emit("erro_socket", {"erro": "Sala não encontrada"})
            return

        # salva no banco de dados
        nova_msg = Message(room_id=sala.id, username=usuario, content=texto, expires_at=expira_em)
        db.session.add(nova_msg)
        db.session.commit()

        # mostra amensagem instantaneamente pra todo mundo da sala
        emit("nova_mensagem", {
            "usuario": usuario,
            "texto": texto,
            "expiraEm": expira_em
        }, to=nome_sala)


    
    # - ja adicionei os eventos no app/__init__.py,
    # - coloquei o socket no script do html, 
    # - modifiquei a função entrarNaSala() em static/js/chat.js, agora eles entram na sala via websocket, 
    # e não fica chamando a api a todo segundo
    # - 

    # agora ta faltando:
    # - terminar essa função de enviar_mensagem ali em cima,
    # - terminar o arquivo socket.js no static/js/socket.js,
    # - alterar a função enviar() em static/js/chat.js, agora deve emitir socket.emit("enviar_mensagem", ...), e não usar apiPost("/mensagens")
    # - alterar a função voltarLobby() em static/js/ui.js, agora deve emitir socket.emit("sair_sala", ...) antes de limpar salaAtual
    # - modificar static/js/chat.js,
    # - emitir evento de saída da sala em voltarLobby() em static/js/ui.js