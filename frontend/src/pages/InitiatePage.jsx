import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PromptForm from '../components/PromptForm';
import { api } from '../api/client';

export default function InitiatePage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // This is the function that calls your API
  async function handleSubmit(description) {
    setLoading(true); // Show the loading indicator
    setError('');
    try {
      // 1. Wait for the API to return the complete plan
      const response = await api.initiateProject(description);
      const plan = response.data.plan;

      // 2. ONLY after getting the plan, navigate to the workspace, 
      //    passing the plan securely in the navigation state.
      navigate('/workspace/1', { state: { plan: plan } });

    } catch (err) {
      console.error('Failed to initiate project:', err);
      const errorMsg = err.response?.data?.detail || 'An unknown error occurred while generating the plan.';
      setError(errorMsg);
    } finally {
      setLoading(false); // Hide the loading indicator
    }
  }

  return (
    <div className="grid grid-init">
      <div className="col-full">
        {/* We pass our API-calling function to PromptForm via the onSubmit prop */}
        <PromptForm onSubmit={handleSubmit} loading={loading} />
        {error && <p style={{ color: '#f87171', marginTop: '1rem' }}>Error: {error}</p>}
      </div>
    </div>
  );
}