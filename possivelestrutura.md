aerotalks/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── message.py
│   │   └── room_participant.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── room_routes.py
│   │   └── message_routes.py
│   │
│   ├── sockets/
│   │   ├── __init__.py
│   │   └── chat_events.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── room_service.py
│   │   ├── message_service.py
│   │   └── redis_service.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── room_schema.py
│   │   └── message_schema.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── decorators.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── global.css
│   │   │   ├── login.css
│   │   │   ├── rooms.css
│   │   │   └── chat.css
│   │   │
│   │   ├── js/
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   ├── rooms.js
│   │   │   ├── chat.js
│   │   │   └── socket.js
│   │   │
│   │   └── img/
│   │       └── logo.png
│   │
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── rooms.html
│       └── chat_room.html
│
├── migrations/
│
├── tests/
│   ├── test_auth.py
│   ├── test_rooms.py
│   └── test_messages.py
│
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md