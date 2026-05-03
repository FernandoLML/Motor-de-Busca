import React, { useState, useEffect } from 'react';
import FileUpload from './components/FileUpload';
import SearchResults from './components/SearchResults';
import { fetchAlgorithms, runSearch } from './utils/api';
import './App.css';

export default function App() {
  const [algorithms, setAlgorithms] = useState([]);
  const [file, setFile] = useState(null);
  const [pattern, setPattern] = useState('');
  const [algorithm, setAlgorithm] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchAlgorithms()
      .then((list) => {
        setAlgorithms(list);
        if (list.length > 0) setAlgorithm(list[0].id);
      })
      .catch(() => setError('Não foi possível conectar ao servidor.'));
  }, []);

  async function handleSearch(e) {
    e.preventDefault();
    if (!file) return setError('Selecione um arquivo .txt.');
    if (!pattern.trim()) return setError('Digite um termo para pesquisar.');
    setError(null);
    setResult(null);
    setLoading(true);

    try {
      const data = await runSearch({ file, pattern, algorithm });
      setResult(data);
      setHistory((h) => [{ ...data, pattern, timestamp: Date.now() }, ...h].slice(0, 10));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-bracket">[</span>
            <span className="logo-text">MOTOR</span>
            <span className="logo-dot">·</span>
            <span className="logo-text dim">BUSCA</span>
            <span className="logo-bracket">]</span>
          </div>
          <p className="header-sub">Substring Search Engine · Algoritmos Avançados</p>
        </div>
        <a
          href="http://localhost:3000"
          target="_blank"
          rel="noreferrer"
          className="dashboard-link"
        >
          ▣ Dashboard Grafana
        </a>
      </header>

      <main className="app-main">
        <div className="layout">
          {/* ── Left Panel: Form ── */}
          <section className="panel form-panel">
            <div className="panel-title">
              <span className="step-num">01</span> Documento
            </div>
            <FileUpload onFile={setFile} />

            <div className="panel-title" style={{ marginTop: 32 }}>
              <span className="step-num">02</span> Algoritmo
            </div>
            <select
              className="select-algo"
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
            >
              {algorithms.map((a) => (
                <option key={a.id} value={a.id}>{a.label}</option>
              ))}
            </select>

            <div className="panel-title" style={{ marginTop: 32 }}>
              <span className="step-num">03</span> Termo / Trecho
            </div>
            <input
              className="search-input"
              type="text"
              placeholder="Digite o que deseja encontrar..."
              value={pattern}
              onChange={(e) => setPattern(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch(e)}
            />

            <button
              className={`search-btn${loading ? ' loading' : ''}`}
              onClick={handleSearch}
              disabled={loading}
            >
              {loading ? (
                <><span className="spinner" /> Buscando...</>
              ) : (
                <><span className="btn-icon">⌕</span> Pesquisar</>
              )}
            </button>
          </section>

          {/* ── Right Panel: Results ── */}
          <section className="panel results-panel">
            <div className="panel-title">
              <span className="step-num">04</span> Resultado
            </div>

            {!result && !error && !loading && (
              <div className="empty-state">
                <div className="empty-icon">◈</div>
                <p>Execute uma busca para ver os resultados aqui.</p>
              </div>
            )}

            {loading && (
              <div className="searching-anim">
                <div className="scan-line" />
                <p>Executando <strong>{algorithms.find(a => a.id === algorithm)?.label}</strong>...</p>
              </div>
            )}

            <SearchResults result={result} error={error} />

            {/* History */}
            {history.length > 0 && (
              <div className="history">
                <div className="history-title">HISTÓRICO</div>
                {history.map((h, i) => (
                  <div key={i} className="history-item">
                    <span className={`history-dot ${h.found ? 'success' : 'danger'}`} />
                    <span className="history-pattern">"{h.pattern}"</span>
                    <span className="history-algo">{h.algorithm}</span>
                    <span className="history-time">{h.execution_time_ms.toFixed(2)}ms</span>
                    <span className="history-occ">{h.occurrences}×</span>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        {/* ── Algorithm Info Cards ── */}
        <section className="algo-cards">
          {[
            { id: 'naive', label: 'Força Bruta', complexity: 'O(N·M)', desc: 'Compara caractere a caractere em todas as posições possíveis.' },
            { id: 'rabin_karp', label: 'Rabin-Karp', complexity: 'O(N+M)', desc: 'Hash rolante para comparação eficiente de janelas de texto.' },
            { id: 'kmp', label: 'KMP', complexity: 'O(N+M)', desc: 'Tabela de falhas evita retroceder o ponteiro no texto.' },
            { id: 'boyer_moore', label: 'Boyer-Moore', complexity: 'O(N/M)', desc: 'Busca da direita para a esquerda com heurística bad char + good suffix.' },
          ].map((a) => (
            <div
              key={a.id}
              className={`algo-card${algorithm === a.id ? ' active' : ''}`}
              onClick={() => setAlgorithm(a.id)}
            >
              <div className="algo-card-label">{a.label}</div>
              <div className="algo-card-complexity">{a.complexity}</div>
              <div className="algo-card-desc">{a.desc}</div>
            </div>
          ))}
        </section>
      </main>

      <footer className="app-footer">
        Motor de Busca · Algoritmos Avançados · OpenTelemetry + Grafana
      </footer>
    </div>
  );
}
