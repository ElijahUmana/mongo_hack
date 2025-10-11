import React, { useState } from 'react';
import { api } from '../api/client';


export default function ChatBox({ projectId, symbol, onPlanRefresh }) {
  const [messages, setMessages] = useState([
    {role:'assistant', text:'Tell me what to change. I can plan a patch and apply when you confirm.'}
  ]);
  const [input, setInput] = useState('Add GET request to Homepage');
  const [quick, setQuick] = useState(['use effect','fetch client','tests']);
  const [busy, setBusy] = useState(false);

  async function send() {
    if(!input.trim()) return;
    const user = {role:'user', text:input};
    setMessages(m => [...m, user]);
    setInput('');
    setBusy(true);
    try {
      const res = await api.postChat(projectId, {message:user.text, symbol});
      setMessages(m => [...m, {role:'assistant', text:res.assistant.text}]);
      if(res.assistant.actions) setQuick(res.assistant.actions);
      onPlanRefresh && onPlanRefresh();
    } finally { 
      setBusy(false); 
    }
  }

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>{m.text}</div>
        ))}
        {busy && <div className="msg assistant">Thinking…</div>}
      </div>
      <div className="quick">
        {quick.map((a, i) => (
          <button 
            key={i} 
            className="chip" 
            onClick={() => setInput(prev => prev ? prev + ` + ${a}` : a)}
          >
            {a}
          </button>
        ))}
      </div>
      <div className="composer">
        <input 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          placeholder="Add GET request to Homepage" 
        />
        <button className="btn" onClick={send}>Send</button>
      </div>
    </div>
  );
}