import React from 'react';

function Stat({ label, value, accent }) {
  return (
    <div className="stat-card">
      <div className="stat-label">{label}</div>
      <div className={`stat-value${accent ? ' accent' : ''}`}>{value}</div>
    </div>
  );
}

export default function SearchResults({ result, error }) {
  if (error) {
    return (
      <div className="results-box error" style={{ animation: 'fadeInUp 0.3s ease' }}>
        <div className="results-status danger">
          <span className="status-dot danger" />
          ERRO
        </div>
        <p style={{ color: 'var(--danger)', fontFamily: 'var(--font-mono)', fontSize: 14 }}>{error}</p>
      </div>
    );
  }

  if (!result) return null;

  const { found, occurrences, positions, execution_time_ms, text_length, pattern_length, algorithm_label } = result;

  const displayPositions = positions.length > 50
    ? [...positions.slice(0, 50).map(String), `... +${positions.length - 50} mais`]
    : positions.map(String);

  return (
    <div className="results-box" style={{ animation: 'fadeInUp 0.35s ease' }}>
      <div className={`results-status ${found ? 'success' : 'danger'}`}>
        <span className={`status-dot ${found ? 'success' : 'danger'}`} />
        {found ? 'ENCONTRADO' : 'NÃO ENCONTRADO'}
        <span className="algo-badge">{algorithm_label}</span>
      </div>

      <div className="stats-grid">
        <Stat label="Ocorrências" value={occurrences} accent={found} />
        <Stat label="Tempo (ms)" value={execution_time_ms.toFixed(4)} />
        <Stat label="Tamanho N" value={text_length.toLocaleString()} />
        <Stat label="Tamanho M" value={pattern_length} />
      </div>

      {positions.length > 0 && (
        <div className="positions-section">
          <div className="positions-label">POSIÇÕES (índices)</div>
          <div className="positions-list">
            {displayPositions.map((p, i) => (
              <span key={i} className={`position-tag${p.startsWith('...') ? ' more' : ''}`}>{p}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
