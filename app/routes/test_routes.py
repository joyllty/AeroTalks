'''
rotas básicas/ de teste pra ver se a API está funcionando
'''

# Blueprint permite separar as rotas em arquivos diferentes
from flask import Blueprint, jsonify

# cria um grupo de rotas chamado "health"
# o primeiro argumento é o nome interno do Blueprint
# o segundo argumento (__name__) ajuda o Flask a localizar esse arquivo
health_bp = Blueprint("health", __name__)


# define uma rota GET para a raiz do servidor
@health_bp.route("/", methods=["GET"])
def home():
    '''
    rota inicial da API
    serve apenas para verificar se o servidor Flask está respondendo
    '''
    return jsonify({'message': 'API do chat funcionando!'}), 200


# define uma rota GET para verificar o status da API
@health_bp.route("/api/health", methods=["GET"])
def health_check():
    '''
    rota de status da API

    se essa rota responder com "online", significa que a aplicação Flask está rodando
    '''
    return jsonify({'status': 'online'}), 200