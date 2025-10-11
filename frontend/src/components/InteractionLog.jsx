import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

// Add logEndRef to the props
export default function InteractionLog({ items = [], logEndRef }) {
  return (
    <div className="panel">
      <div className="panel-title">Interaction Log</div>
      <div className="log-list">
        {items.map((entry, idx) => (
          <div key={idx} className={`log-item ${entry.type}`}>
            {entry.type === 'message' && (
              <div className="bubble">
                <div className="muted">
                  {entry.role === 'assistant' ? 'Hierra Agent' : 'You'}
                </div>
                <div>{entry.text}</div>
              </div>
            )}
            {entry.type === 'code' && (
               <SyntaxHighlighter language={entry.lang || 'bash'} style={atomDark} customStyle={{ margin: 0, borderRadius: '10px' }}>
                {String(entry.text)}
              </SyntaxHighlighter>
            )}
          </div>
        ))}
        {/* Add this empty div at the end for the ref to attach to */}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}