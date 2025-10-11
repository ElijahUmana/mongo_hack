import React, { useState } from 'react';
import { syntaxColor } from '../utils/syntax';


export default function EditorPane({ breadcrumbs, codeLines, loading }) {
  const [tabs] = useState(['Homepage.tsx','apits','Diff']);
  const [activeTab, setActiveTab] = useState('Homepage.tsx');

  return (
    <section className="editor-col">
      <div className="tabs">
        {tabs.map((t) => (
          <button 
            key={t} 
            className={`tab ${activeTab === t ? 'active' : ''}`} 
            onClick={() => setActiveTab(t)}
          >
            {t}
          </button>
        ))}
        <div className="tab-tools">•••</div>
      </div>

      <div className="crumbs">
        • {breadcrumbs?.length ? breadcrumbs.join(' • ') : 'Context'}
      </div>

      <div className="code-panel">
        <div className="gutter">
          {(codeLines || Array.from({length:8})).map((_, i) => (
            <div key={i}>{i+1}</div>
          ))}
        </div>
        <pre className="code">
          {loading ? (
            Array.from({length:8}).map((_,i) => (
              <div key={i} className="line skeleton" />
            ))
          ) : (
            (codeLines || []).map((line, i) => (
              <div 
                key={i} 
                className="line" 
                dangerouslySetInnerHTML={syntaxColor(line)} 
              />
            ))
          )}
        </pre>
      </div>
    </section>
  );
}