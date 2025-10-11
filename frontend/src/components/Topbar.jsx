import React from 'react';


export default function Topbar({ value, onChange, tokens }) {
  return (
    <div className="topbar">
      <input 
        className="search" 
        value={value} 
        onChange={e => onChange(e.target.value)} 
        placeholder="Resolve symbol or file .." 
      />
      <div className="branch">main</div>
      <div className="tokens">{tokens.used}/{tokens.max}</div>
    </div>
  );
}