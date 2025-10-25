# Hierra: An Agentic Software Developer with Autonomous Long-Term Memory

<img width="1283" height="571" alt="image" src="https://github.com/user-attachments/assets/f2e37173-02db-485d-b37a-be9104e4ae3b" />
<img width="1226" height="675" alt="image" src="https://github.com/user-attachments/assets/c2c71f33-0ad3-4db4-9aa9-cf954be79905" />


> **An autonomous AI agent that takes a single high-level prompt and generates, executes, and remembers the entire software development lifecycle for a full-stack application.**

## About The Project

Hierra is an experimental AI agent designed to tackle one of the biggest challenges in autonomous code generation: long-term context retention. Traditional LLM interactions are limited by context windows, causing agents to "forget" earlier decisions when building large projects. Hierra solves this by implementing a novel **hierarchical memory system**, allowing it to maintain a coherent understanding of the entire project, from high-level architecture down to specific lines of code.

This project demonstrates a robust human-in-the-loop workflow where the agent proposes actions, and the user confirms or provides natural language feedback for refinement. The agent can create files, write code, and run terminal commands, effectively acting as an autonomous junior developer guided by a human senior.

### Core Features

-   **Autonomous Planning:** Generates a complete, step-by-step project plan for both frontend and backend from a single user prompt.
-   **Hierarchical Long-Term Memory:** Utilizes a 3-level memory system (stored in MongoDB) to efficiently manage context, mimicking how human developers recall information at different levels of detail.
-   **Human-in-the-Loop Interaction:** Proposes each action (e.g., code to be written) for user review. The user can confirm with a simple "proceed" or provide corrective feedback in natural language.
-   **Full-Stack Generation:** Capable of building both a Python-based FastAPI backend and a React frontend within a sandboxed local workspace.
-   **Robust and State-Aware Backend:** Built with FastAPI, it manages the agent's state (current plan, progress, and pending actions) across multiple stateless API calls.

## How It Works

The entire development process is managed through a simple, iterative loop:

1.  **Initiate:** The user provides a high-level description of the application they want to build.
2.  **Plan:** Hierra's backend sends this description to an AI model (GPT-4o) to generate a structured, multi-step implementation plan.
3.  **Propose:** The user types "proceed". The agent takes the first step of the plan, retrieves high-level context from its memory, and decides on a single, precise action (e.g., create a specific file with specific code). This proposed action is displayed to the user.
4.  **Confirm or Refine:**
    -   If the user is satisfied, they type "proceed" or "ok".
    -   If the user wants a change, they provide natural language feedback (e.g., "I don't like that, use a different port").
5.  **Execute & Remember:**
    -   Upon confirmation, the backend executes the proposed action (writing the file or running the command). The result is then summarized by the AI into three levels of detail and saved to the long-term memory in MongoDB.
    -   Upon refinement, the agent takes the feedback and generates a new, corrected proposal.
6.  **Repeat:** The agent advances to the next step, using the growing memory of completed tasks as context for future actions.

### The Hierarchical Memory System

This is the core innovation of Hierra. Instead of feeding the entire project history back to the AI for every step, it uses a tiered approach to conserve tokens and improve efficiency.

-   **Level 3: High-Level Summary**
    A concise, one-sentence summary of what was accomplished (e.g., "Created the main FastAPI server file with a root endpoint."). This is the default context provided for every step.

-   **Level 2: Detailed Summary**
    A more detailed, one-paragraph summary explaining the implementation, its purpose, and key logic (e.g., "Implemented `main.py` using FastAPI, added CORS middleware, and defined a GET route at `/` that returns a 'Hello World' JSON object.").

-   **Level 1: Full Context**
    The raw, complete data of the action, including the exact code written, the filename, and any terminal output. The agent is designed to be able to request this level of detail for a specific past step if it determines the high-level summaries are insufficient.

## Tech Stack

-   **Backend:** 🐍 FastAPI (Python)
-   **Frontend:** ⚛️ React (Vite)
-   **AI Model:** 🧠 OpenAI API (`gpt-4o-2024-08-06`)
-   **Database (Memory):** 🍃 MongoDB Atlas
-   **API Validation:** Pydantic

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

-   **Node.js and npm:** [https://nodejs.org/](https://nodejs.org/)
-   **Python 3.10+ and pip:** [https://www.python.org/](https://www.python.org/)
-   **Git:** [https://git-scm.com/](https://git-scm.com/)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/hierra-app.git
    cd hierra-app
    ```

2.  **Set up the Backend:**
    ```bash
    # Navigate to the backend directory
    cd backend

    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate

    # Install Python dependencies
    pip install -r requirements.txt 
    ```
    *(Note: If `requirements.txt` is not present, run `pip install "fastapi[all]" openai pymongo python-dotenv certifi`)*

3.  **Set up the Frontend:**
    ```bash
    # Navigate to the frontend directory from the root
    cd frontend

    # Install Node.js dependencies
    npm install
    ```

4.  **Configure Environment Variables:**
    -   In the `backend` directory, create a file named `.env`.
    -   Copy the contents of `.env.example` (if it exists) or paste the following into it:
        ```env
        OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
        MONGO_URI="YOUR_MONGODB_ATLAS_CONNECTION_URI_HERE"
        ```
    -   Replace the placeholders with your actual OpenAI API key and your MongoDB Atlas connection string.

## Running the Application

You will need two separate terminals to run both the backend and frontend servers.

#### Terminal 1: Start the Backend

# Navigate to the backend directory
cd backend

# Activate the virtual environment
source venv/bin/activate

# Start the server (use this stable command for the demo)
uvicorn main:app

The backend will be running at http://localhost:8000.

The frontend will open in your browser, typically at http://localhost:5173. You can now start using Hierra!

