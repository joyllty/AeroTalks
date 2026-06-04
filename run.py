'''
arquivo principal para executar a aplicação Flask / ponto de entrada do projeto

executa ele quando quiser iniciar o servidor
'''

# função que cria e configura o Flask
from app import create_app

# iniciar o servidor com suporte a WebSocket
from app.extensions import socketio


# cria a aplicação Flask chamando a factory create_app()
app = create_app()


if __name__ == "__main__":

    # inicia o servidor Flask usando SocketIO
    # se fosse uma API Flask comum, poderia ser app.run()
    socketio.run(app,

        # permite que a aplicação aceite conexões externas tambem, não apenas do próprio computador
        host="0.0.0.0",

        # porta onde o servidor vai rodar, http://localhost:5000
        port=5000,

        # ativa o modo debug durante o desenvolvimento, mostra erros detalhados e reinicia o servidor quando o código muda.
        debug=True
    )