async function fazerLogin() {
  const usuario = document.getElementById("login-usuario").value.trim();
  const senha = document.getElementById("login-senha").value.trim();

  if (!usuario || !senha) {
    mostrarNotif("Preencha todos os campos!");
    return;
  }

  try {
    const data = await apiPost("/auth/login", {
      usuario: usuario,
      senha: senha
    });

    meuUser = data.usuario;
    document.getElementById("user-tag").innerText = meuUser;

    fecharAuth();

  } catch (e) {
    mostrarNotif("Usuário ou senha incorretos!");
  }
}

async function fazerCadastro() {
  const email = document.getElementById("cad-email").value.trim();
  const usuario = document.getElementById("cad-usuario").value.trim();
  const senha = document.getElementById("cad-senha").value.trim();
  const senha2 = document.getElementById("cad-senha2").value.trim();

  if (!email || !usuario || !senha || !senha2) {
    mostrarNotif("Preencha todos os campos!");
    return;
  }

  if (senha !== senha2) {
    mostrarNotif("As senhas não coincidem!");
    return;
  }

  try {
    await apiPost("/auth/cadastro", {
      email: email,
      usuario: usuario,
      senha: senha
    });

    mostrarNotif("Conta criada! Faça login.");
    trocarAba("login");

  } catch (e) {
    mostrarNotif("Erro ao cadastrar. Tente outro usuário!");
  }
}

function iniciarApp() {
  atualizarRelogio();
  setInterval(atualizarRelogio, 10000);

  document.getElementById("user-tag").innerText = "Aguardando Login...";
  document.getElementById("win-lobby").style.display = "none";
  document.getElementById("win-chat").style.display = "none";

  document.getElementById("auth-overlay").addEventListener("click", function(e) {
    e.stopPropagation();
  });

  setInterval(tickTimers, 1000);
}

iniciarApp();