async function carregarSalas() {
  let salasAtivas = [];

  try {
    salasAtivas = await apiGet("/salas");
  } catch (e) {
    salasAtivas = [];
  }

  const lista = document.getElementById("lista-salas");
  lista.innerHTML = "";

  document.getElementById("qtd-salas").innerText = salasAtivas.length;

  salasAtivas.forEach(sala => {
    const div = document.createElement("div");
    div.className = "sala-row";
    div.style.justifyContent = "space-between";

    const spanNome = document.createElement("span");
    spanNome.innerText = sala.nome;
    spanNome.style.flex = "1";

    div.onclick = () => {
      document.querySelectorAll(".sala-row").forEach(el => el.classList.remove("selected"));
      div.classList.add("selected");
      salaSel = sala.nome;
    };

    div.ondblclick = () => entrarNaSala(sala.nome);

    div.appendChild(spanNome);

    if (sala.criador === meuUser) {
      const btnDelete = document.createElement("span");
      btnDelete.innerText = "🗑️";
      btnDelete.title = "Destruir Sala";
      btnDelete.style.cursor = "pointer";
      btnDelete.style.fontSize = "14px";

      btnDelete.onclick = (e) => {
        e.stopPropagation();
        deletarSala(sala.nome);
      };

      div.appendChild(btnDelete);
    }

    lista.appendChild(div);
  });
}

function entrarSalaSelecionada() {
  if (salaSel) {
    entrarNaSala(salaSel);
  } else {
    mostrarNotif("Selecione uma sala primeiro!");
  }
}

async function criarSala() {
  const inp = document.getElementById("input-nova-sala");
  const nome = inp.value.trim();

  if (!nome) return;

  try {
    await apiPost("/salas", {
      nome: nome,
      criador: meuUser
    });
  } catch (e) {}

  inp.value = "";
  entrarNaSala(nome);
}

async function deletarSala(nomeSala) {
  if (!confirm(`ALERTA: Tem certeza que deseja destruir a sala "${nomeSala}" e todas as suas mensagens?`)) {
    return;
  }

  try {
    await apiDelete(`/salas/${encodeURIComponent(nomeSala)}`, {
      usuario: meuUser
    });

    mostrarNotif(`A sala ${nomeSala} foi destruída!`);

    if (salaAtual === nomeSala) {
      voltarLobby();
    } else {
      carregarSalas();
    }

  } catch (err) {
    mostrarNotif(err.erro || "Erro ao deletar sala.");
  }
}