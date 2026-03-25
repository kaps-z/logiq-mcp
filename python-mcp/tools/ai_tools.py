import os
import json
import shutil
import datetime
from openai import AsyncOpenAI
import traceback

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy_key"))

async def analyze_logs(logs: str) -> str:
    try:
        prompt = f"""
        You are a senior DevOps engineer analyzing application logs. Analyze these logs and identify the root cause of any issues.
        Return ONLY a JSON object with the following schema:
        {{
            "issue_type": "string (e.g., db_failure, memory_issue, network_timeout, etc.)",
            "severity": "string (HIGH, MEDIUM, LOW)",
            "explanation": "string explaining the issue",
            "confidence_score": "float from 0.0 to 1.0"
        }}
        
        Logs to analyze:
        {logs}
        """
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": f"AI Analysis failed: {str(e)}"})

async def fix_issue(issue_type: str) -> str:
    try:
        prompt = f"""
        Provide actionable fix steps for the issue type: {issue_type}.
        Return ONLY a JSON object with this schema:
        {{
            "actionable_steps": ["step 1", "step 2"],
            "requires_restart": "boolean"
        }}
        """
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": f"Actionable steps generation failed: {str(e)}"})

async def fix_code_based_on_logs(logs: str, file_path: str) -> str:
    try:
        if not os.path.exists(file_path):
            return json.dumps({"error": f"File not found: {file_path}"})
            
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.{timestamp}.bak"
        shutil.copy2(file_path, backup_path)
        
        prompt = f"""
        You are an elite autonomous AI developer. 
        Analyze the provided logs and the source code of the file. 
        Determine the root cause of the errors in the logs and fix the source code.
        
        Requirements:
        1. Add proper error handling, retry logic, or resource cleanup.
        2. Ensure logging statements are added/updated for future debugging.
        3. Add clear comments in the code explaining what the AI changed and why (e.g. "// AI FIX: ...").
        4. Do NOT wrap the returned code in markdown blocks like ```python or ```javascript, just return the raw valid code as a string inside the JSON object's 'updated_code' field.

        Return ONLY a JSON object with this schema:
        {{
            "updated_code": "The full source code of the file after your fixes (no markdown blocks)",
            "changes_summary": "A detailed explanation of what was fixed and why",
            "confidence_score": "float from 0.0 to 1.0",
            "affected_logs": "Short summary of the logs that triggered this fix"
        }}
        
        Logs:
        {logs}
        
        Original Source Code:
        {original_code}
        """
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        result_json = json.loads(response.choices[0].message.content)
        updated_code = result_json.get("updated_code", "")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)
            
        audit_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audit.log")
        with open(audit_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] FIX APPLIED to {file_path}\n")
            f.write(f"Confidence: {result_json.get('confidence_score')}\n")
            f.write(f"Summary: {result_json.get('changes_summary')}\n")
            f.write("-" * 50 + "\n")
            
        return json.dumps({
            "status": "success",
            "file_patched": file_path,
            "backup_created": backup_path,
            "changes_summary": result_json.get("changes_summary"),
            "confidence_score": result_json.get("confidence_score")
        })
        
    except Exception as e:
        return json.dumps({"error": f"Auto-fix failed: {str(e)}", "traceback": traceback.format_exc()})

