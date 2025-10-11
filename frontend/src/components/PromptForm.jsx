import React, { useState } from 'react';


export default function PromptForm({ onSubmit, loading }) {
  const [text, setText] = useState(
    'I want to build a task management app with user authentication and real-time updates for collaborative projects'
  );

  function handleSubmit(e) {
    e.preventDefault();
    onSubmit?.(text);
  }

  return (
    <div className="panel">
      <div className="panel-title">PromptForm</div>
      <form onSubmit={handleSubmit} className="pf-form">
        <textarea
          className="pf-textarea"
          rows={8}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button className="btn-primary" disabled={loading}>
          {loading ? 'Starting…' : 'Initiate Project'}
        </button>
      </form>
    </div>
  );
}