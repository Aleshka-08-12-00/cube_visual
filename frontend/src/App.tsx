import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Report {
  name: string;
  mdx: string;
}

interface QueryResult {
  columns: string[];
  data: Record<string, any>[];
}

const App: React.FC = () => {
  const [mdx, setMdx] = useState('');
  const [result, setResult] = useState<QueryResult | null>(null);
  const [reports, setReports] = useState<Report[]>([]);

  const fetchReports = async () => {
    const { data } = await axios.get<Report[]>('/reports');
    setReports(data);
  };

  const runQuery = async () => {
    const { data } = await axios.post<QueryResult>('/query', { mdx });
    setResult(data);
    fetchReports();
  };

  const saveReport = async () => {
    await axios.post('/reports', { name: `Report ${Date.now()}`, mdx });
    fetchReports();
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <div>
      <h1>Cube Visual</h1>
      <textarea value={mdx} onChange={e => setMdx(e.target.value)} rows={4} cols={80} />
      <div>
        <button onClick={runQuery}>Run Query</button>
        <button onClick={saveReport}>Save Report</button>
      </div>
      {result && (
        <table border={1} cellPadding={4} style={{ marginTop: '1rem' }}>
          <thead>
            <tr>
              {result.columns.map(col => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.data.map((row, i) => (
              <tr key={i}>
                {result.columns.map(col => (
                  <td key={col}>{row[col]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <h2>Saved Reports</h2>
      <ul>
        {reports.map((r, i) => (
          <li key={i}>{r.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
