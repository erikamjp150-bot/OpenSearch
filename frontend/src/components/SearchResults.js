import React from 'react';

export default function SearchResults({ results = [] }) {
  if (!results.length) {
    return <p>No results yet.</p>;
  }

  return (
    <ul style={{ listStyle: 'none', padding: 0 }}>
      {results.map((result, index) => (
        <li key={`${result.url}-${index}`} style={{ marginBottom: 16 }}>
          <a href={result.url} target="_blank" rel="noreferrer">
            <strong>{result.title || result.url}</strong>
          </a>
          <div>{result.content_snippet}</div>
          <small>{result.domain} • score {result.score}</small>
        </li>
      ))}
    </ul>
  );
}
