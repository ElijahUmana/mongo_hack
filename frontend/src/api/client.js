import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const api = {
  initiateProject: (description) => {
    return client.post('/initiate-project', { description });
  },
  
  // CORRECTED: Was 'executeNextStep'
  executeStep: () => {
    return client.post('/execute-step');
  },
  
  // CORRECTED: Was 'proceedAndSave'
  confirmAndProceed: () => {
    return client.post('/confirm-and-proceed');
  },
  
  // NEW: For handling feedback
  refineStep: (feedback) => {
    return client.post('/refine-step', { feedback });
  },
};