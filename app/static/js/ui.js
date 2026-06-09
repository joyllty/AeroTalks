function atualizarRelogio() {
  const d = new Date();
  const h = String(d.getHours()).padStart(2, "0");
  const m = String(d.getMinutes()).padStart(2, "0");

  document.getElementById("relogio").innerText = h + ":" + m;
}

function mostrarNotif(txt) {
  document.getElementById("notif-text").innerHTML = txt;
  document.getElementById("notif").style.display = "block";
  setTimeout(fecharNotif, 4000);
}

function fecharNotif() {
  document.getElementById("notif").style.display = "none";
}

function abrirLobby() {
  document.getElementById("win-lobby").style.display = "block";
  document.getElementById("task-lobby").classList.add("active");
  carregarSalas();
}

function mostrarChat() {
  document.getElementById("win-chat").style.display = "block";
}

function voltarLobby() {
  if (salaAtual) {
    socket.emit("sair_sala", {
      sala: salaAtual,
      usuario: meuUser
    });
  }

  salaAtual = "";

  document.getElementById("win-chat").style.display = "none";
  document.getElementById("task-chat").style.display = "none";
  document.getElementById("task-lobby").classList.add("active");

  abrirLobby();
}

function trocarAba(aba) {
  document.getElementById("form-login").style.display = aba === "login" ? "flex" : "none";
  document.getElementById("form-cadastro").style.display = aba === "cadastro" ? "flex" : "none";

  document.getElementById("tab-login").classList.toggle("active", aba === "login");
  document.getElementById("tab-cadastro").classList.toggle("active", aba === "cadastro");
}

function fecharAuth() {
  document.getElementById("win-auth").style.display = "none";
  document.getElementById("auth-overlay").style.display = "none";
  document.getElementById("win-lobby").style.display = "block";

  carregarSalas();
}