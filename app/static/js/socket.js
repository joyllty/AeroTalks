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

/*
!!!!!!!!!!!!!!!!!!!
falta listeners para:
"nova_mensagem",
"usuarios_online",
"usuario_entrou",
"usuario_saiu"
 */