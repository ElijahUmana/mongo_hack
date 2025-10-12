# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import agent_core
import file_handler
import memory_manager

# --- Pydantic Models for API Requests ---
class ProjectInitRequest(BaseModel):
    description: str

class RefineRequest(BaseModel):
    feedback: str

# --- In-Memory State Management ---
class AppState:
    def __init__(self):
        self.plan: agent_core.Plan | None = None
        self.current_step_index: int = 0
        self.full_plan_sequence: list = []
        self.last_action: dict = {} # Stores the most recent PROPOSED action

    def set_plan(self, plan: agent_core.Plan):
        self.plan = plan
        self.full_plan_sequence = plan.backend_plan + plan.frontend_plan
        self.current_step_index = 0
        self.last_action = {}

    def get_current_step(self):
        if self.plan and self.current_step_index < len(self.full_plan_sequence):
            return {"step_index": self.current_step_index, "description": self.full_plan_sequence[self.current_step_index]}
        return None
    
    def advance_to_next_step(self):
        self.current_step_index += 1

# --- FastAPI App and State Initialization ---
app_state = AppState()
app = FastAPI()

origins = ["http://localhost", "http://localhost:3000", "http://localhost:5173"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "Hierra Backend is running!"}

@app.post("/initiate-project")
def initiate_project(request: ProjectInitRequest):
    plan = agent_core.generate_plan(request.description)
    if not plan:
        raise HTTPException(status_code=500, detail="Failed to generate plan.")
    app_state.set_plan(plan)
    return {"plan": plan.dict()}

@app.post("/execute-step")
def execute_step():
    """
    Generates the action for the current step. Does NOT execute it yet.
    """
    current_step_info = app_state.get_current_step()
    if not current_step_info:
        return {"status": "complete", "message": "Plan finished."}
    
    context_buffer = memory_manager.get_context_buffer()
    agent_action = agent_core.execute_step(current_step_info['description'], context_buffer)
    
    if not agent_action:
        raise HTTPException(status_code=500, detail="Agent failed to decide on an action.")
    
    # Save the PROPOSED action to state, so it can be confirmed or refined
    app_state.last_action = agent_action.dict() 
    return {"thought": agent_action.thought, "action": agent_action.dict()}

@app.post("/confirm-and-proceed")
def confirm_and_proceed():
    """
    Executes the last proposed action, saves it to memory, and advances the plan.
    """
    current_step_info = app_state.get_current_step()
    if not current_step_info:
        raise HTTPException(status_code=400, detail="No active plan or step to proceed from.")

    action_to_perform = app_state.last_action
    if not action_to_perform:
        raise HTTPException(status_code=400, detail="No action has been generated to proceed with.")

    action_type = action_to_perform.get("action_type")
    
    # 1. Execute the saved action
    if action_type == "create_file":
        result = file_handler.create_or_update_file(action_to_perform.get("relative_path"), action_to_perform.get("content"))
    elif action_type == "run_command":
        result = file_handler.run_command(action_to_perform.get("command"))
    else: # final_response
        result = {"status": "success"}

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=f"Action execution failed: {result.get('message')}")

    # 2. Generate and save summaries to memory
    summaries = agent_core.generate_summaries(current_step_info['description'], action_to_perform)
    if summaries:
        memory_manager.save_step_to_memory(
            step_id=current_step_info['step_index'],
            plan_description=current_step_info['description'],
            level_3_summary=summaries.level_3_summary,
            level_2_summary=summaries.level_2_summary,
            level_1_full_context=action_to_perform
        )
    
    # 3. Advance to the next step
    app_state.advance_to_next_step()
    app_state.last_action = {} # Clear the action now that it's done
    
    next_step = app_state.get_current_step()
    
    if not next_step:
        return {"status": "complete", "message": "Plan finished! All steps executed and saved."}
    
    return {"status": "success", "message": f"Step saved. Now at step {next_step['step_index'] + 1}: {next_step['description']}"}

@app.post("/refine-step")
def refine_step(request: RefineRequest):
    """
    Takes user feedback and the last action, and generates a new, refined action.
    """
    if not app_state.last_action:
        raise HTTPException(status_code=400, detail="No previous action to refine.")

    refined_action = agent_core.refine_action(app_state.last_action, request.feedback)
    if not refined_action:
        raise HTTPException(status_code=500, detail="Agent failed to refine the action.")

    # Overwrite the last action with the new, refined one
    app_state.last_action = refined_action.dict() 
    return {"thought": refined_action.thought, "action": refined_action.dict()}