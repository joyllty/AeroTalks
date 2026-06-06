async function apiGet(endpoint) {
  const response = await fetch(`${API}${endpoint}`);

  if (!response.ok) {
    throw new Error("Erro na requisição GET");
  }

  return await response.json();
}

async function apiPost(endpoint, data) {
  const response = await fetch(`${API}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if (!response.ok) {
    throw result;
  }

  return result;
}

async function apiDelete(endpoint, data) {
  const response = await fetch(`${API}${endpoint}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if (!response.ok) {
    throw result;
  }

  return result;
}