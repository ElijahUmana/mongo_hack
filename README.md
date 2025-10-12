# Hierra

**An Agentic Web Application for Automated Software Development**

<img width="1283" height="571" alt="image" src="https://github.com/user-attachments/assets/f2e37173-02db-485d-b37a-be9104e4ae3b" />
<img width="1226" height="675" alt="image" src="https://github.com/user-attachments/assets/c2c71f33-0ad3-4db4-9aa9-cf954be79905" />


# Hierra: An Agentic Software Developer with Autonomous Long-Term Memory

**An autonomous AI agent that takes a single high-level prompt and generates, executes, and remembers the entire software development lifecycle for a full-stack application.**

_Built for the [Name of Hackathon] Hackathon._

---

![Hierra Demo GIF](https://your-gif-hosting-link-here.gif)
> *A quick demonstration of Hierra generating a full FastAPI application from a single prompt, executing the plan step-by-step, and writing code to the local filesystem.*

## 🚀 The Problem

Modern Large Language Models (LLMs) are incredibly powerful at generating code snippets. However, when tasked with building an entire application, they suffer from a critical limitation: **a finite context window**. As a project grows, the LLM loses track of the overall architecture, file structures, and past decisions, leading to inconsistent, repetitive, and often broken code. It's like a developer with severe short-term memory loss.

## ✨ Our Solution: Autonomous Hierarchical Memory

Hierra solves the context problem with a novel **Hierarchical Memory System**, inspired by how human developers navigate complex codebases. Instead of naively feeding the entire project history into every prompt, Hierra's agent **autonomously decides when it needs deeper context** and retrieves information with surgical precision. This allows it to maintain long-term coherence and build applications far beyond the capacity of a single context window.

This memory is structured into three levels, which the agent can traverse as needed:

*   **🧠 Level 3 (The Map): A High-Level Summary**
    *   **What it is:** A single, concise sentence describing what was accomplished in a past step.
    *   **Example:** `"Created the main FastAPI application file with a root endpoint."`
    *   **Use Case:** This is the default context. The agent reviews the "map" of all past steps to understand the project's history at a glance, ensuring maximum token efficiency.

*   ** blueprint Level 2 (The Blueprint): A Detailed Summary**
    *   **What it is:** A detailed paragraph explaining the logic, functions, and purpose of the code implemented in a step.
    *   **Example:** `"Implemented `main.py` using FastAPI, which includes a GET route at `/` returning `{'message': 'Hello World'}`."`
    *   **Use Case:** If the agent determines the high-level summary is insufficient for the current task, **it autonomously requests this "blueprint"** for specific past steps to gain a deeper understanding without needing to see the full code.

*   **📄 Level 1 (The Code): The Full Implementation**
    *   **What it is:** The complete, raw data, including the final generated code, filename, and terminal output.
    *   **Example:** `{"action_type": "create_file", "path": "...", "content": "from fastapi import FastAPI..."}`
    *   **Use Case:** The last resort. This is requested by the agent **only when it concludes that the exact implementation details of a previous task are critical** for ensuring perfect integration or resolving a complex dependency.

This intelligent, on-demand context escalation is the core of Hierra. It allows the agent to think and act like a senior developer, focusing on the big picture while knowing exactly when and where to dive into the details.

## 核心 Key Features

*   **Autonomous Plan Generation:** Translates a single natural language prompt into a detailed, step-by-step implementation plan for both frontend and backend.
*   **Intelligent Context Management:** The agent autonomously determines the level of detail required for each task, requesting deeper memory levels only when necessary, which radically improves efficiency and coherence.
*   **Step-by-Step Code Execution:** Executes the plan one action at a time, interacting directly with the local filesystem to create files, write code, and run terminal commands.
*   **Interactive Feedback Loop:** Allows the user to confirm each proposed action with a simple "proceed" or provide natural language feedback (e.g., "I don't like that, use a different port"), which the agent uses to refine its action.
*   **Persistent Hierarchical Memory:** All completed steps are summarized and stored in our three-level memory system on MongoDB Atlas, enabling true long-term project memory.

## 🏗️ Architecture & Tech Stack

Hierra operates on a simple yet powerful agentic loop, orchestrated by a FastAPI backend and a React frontend.

**Flow:**
`[User Prompt]` ➡️ `[Plan Generation]` ➡️ `[Agent Proposes Step 1 Action]` ➡️ `[User Confirms/Refines]` ➡️ `[Agent Executes & Saves to Memory]` ➡️ `[Agent Proposes Step 2 Action]` ➡️ ...

**Technology:**
*   **🤖 Backend:** **FastAPI (Python)** - For the robust, high-performance agent server.
*   **🎨 Frontend:** **React (Vite)** - For a responsive and interactive user interface.
*   **🧠 AI Model:** **OpenAI GPT-4o** - Leveraged for its powerful reasoning and Structured Outputs capabilities.
*   **💾 Memory:** **MongoDB Atlas** - For storing the persistent, cloud-based hierarchical memory.



## 🎥 Demo

[View Demo Video](https://www.loom.com/share/0b017086b082464ba81983cb7f865deb?sid=9f3205c5-1843-4946-98b2-fc8d4652e595)



