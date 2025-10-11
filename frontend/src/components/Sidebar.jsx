import React from 'react';


const defaultTree = [
  { label: 'L0 Repository' },
  { label: 'L1 Frentend' },
  { label: 'L2 Backend' },
  { label: 'L3 Homepage.tsx', active: true },
  { label: 'L4 λxpt…' },
];

export default function Sidebar({ projects, projectId, setProjectId, loading }) {
  return (
    <aside className="sidebar">
      <div className="brand">Agentic Dev</div>
      <div className="section-title">Project Graph</div>
      <ul className="tree">
        {defaultTree.map((n, i) => (
          <li key={i} className={n.active ? 'active' : ''}>{n.label}</li>
        ))}
      </ul>
      <div className="sidebar-footer">
        <div className="status pass">
          <span className="dot"/> tsc passed
        </div>
        <div className="users">
          <span className="pill">etαnet</span>
          <span className="pill">paskeb</span>
        </div>
        <div className="projects">
          <label>Project</label>
          <select 
            value={projectId || ''} 
            onChange={e => setProjectId(e.target.value)} 
            disabled={loading}
          >
            {projects.map(p => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>
      </div>
    </aside>
  );
}