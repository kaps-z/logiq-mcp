from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import shutil
import datetime
from dotenv import load_dotenv

from tools.db_tools import fetch_logs
from tools.ai_tools import preview_code_fix

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FixRequest(BaseModel):
    service: str
    file_path: str

class ApplyRequest(BaseModel):
    file_path: str
    updated_code: str
    changes_summary: str

@app.post("/api/suggest-fix")
async def suggest_fix(req: FixRequest):
    """
    Fetch recent logs for the service and run AI to generate a patched preview snippet.
    Does not modify any files.
    """
    try:
        raw_logs = fetch_logs(level="ERROR", service=req.service, limit=10)
        logs_list = json.loads(raw_logs)
        if not logs_list or "error" in logs_list:
            # Fallback if no specific ERROR logs exist; fetch standard ones.
            raw_logs = fetch_logs(service=req.service, limit=5)
            
        result = await preview_code_fix(raw_logs, req.file_path)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/apply-fix")
async def apply_fix(req: ApplyRequest):
    """
    Given an approved payload, actually writes the corrected code to disk,
    backs up the original safely, and publishes an audit log.
    """
    if not os.path.exists(req.file_path):
         raise HTTPException(status_code=400, detail="File not found")
         
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{req.file_path}.{timestamp}.bak"
        shutil.copy2(req.file_path, backup_path)
        
        with open(req.file_path, "w", encoding="utf-8") as f:
             f.write(req.updated_code)
             
        audit_log_path = os.path.join(os.path.dirname(__file__), "audit.log")
        with open(audit_log_path, "a", encoding="utf-8") as f:
             f.write(f"[{datetime.datetime.now().isoformat()}] FIX APPLIED to {req.file_path} via UI Approval\n")
             f.write(f"Summary: {req.changes_summary}\n")
             f.write("-" * 50 + "\n")
             
        return {"status": "success", "message": f"Code fixed successfully! Backup at {backup_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply fix: {str(e)}")
