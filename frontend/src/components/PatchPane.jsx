import React from 'react';
import Gauge from './Gauge';


export default function PatchPane({ plan, onPlan, onApply, lintStatus }) {
  return (
    <aside className="patch-col">
      <div className="panel-title">Plan &amp; Patch</div>

      <div className="meter">
        <Gauge value={plan.score} />
        <div className="meter-side">
          <div className="meta">Compatibility</div>
          <div className="tiny">{plan.tokens}</div>
        </div>
      </div>

      <div className="kv">
        <span>Context tokens</span>
        <b>{plan.tokens}</b>
      </div>
      <div className="kv">
        <span>Neighbors considered</span>
        <b>{plan.neighbors}</b>
      </div>

      <div className="subhead">Proposed edits</div>
      <ul className="edits">
        {plan.edits.map((e, i) => (
          <li key={i}>
            <span>{e.level}</span> {e.text}
          </li>
        ))}
      </ul>

      <div className="subhead">Diff preview</div>
      <div className="actions">
        <button className="btn" onClick={onPlan}>Plan</button>
        <button className="btn" onClick={onApply}>Apply</button>
        <button className="btn" onClick={() => alert('Revert simulated')}>Revert</button>
      </div>

      <div className={`lint ${lintStatus === 'passed' ? 'pass' : 'fail'}`}>
        <span className="dot"/> Eslint {lintStatus}
      </div>
    </aside>
  );
}