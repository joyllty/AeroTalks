'''
arquivo principal para executar a aplicação Flask / ponto de entrada do projeto

executa ele quando quiser iniciar o servidor
'''
import os

from app import create_app
from app.extensions import socketio


# cria a aplicação Flask chamando a factory create_app()
app = create_app()


if __name__ == "__main__":

    # se não existir variavel PORT, vai entrar na porta 5000
    # pra mudar de porta, chame PORT quando for rodar o código, exemplo:
    # $env:PORT=5001; python run.py
    porta = int(os.getenv("PORT", 5000))

    # inicia o servidor Flask usando SocketIO
    # se fosse uma API Flask comum, poderia ser app.run()
    socketio.run(app,

        # permite que a aplicação aceite conexões externas tambem, não apenas do próprio computador
        host="0.0.0.0",

        # porta onde o servidor vai rodar
        port=porta,

        # ativa o modo debug durante o desenvolvimento, mostra erros detalhados e reinicia o servidor quando o código muda.
        debug=True,

        # se o código for alterado enquanto está rodandd, não recarrega
        use_reloader=False
    )