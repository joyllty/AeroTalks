# AeroTalks

O projeto consiste em uma aplicação web de bate-papo em tempo real, com salas temáticas e mensagens temporárias. 
Possui comunicação via WebSocket, persistência em banco de dados e integração com Redis para suporte a escalabilidade horizontal.


# Acesso Rápido - Produção

O projeto está implantado na Railway e pode ser acessado pelo link:

https://aerotalks-production.up.railway.app/

# Estrutura do Repositório
```txt
AeroTalks/
├── app/
│   ├── models/        # Models do banco de dados
│   ├── routes/        # Rotas HTTP 
│   ├── sockets/       # Eventos WebSocket com Socket.IO
│   ├── static/        # Arquivos CSS e JavaScript
│   ├── templates/     # Página HTML principal
│   ├── config.py      # Configurações da aplicação
│   ├── extensions.py  # Inicialização das extensões Flask
│   └── __init__.py    # Factory da aplicação Flask
│
├── migrations/        # Migrations do banco com Flask-Migrate
├── run.py             # Arquivo para iniciar a aplicação
├── requirements.txt   # Dependências do projeto
├── railway.toml       # Configuração de deploy na Railway
└── README.md
```
