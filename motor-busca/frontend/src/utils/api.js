const BASE = process.env.REACT_APP_API_URL || '/api';

export async function fetchAlgorithms() {
  const res = await fetch(`${BASE}/algorithms`);
  if (!res.ok) throw new Error('Falha ao carregar algoritmos');
  return res.json();
}

export async function runSearch({ file, pattern, algorithm }) {
  const form = new FormData();
  form.append('file', file);
  form.append('pattern', pattern);
  form.append('algorithm', algorithm);

  const res = await fetch(`${BASE}/search`, {
    method: 'POST',
    body: form,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Erro desconhecido' }));
    throw new Error(err.detail || 'Erro na busca');
  }

  return res.json();
}
