import React, { useEffect, useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}/dashboard/flags`)
      .then((response) => response.json())
      .then((data) => setItems(data))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>OpenSearch HITL Dashboard</h1>
      <p>Review flagged content before it is promoted into the search index.</p>
      {loading ? <p>Loading review queue…</p> : null}
      <ul>
        {items.map((item) => (
          <li key={item.id} style={{ marginBottom: 16 }}>
            <strong>{item.title || item.url}</strong>
            <div>{item.url}</div>
            <div>{item.content}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}
