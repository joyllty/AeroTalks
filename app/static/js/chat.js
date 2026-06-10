// --- SISTEMA DE PALETA DE CORES PARA USUÁRIOS ---
function obterCorDoUsuario(nome) {
  // Cores selecionadas para combinar com a estética AeroTalks OS (tons escuros/pastéis para dar contraste)
  const paleta = [
  '#bf40fa', // Roxo Neon original
  '#4c5dd7', // Azul Cyber original
  '#4400ff', // Roxo Escuro do Grid original
  '#9b86c8', // Lavanda Retrô original
  '#ff7eb3', // Rosa Chiclete original
  '#e066ff', // Lilás Brilhante
  '#3343a2', // Azul Noturno
  '#7053a0', // Roxo Opaco
  '#ff4fa8', // Hot Pink
  '#8a2be2'  // Violeta Intenso
  ];

  // Algoritmo simples de hash para transformar o nome em um número único
  let hash = 0;
  for (let i = 0; i < nome.length; i++) {
    hash = nome.charCodeAt(i) + ((hash << 5) - hash);
  }

  // Garante que o número seja positivo e escolhe um índice da paleta
  const index = Math.abs(hash) % paleta.length;
  return paleta[index];
}
// ------------------------------------------------

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

  // Só aplica a paleta dinâmica se NÃO for você. Se for você, deixa o CSS padrão agir.
  const estiloNome = mine ? "" : `style="color: ${obterCorDoUsuario(user)}; font-weight: bold;"`;

  div.innerHTML = `
    <div class="msg-head">
      <span ${estiloNome}>${mine ? user + " (você)" : user}</span>
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