import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import PlanDisplay from '../components/PlanDisplay';
import InteractionLog from '../components/InteractionLog';
import UserInput from '../components/UserInput';
import { api } from '../api/client';

export default function WorkspacePage() {
  const [plan, setPlan] = useState(null);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [interactionLog, setInteractionLog] = useState([]);
  const [lastAction, setLastAction] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const logEndRef = useRef(null); // Ref to auto-scroll the log

  // Effect for initial plan loading
  useEffect(() => {
    const receivedPlan = location.state?.plan;
    if (receivedPlan) {
      setPlan(receivedPlan);
      setInteractionLog([{ type: 'message', role: 'assistant', text: "Plan generated successfully. Type 'proceed' to execute the first step." }]);
    } else {
      // If no plan is found (e.g., user refreshed the page), go back to the start
      navigate('/');
    }
  }, []); // Run only once on mount

  // Effect for auto-scrolling the interaction log
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [interactionLog]);


  async function handleExecuteStep(inputText) {
    setLoading(true);
    setInteractionLog(prev => [...prev, { type: 'message', role: 'user', text: inputText }]);

    if (inputText.toLowerCase().trim() !== 'proceed') {
        setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: "For this demo, only 'proceed' is supported to execute the next step." }]);
        setLoading(false);
        return;
    }

    try {
      const response = await api.executeNextStep();
      const { thought, action, action_result } = response.data;
      
      setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: `Thought: ${thought}` }]);
      
      let nextMessage = "Action completed. Please review and click 'Accept' to save and continue.";
      let codeToDisplay = null;

      if (action.action_type === 'create_file') {
        codeToDisplay = action.content;
        nextMessage = `I plan to create/update the file '${action.relative_path}'. Review the code and click 'Accept'.`;
      } else if (action.action_type === 'run_command') {
        codeToDisplay = `COMMAND:\n${action.command}\n\nSTDOUT:\n${action_result.stdout}\n\nSTDERR:\n${action_result.stderr}`;
        nextMessage = "Command executed. Review the output and click 'Accept'.";
      } else {
        nextMessage = action.message || "Step complete. Click 'Accept' to continue.";
      }

      if(codeToDisplay) {
         setInteractionLog(prev => [...prev, { type: 'code', text: codeToDisplay, lang: getLang(action.relative_path) }]);
      }
      setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: nextMessage }]);
      setLastAction(action);

    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'An error occurred during execution.';
      setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: `Error: ${errorMsg}` }]);
    } finally {
      setLoading(false);
    }
  }

  async function handleAcceptAndProceed() {
    setLoading(true);
    setInteractionLog(prev => [...prev, { type: 'message', role: 'user', text: 'Accept' }]);
    
    try {
        const response = await api.proceedAndSave();
        setLastAction(null);
        setCurrentStepIndex(prev => prev + 1);
        setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: response.data.message }]);
    } catch (err) {
        const errorMsg = err.response?.data?.detail || 'An error occurred while saving progress.';
        setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: `Error: ${errorMsg}` }]);
    } finally {
        setLoading(false);
    }
  }

  const getLang = (path = '') => {
    const extension = path.split('.').pop();
    switch (extension) {
      case 'py': return 'python';
      case 'js':
      case 'jsx': return 'javascript';
      case 'css': return 'css';
      case 'json': return 'json';
      case 'html': return 'html';
      default: return 'bash';
    }
  }

  // --- CRITICAL FIX IS HERE ---
  // This robustly checks if the plan is fully loaded before trying to render.
  if (!plan || !plan.backend_plan || !plan.frontend_plan) {
    return (
      <div style={{color: 'white', textAlign: 'center', padding: '2rem'}}>
        Loading and preparing workspace...
      </div>
    );
  }

  const fullPlanSteps = [...plan.backend_plan, ...plan.frontend_plan];

  return (
    <div className="workspace-layout">
      <div className="workspace-header">
        <button className="btn-back" onClick={() => navigate('/')}>← Back to Initiate</button>
        <span className="project-id">Hierra Workspace</span>
      </div>
      
      <div className="workspace-content">
        <div className="grid grid-workspace">
          <div className="col">
            <PlanDisplay steps={fullPlanSteps} currentStepIndex={currentStepIndex} />
          </div>
          <div className="col">
            <InteractionLog items={interactionLog} logEndRef={logEndRef} />
          </div>
        </div>
      </div>

      <UserInput onSend={handleExecuteStep} onAccept={handleAcceptAndProceed} disabled={loading} hasCode={!!lastAction} />
    </div>
  );
}