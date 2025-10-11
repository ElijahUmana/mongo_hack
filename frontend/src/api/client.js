import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const api = {
  initiateProject: (description) => {
    return client.post('/initiate-project', { description });
  },
  executeNextStep: () => {
    return client.post('/execute-next-step');
  },
  proceedAndSave: () => {
    return client.post('/proceed-and-save');
  },
};