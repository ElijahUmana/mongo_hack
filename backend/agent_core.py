# agent_core.py

import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables
load_dotenv()

# --- Initialize OpenAI Client ---
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

# --- Pydantic Schemas for Structured Outputs ---

class Plan(BaseModel):
    """Defines the structure for the agent's implementation plan."""
    thought: str = Field(description="A brief thought process on how the plan was generated.")
    frontend_plan: List[str] = Field(description="A detailed, step-by-step plan for the React frontend.")
    backend_plan: List[str] = Field(description="A detailed, step-by-step plan for the FastAPI backend.")

# --- Pydantic Schemas for the Execution Step (REVISED) ---
class Action(BaseModel):
    """
    Defines a single, explicit action the agent can take.
    Only the parameters relevant to the action_type should be populated.
    """
    action_type: str = Field(
        description="The type of action to take.",
        enum=["create_file", "run_command", "final_response"]
    )
    thought: str = Field(description="A brief thought process explaining the chosen action based on the context and current step.")
    
    # Parameters for 'create_file'
    relative_path: Optional[str] = Field(None, description="The path to the file to create, relative to the workspace.")
    content: Optional[str] = Field(None, description="The full content to write to the file.")
    
    # Parameter for 'run_command'
    command: Optional[str] = Field(None, description="The shell command to execute.")
    
    # Parameter for 'final_response'
    message: Optional[str] = Field(None, description="The final message to the user for this step.")

# Note: The AgentResponse is now simplified, as 'thought' is part of the Action.
# We will keep the original name for consistency in the function call.
AgentResponse = Action


# --- Core Agent Functions ---

def generate_plan(project_description: str) -> Plan | None:
    """
    Generates a structured, step-by-step implementation plan for a project.
    """
    if not client:
        print("OpenAI client not initialized.")
        return None
    
    system_prompt = """
    You are a world-class AI software architect. Your role is to take a user's project description
    and generate a comprehensive, step-by-step implementation plan for a React frontend and a FastAPI backend.

    IMPORTANT CONSTRAINTS FOR THIS HACKATHON:
    1. The generated plan must be atomic and granular, starting from creating files.
    2. For the application being built (the user's app), its backend must NOT use an external database like MongoDB. It should only use in-memory Python dictionaries for data storage.
    3. The plan should prioritize building the backend first, followed by the frontend.
    4. Your output MUST conform to the 'Plan' JSON schema.
    """
    
    user_prompt = f"Here is the project I want to build: '{project_description}'"
    
    try:
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text_format=Plan,
        )
        
        plan_object = response.output_parsed
        return plan_object

    except Exception as e:
        print(f"An error occurred while generating the plan: {e}")
        return None

def execute_step(current_step: str, context_buffer: list) -> AgentResponse | None:
    """
    Executes a single step of the plan based on the available context.
    """
    if not client:
        print("OpenAI client not initialized.")
        return None

    system_prompt = """
    You are an expert AI software developer executing a plan. Your task is to take the current step from the plan,
    analyze the context of previous steps, and decide on a single, precise action to take.

    You have access to three actions:
    1. `create_file(relative_path: str, content: str)`: Creates or overwrites a file in the workspace.
    2. `run_command(command: str)`: Executes a shell command in the workspace terminal (e.g., 'npm install').
    3. `final_response(message: str)`: Use this action if the step is complete or is just a concluding thought.
    
    Based on the current step and context, you must decide on ONE action.
    - If the step is about creating or modifying code, use `create_file`.
    - If the step involves installing dependencies or running a process, use `run_command`.
    - If the step is a meta-instruction, a comment, or the task is finished, use `final_response`.

    Your output MUST conform to the 'Action' JSON schema, containing your thought process and the single action to perform.
    """

    formatted_context = "\n".join([f"- Step {c.get('step_id', 'N/A')} ({c.get('plan_description', 'N/A')}): {c.get('level_3_summary', 'N/A')}" for c in context_buffer])
    if not formatted_context:
        formatted_context = "No previous steps have been completed."

    user_prompt = f"""
    CONTEXT OF PREVIOUSLY COMPLETED STEPS:
    {formatted_context}

    CURRENT STEP TO EXECUTE:
    "{current_step}"

    Based on the context and the current step, what is the single next action you should take?
    """

    try:
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text_format=AgentResponse,
        )
        return response.output_parsed
    except Exception as e:
        print(f"An error occurred during step execution: {e}")
        return None


# --- Append this code to the end of agent_core.py ---

# Pydantic Schema for Summarization
class StepSummary(BaseModel):
    """Defines the structure for the hierarchical summary of a completed step."""
    level_3_summary: str = Field(description="A concise, one-sentence summary of what was accomplished in the step.")
    level_2_summary: str = Field(description="A more detailed, one-paragraph summary explaining the implementation, its purpose, and key details.")

def generate_summaries(step_description: str, full_context: dict) -> StepSummary | None:
    """
    Generates Level 2 and Level 3 summaries for a completed step.
    """
    if not client:
        print("OpenAI client not initialized.")
        return None

    system_prompt = """
    You are a senior software engineer responsible for documenting progress. Your task is to take a description
    of a completed programming task and its full implementation context (e.g., the code written, the command run)
    and generate two levels of summary for our hierarchical memory system.

    - Level 3 Summary: Must be a single, concise sentence.
    - Level 2 Summary: Must be a detailed paragraph, explaining the 'what' and 'why' of the implementation.

    Your output MUST conform to the 'StepSummary' JSON schema.
    """

    user_prompt = f"""
    The completed task was: "{step_description}"

    Here is the full context of what was done (e.g., file content, command output):
    ---
    {str(full_context)}
    ---

    Please generate the Level 2 and Level 3 summaries for this task.
    """

    try:
        response = client.responses.parse(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text_format=StepSummary,
        )
        return response.output_parsed
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None

# --- Test Block ---
if __name__ == "__main__":
    print("Testing agent core functions...")
    test_project_description = "A simple to-do list app. Users can add tasks and view a list of all tasks."
    generated_plan = generate_plan(test_project_description)
    
    if generated_plan:
        print("\n--- Generated Plan ---")
        print("\nThought:", generated_plan.thought)
        print("\nBackend Plan:")
        for i, step in enumerate(generated_plan.backend_plan, 1):
            print(f"  {i}. {step}")
        
        print("\nFrontend Plan:")
        for i, step in enumerate(generated_plan.frontend_plan, 1):
            print(f"  {i}. {step}")
    else:
        print("\nFailed to generate a plan.")