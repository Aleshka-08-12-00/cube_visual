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

interface CubeFields {
  dimensions: string[];
  measures: string[];
}

const App: React.FC = () => {
  const [mdx, setMdx] = useState('');
  const [result, setResult] = useState<QueryResult | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [fields, setFields] = useState<CubeFields | null>(null);

  const fetchReports = async () => {
    const { data } = await axios.get<Report[]>('/reports');
    setReports(data);
  };

  const fetchFields = async () => {
    const { data } = await axios.get<CubeFields>('/fields');
    setFields(data);
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
    fetchFields();
  }, []);

  return (
    <div>
      <h1>Cube Visual</h1>
      {fields && (
        <div>
          <h2>Available Fields</h2>
          <div style={{ display: 'flex', gap: '2rem' }}>
            <div>
              <h3>Dimensions</h3>
              <ul>
                {fields.dimensions.map(d => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            </div>
            <div>
              <h3>Measures</h3>
              <ul>
                {fields.measures.map(m => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
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
