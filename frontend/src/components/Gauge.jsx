import React from 'react';


export default function Gauge({ value = 0 }) {
  const v = Math.max(0, Math.min(1, value));
  return (
    <div className="gauge" style={{'--val': v}}>
      <div className="gauge-inner">{v.toFixed(2)}</div>
    </div>
  );
}