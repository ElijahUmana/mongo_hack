import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import InitiatePage from './pages/InitiatePage';
import WorkspacePage from './pages/WorkspacePage';
import './styles.css';

export default function App() {
  return (
    <Router>
      <div className="screen">
        <div className="screen-header">
          <div className="brand">Hierra Agent</div>
        </div>
        
        <Routes>
          <Route path="/" element={<InitiatePage />} />
          <Route path="/workspace/:projectId" element={<WorkspacePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}