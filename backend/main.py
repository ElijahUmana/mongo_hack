# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our agent modules
import agent_core
import file_handler
import memory_manager

# --- Pydantic Models for API Requests ---
class ProjectInitRequest(BaseModel):
    description: str

# --- In-Memory State Management ---
class AppState:
    def __init__(self):
        self.plan: agent_core.Plan | None = None
        self.current_step_index: int = 0
        self.total_steps: int = 0
        self.full_plan_sequence: list = []
        self.last_action_context: dict = {} # NEW: To store context for saving

    def set_plan(self, plan: agent_core.Plan):
        self.plan = plan
        self.full_plan_sequence = plan.backend_plan + plan.frontend_plan
        self.total_steps = len(self.full_plan_sequence)
        self.current_step_index = 0
        self.last_action_context = {}

    def get_current_step(self):
        if self.plan and self.current_step_index < self.total_steps:
            return {
                "step_index": self.current_step_index,
                "description": self.full_plan_sequence[self.current_step_index]
            }
        return None
    
    def advance_to_next_step(self):
        if self.current_step_index < self.total_steps:
            self.current_step_index += 1
            return True
        return False

app_state = AppState()

# --- FastAPI App Initialization ---
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000", # For standard React dev server
    "http://localhost:5173", # For Vite dev server
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "Hierra Backend is running!"}

@app.post("/initiate-project")
def initiate_project(request: ProjectInitRequest):
    print(f"Received project description: {request.description}")
    plan = agent_core.generate_plan(request.description)
    if not plan:
        raise HTTPException(status_code=500, detail="Failed to generate a plan from the AI model.")
    
    app_state.set_plan(plan)
    print("Successfully generated and stored the plan.")
    return {"plan": plan.dict()}

@app.post("/execute-next-step")
def execute_next_step():
    current_step_info = app_state.get_current_step()
    if not current_step_info:
        return {"status": "complete", "message": "The entire plan has been executed."}

    print(f"Executing Step {current_step_info['step_index']}: {current_step_info['description']}")
    
    context_buffer = memory_manager.get_context_buffer()
    
    agent_action = agent_core.execute_step(current_step_info['description'], context_buffer)
    
    if not agent_action:
        raise HTTPException(status_code=500, detail="Agent failed to decide on an action.")

    action_result = {}
    action_type = agent_action.action_type

    # Perform the action decided by the agent
    if action_type == "create_file":
        # Ensure parameters are not None before using them
        if agent_action.relative_path is None or agent_action.content is None:
             raise HTTPException(status_code=400, detail="Agent chose 'create_file' but did not provide 'relative_path' or 'content'.")
        action_result = file_handler.create_or_update_file(
            relative_path=agent_action.relative_path,
            content=agent_action.content
        )
    elif action_type == "run_command":
        if agent_action.command is None:
            raise HTTPException(status_code=400, detail="Agent chose 'run_command' but did not provide a 'command'.")
        action_result = file_handler.run_command(command=agent_action.command)
    elif action_type == "final_response":
        action_result = {"status": "success", "message": agent_action.message}
    else:
        raise HTTPException(status_code=400, detail=f"Agent chose an invalid action type: {action_type}")
    
    if action_result.get("status") == "error":
        raise HTTPException(status_code=500, detail=f"Action failed: {action_result.get('message')}")
    
    app_state.last_action_context = {"action": agent_action.dict(), "result": action_result}

    # Return the agent's thought process and the result of the action to the frontend
    return {
        "thought": agent_action.thought,
        "action": agent_action.dict(),
        "action_result": action_result
    }

@app.post("/proceed-and-save")
def proceed_and_save():
    """
    Confirms the last action was successful, saves it to memory, and advances the plan.
    """
    current_step_info = app_state.get_current_step()
    if not current_step_info:
        raise HTTPException(status_code=400, detail="No active plan or step to proceed from.")

    last_action = app_state.last_action_context
    if not last_action:
         raise HTTPException(status_code=400, detail="No previous action to save. Please execute a step first.")

    print(f"Saving step {current_step_info['step_index']} to memory...")
    
    # 1. Generate Summaries
    summaries = agent_core.generate_summaries(
        step_description=current_step_info['description'],
        full_context=last_action
    )
    if not summaries:
        raise HTTPException(status_code=500, detail="Failed to generate summaries for the step.")
    
    # 2. Save to Hierarchical Memory
    memory_manager.save_step_to_memory(
        step_id=current_step_info['step_index'],
        plan_description=current_step_info['description'],
        level_3_summary=summaries.level_3_summary,
        level_2_summary=summaries.level_2_summary,
        level_1_full_context=last_action
    )
    
    print("Step saved successfully.")
    
    # 3. Advance to the next step
    app_state.advance_to_next_step()
    
    next_step = app_state.get_current_step()
    if not next_step:
        return {"status": "complete", "message": "Plan finished! All steps have been saved to memory."}
    
    return {"status": "success", "message": f"Step saved. Now at step {next_step['step_index']}: {next_step['description']}"}

