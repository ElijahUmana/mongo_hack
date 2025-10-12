import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import PlanDisplay from '../components/PlanDisplay';
import InteractionLog from '../components/InteractionLog';
import UserInput from '../components/UserInput';
import { api } from '../api/client';

export default function WorkspacePage() {
    const location = useLocation();
    const navigate = useNavigate();
    const [plan, setPlan] = useState(location.state?.plan || null);
    const [currentStepIndex, setCurrentStepIndex] = useState(0);
    const [interactionLog, setInteractionLog] = useState([]);
    const [lastAction, setLastAction] = useState(null); // Tracks a pending action
    const [loading, setLoading] = useState(false);
    const logEndRef = useRef(null);

    useEffect(() => {
        if (plan) {
            setInteractionLog([{ type: 'message', role: 'assistant', text: "Plan generated. Type 'proceed' to execute the first step." }]);
        } else {
            navigate('/');
        }
    }, []);

    useEffect(() => {
        logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [interactionLog]);

    const handleNewAgentAction = (thought, action) => {
        setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: `Thought: ${thought}` }]);
        let nextMessage = "";
        let codeToDisplay = null;

        if (action.action_type === 'create_file') {
            codeToDisplay = action.content;
            nextMessage = `I plan to create/update the file '${action.relative_path}'. Review the code and type 'proceed' to confirm, or provide feedback.`;
        } else if (action.action_type === 'run_command') {
            codeToDisplay = `COMMAND:\n${action.command}`;
            nextMessage = "I plan to run this command. Type 'proceed' to confirm, or provide feedback.";
        } else {
            nextMessage = action.message || "Step complete. Type 'proceed' to confirm.";
        }

        if (codeToDisplay) {
            setInteractionLog(prev => [...prev, { type: 'code', text: codeToDisplay, lang: getLang(action.relative_path) }]);
        }
        setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: nextMessage }]);
        setLastAction(action);
    };

    async function handleUserInput(inputText) {
        setLoading(true);
        setInteractionLog(prev => [...prev, { type: 'message', role: 'user', text: inputText }]);
        
        const confirmationTerms = ['proceed', 'ok', 'yes', 'accept', 'continue', 'go', 'y', 'sounds good'];
        const isConfirmation = confirmationTerms.includes(inputText.toLowerCase().trim());

        try {
            if (!lastAction) { // No action is pending, so we need to generate one for the current step.
                if (isConfirmation) {
                    const response = await api.executeStep();
                    handleNewAgentAction(response.data.thought, response.data.action);
                } else {
                     setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: "Please type 'proceed' to start the action for this step." }]);
                }
            } else { // An action is pending confirmation or refinement.
                if (isConfirmation) { // User confirms the pending action.
                    const response = await api.confirmAndProceed();
                    setLastAction(null); // Clear the pending action
                    setCurrentStepIndex(prev => prev + 1);
                    setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: response.data.message }]);
                } else { // User provides feedback.
                    const response = await api.refineStep(inputText);
                    // The backend returns a new, refined action. We display it.
                    handleNewAgentAction(response.data.thought, response.data.action);
                }
            }
        } catch (err) {
            const errorMsg = err.response?.data?.detail || 'An unexpected error occurred.';
            setInteractionLog(prev => [...prev, { type: 'message', role: 'assistant', text: `Error: ${errorMsg}` }]);
        } finally {
            setLoading(false);
        }
    }
    
    const getLang = (path = '') => {
        const extension = path?.split('.').pop() || '';
        switch (extension) {
            case 'py': return 'python';
            case 'js': case 'jsx': return 'javascript';
            case 'css': return 'css';
            case 'json': return 'json';
            case 'html': return 'html';
            default: return 'bash';
        }
    };

    if (!plan || !plan.backend_plan || !plan.frontend_plan) {
        return <div style={{color: 'white', textAlign: 'center', padding: '2rem'}}>Loading Workspace...</div>;
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
                    <div className="col"><PlanDisplay steps={fullPlanSteps} currentStepIndex={currentStepIndex} /></div>
                    <div className="col"><InteractionLog items={interactionLog} logEndRef={logEndRef} /></div>
                </div>
            </div>
            <UserInput onSend={handleUserInput} disabled={loading} />
        </div>
    );
}