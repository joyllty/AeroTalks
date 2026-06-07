const socket = io();

socket.on("connect", function () {
  console.log("Conectado ao WebSocket:", socket.id);
});

socket.on("disconnect", function () {
  console.log("Desconectado do WebSocket");
});

socket.on("erro_socket", function (data) {
  mostrarNotif(data.erro || "Erro no WebSocket");
});


//nova mensagem
socket.on("nova_mensagem", function (m) {
  //  se a mensagem for de outra pessoa, mostra na tela
  if (m.usuario !== meuUser) {
    renderMsg(m.usuario, m.texto, m.expiraEm, false);
  }
});

//atualiza a lista  mostrando quem ta online na sala
socket.on("usuarios_online", function (data) {
  renderUsuarios(data.usuarios);
});

//notificacoes de quem entra e sai da sala
socket.on("usuario_entrou", function (data) {
  if (data.usuario !== meuUser) {
    mostrarNotif(`O usuário ${data.usuario} entrou na sala.`);
  }
});

socket.on("usuario_saiu", function (data) {
  mostrarNotif(`O usuário ${data.usuario} saiu da sala.`);
});

// novo socket: atualiza a lista de salas em tempo real
socket.on("atualizar_salas", function () {
  carregarSalas();
});

// expulsa o usuario se o dono deletar a sala enquanto ele tiver dentro
socket.on("sala_destruida", function (data) {
  if (salaAtual === data.sala) {
    mostrarNotif("A sala foi encerrada pelo criador!");
    voltarLobby();
  }
});

/*
"nova_mensagem", OK
"usuarios_online", OK
"usuario_entrou", OK
"usuario_saiu" OK
 */