function entrarNaSala(nome) {
  salaAtual = nome;

  document.getElementById("win-lobby").style.display = "none";
  document.getElementById("win-chat").style.display = "block";

  document.getElementById("nome-sala-atual").innerText = nome;
  document.getElementById("nome-sala-titulo").innerText = nome;

  document.getElementById("task-chat").style.display = "block";
  document.getElementById("task-chat").innerText = "💬 " + nome;

  document.getElementById("task-lobby").classList.remove("active");
  document.getElementById("task-chat").classList.add("active");

  document.getElementById("container-msgs").innerHTML =
    `<div class="msg-sys">Entrou em <em>${nome}</em> — ⏱ msgs somem em 60min</div>`;


  // busca histórico uma vez ao entrar
  buscarMsgs();

  // entra na sala via WebSocket
  socket.emit("entrar_sala", {
    sala: nome,
    usuario: meuUser
  });
}

async function buscarUsuarios() {
  if (!salaAtual) return;

  let lista = [meuUser];

  try {
    const data = await apiGet(`/usuarios?sala=${encodeURIComponent(salaAtual)}`);

    if (data.length > 0) {
      lista = data;
    }
  } catch (e) {}

  renderUsuarios(lista);
}

function renderUsuarios(lista) {
  const box = document.getElementById("lista-usuarios");
  box.innerHTML = "";

  lista.forEach(u => {
    const div = document.createElement("div");
    div.className = "user-row" + (u === meuUser ? " me" : "");
    div.innerHTML = `<span class="udot"></span>${u}${u === meuUser ? " (você)" : ""}`;
    box.appendChild(div);
  });
}

function checarEnter(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    enviar();
  }
}

async function enviar() {
  const inp = document.getElementById("input-msg");
  const txt = inp.value.trim();

  if (!txt) return;

  const exp = Date.now() + TTL;

  renderMsg(meuUser, txt, exp, true);

  inp.value = "";

socket.emit("enviar_mensagem", {
    sala: salaAtual,
    usuario: meuUser,
    texto: txt,
    expiraEm: exp
  });
}

async function buscarMsgs() {
  if (!salaAtual) return;

  try {
    const msgs = await apiGet(`/mensagens?sala=${encodeURIComponent(salaAtual)}`);

    const c = document.getElementById("container-msgs");
    const topo = c.firstElementChild.outerHTML;

    c.innerHTML = topo;

    msgs.forEach(m => {
      renderMsg(m.usuario, m.texto, m.expiraEm, m.usuario === meuUser);
    });

  } catch (e) {}
}

function renderMsg(user, txt, exp, mine) {
  const c = document.getElementById("container-msgs");
  const div = document.createElement("div");

  div.className = `msg ${mine ? "mine" : "theirs"}`;
  div.dataset.exp = exp;

  div.innerHTML = `
    <div class="msg-head">
      <span>${mine ? user + " (você)" : user}</span>
      <span class="msg-timer">⏱ ...</span>
    </div>
    <div class="msg-bubble">${txt}</div>
  `;

  c.appendChild(div);
  c.scrollTop = c.scrollHeight;

  tickTimers();
}

function tickTimers() {
  const now = Date.now();

  document.querySelectorAll(".msg").forEach(m => {
    const exp = parseInt(m.dataset.exp);
    const left = exp - now;

    if (left <= 0) {
      m.remove();
      return;
    }

    const min = Math.floor(left / 60000);
    const sec = Math.floor((left % 60000) / 1000);
    const t = m.querySelector(".msg-timer");

    t.innerText = min > 0 ? `⏱ ${min}m` : `⏱ ${sec}s`;

    if (min === 0) {
      t.style.color = "#c030a0";
    }
  });
}