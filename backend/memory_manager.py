# memory_manager.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

# Load environment variables from the .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# --- Database Connection ---
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client.hierra_agent_db # You can name your database anything
    # The collection will store one document per completed step
    memory_collection = db.hierarchical_memory 
    
    # Test the connection
    client.admin.command('ping')
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None
    memory_collection = None

# --- Core Memory Functions ---

def save_step_to_memory(
    step_id: int, 
    plan_description: str,
    level_3_summary: str, 
    level_2_summary: str, 
    level_1_full_context: dict
    ):
    """
    Saves a completed step's context across all three hierarchical levels.
    A unique document is created for each step.
    """
    if memory_collection is None:
        return {"status": "error", "message": "Database not connected."}
    
    try:
        document = {
            "step_id": step_id,
            "plan_description": plan_description,
            "level_3_summary": level_3_summary, # High-level summary (1 sentence)
            "level_2_summary": level_2_summary, # Detailed summary (paragraph)
            "level_1_full_context": level_1_full_context # Raw code, filename, etc.
        }
        # Use update_one with upsert=True to create or overwrite the document for a given step_id
        memory_collection.update_one(
            {"step_id": step_id},
            {"$set": document},
            upsert=True
        )
        return {"status": "success", "step_id": step_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_context_buffer() -> list:
    """
    Retrieves the default context buffer for the agent.
    This consists of all Level 3 summaries from previously completed steps.
    """
    if memory_collection is None:
        return []
    
    try:
        # Find all documents, but only project the fields we need (step_id and level_3_summary)
        steps = memory_collection.find({}, {"_id": 0, "step_id": 1, "plan_description": 1, "level_3_summary": 1}).sort("step_id", 1)
        return list(steps)
    except Exception:
        return []

def get_deep_context(step_id: int, level: int) -> dict:
    """
    Retrieves a deeper level of context (Level 2 or Level 1) for a specific step.
    """
    if memory_collection is None:
        return {"status": "error", "message": "Database not connected."}
    
    if level not in [1, 2]:
        return {"status": "error", "message": "Invalid context level requested."}
    
    try:
        field_to_get = f"level_{level}_summary" if level == 2 else f"level_{level}_full_context"
        
        # Find the specific document and project only the requested field
        result = memory_collection.find_one(
            {"step_id": step_id},
            {"_id": 0, field_to_get: 1}
        )
        
        if result:
            return {"status": "success", "data": result.get(field_to_get)}
        else:
            return {"status": "error", "message": f"Step {step_id} not found in memory."}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
