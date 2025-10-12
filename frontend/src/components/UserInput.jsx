import React, { useState } from 'react';

export default function UserInput({ onSend, disabled }) {
  const [text, setText] = useState('proceed');

  function handleSend(e) {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend?.(text);
    // We clear the input only if the user typed something other than a confirmation
    if (text.toLowerCase().trim() !== 'proceed') {
      setText('');
    }
  }

  return (
    <div className="user-panel">
      <div className="panel-title">Controls</div>
      <form onSubmit={handleSend} className="composer">
        <input
          className="composer-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type 'proceed' to confirm, or provide feedback..."
          disabled={disabled}
        />
        <button 
          className="btn-primary sm" 
          disabled={disabled} 
          type="submit"
        >
          Send
        </button>
      </form>
    </div>
  );
}