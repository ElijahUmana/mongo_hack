import React from 'react';

export default function PlanDisplay({ steps = [], currentStepIndex = 0 }) {
  return (
    <div className="panel">
      <div className="panel-title">Implementation Plan</div>
      <ol className="plan-list">
        {steps.map((step, i) => (
          <li 
            key={i}
            className={`plan-step ${i === currentStepIndex ? 'active' : ''} ${i < currentStepIndex ? 'completed' : ''}`}
          >
            <span className="idx">{i + 1}</span>
            {step}
          </li>
        ))}
      </ol>
    </div>
  );
}