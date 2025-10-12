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
    
    relative_path: Optional[str] = Field(None, description="The path to the file to create, relative to the workspace.")
    content: Optional[str] = Field(None, description="The full content to write to the file.")
    command: Optional[str] = Field(None, description="The shell command to execute.")
    message: Optional[str] = Field(None, description="The final message to the user for this step.")

AgentResponse = Action


class StepSummary(BaseModel):
    """Defines the structure for the hierarchical summary of a completed step."""
    level_3_summary: str = Field(description="A concise, one-sentence summary of what was accomplished in the step.")
    level_2_summary: str = Field(description="A more detailed, one-paragraph summary explaining the implementation, its purpose, and key details.")


# --- Core Agent Functions ---

def generate_plan(project_description: str) -> Plan | None:
    if not client:
        print("OpenAI client not initialized.")
        return None
    
    system_prompt = """
    You are a world-class AI software architect. Your role is to take a user's project description
    and generate a comprehensive, step-by-step implementation plan for a React frontend and a FastAPI backend.
    The plan should prioritize building the backend first, followed by the frontend.
    For the application being built, its backend must ONLY use in-memory Python dictionaries for data storage.
    Your output MUST conform to the 'Plan' JSON schema.
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
        return response.output_parsed
    except Exception as e:
        print(f"An error occurred while generating the plan: {e}")
        return None

def execute_step(current_step: str, context_buffer: list) -> AgentResponse | None:
    if not client:
        print("OpenAI client not initialized.")
        return None

    system_prompt = """
    You are an expert AI software developer executing a plan. Your task is to take the current step from the plan,
    analyze the context of previous steps, and decide on a single, precise action to take using one of your available actions:
    `create_file`, `run_command`, or `final_response`.
    Your output MUST conform to the 'Action' JSON schema.
    """

    formatted_context = "\n".join([f"- Step {c.get('step_id', 'N/A')}: {c.get('level_3_summary', 'N/A')}" for c in context_buffer])
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

def generate_summaries(step_description: str, full_context: dict) -> StepSummary | None:
    if not client:
        print("OpenAI client not initialized.")
        return None

    system_prompt = """
    You are a senior software engineer documenting progress. Take a description of a completed task and its full context
    and generate two levels of summary for our hierarchical memory system.
    - Level 3 Summary: Must be a single, concise sentence.
    - Level 2 Summary: Must be a detailed paragraph.
    Your output MUST conform to the 'StepSummary' JSON schema.
    """

    user_prompt = f"""
    The completed task was: "{step_description}"
    Full context of what was done:
    ---
    {str(full_context)}
    ---
    Please generate the Level 2 and Level 3 summaries.
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

# --- NEW FUNCTION FOR REFINEMENT ---
def refine_action(previous_action: dict, user_feedback: str) -> AgentResponse | None:
    """
    Takes a previously generated action and user feedback, and returns a new, refined action.
    """
    if not client:
        print("OpenAI client not initialized.")
        return None

    system_prompt = """
    You are an expert AI software developer. Your previous attempt at a task resulted in the action below.
    The user has provided feedback. Your job is to generate a new, corrected action that incorporates this feedback.
    The new action should completely replace the old one.
    Your output MUST conform to the 'Action' JSON schema.
    """

    user_prompt = f"""
    This was your previous proposed action:
    ---
    {str(previous_action)}
    ---

    Here is the user's feedback on it:
    ---
    "{user_feedback}"
    ---

    Based on this feedback, generate a new, complete, and corrected action.
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
        print(f"An error occurred during refinement: {e}")
        return None