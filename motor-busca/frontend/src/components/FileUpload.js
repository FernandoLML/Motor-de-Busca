import React, { useRef, useState } from 'react';

export default function FileUpload({ onFile }) {
  const inputRef = useRef();
  const [dragging, setDragging] = useState(false);
  const [fileName, setFileName] = useState(null);

  function handle(file) {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.txt')) {
      alert('Apenas arquivos .txt são suportados.');
      return;
    }
    setFileName(file.name);
    onFile(file);
  }

  function onDrop(e) {
    e.preventDefault();
    setDragging(false);
    handle(e.dataTransfer.files[0]);
  }

  return (
    <div
      className={`file-drop${dragging ? ' dragging' : ''}${fileName ? ' has-file' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      onClick={() => inputRef.current.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".txt"
        style={{ display: 'none' }}
        onChange={(e) => handle(e.target.files[0])}
      />
      <div className="file-drop-icon">{fileName ? '📄' : '📁'}</div>
      <div className="file-drop-text">
        {fileName
          ? <><strong>{fileName}</strong><span>Clique para trocar</span></>
          : <><strong>Arraste um arquivo .txt</strong><span>ou clique para selecionar</span></>
        }
      </div>
    </div>
  );
}
