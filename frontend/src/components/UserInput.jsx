import React, { useState } from 'react';

export default function UserInput({ onSend, onAccept, disabled, hasCode }) {
  const [text, setText] = useState('proceed');

  function handleSend(e) {
    e.preventDefault();
    if(!text.trim()) return;
    onSend?.(text);
  }

  return (
    <div className="user-panel">
      <div className="panel-title">Controls</div>
      <form onSubmit={handleSend} className="composer">
        <input
          className="composer-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type 'proceed' or give feedback..."
        />
        <button 
          className="btn-primary sm" 
          disabled={disabled} 
          type="submit"
        >
          Send
        </button>
        {hasCode && (
          <button 
            type="button"
            className="btn-accept sm" 
            disabled={disabled} 
            onClick={onAccept}
          >
            Accept
          </button>
        )}
      </form>
    </div>
  );
}