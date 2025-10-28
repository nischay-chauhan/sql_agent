from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel, Field
from typing import Dict
import secrets
import json
from core.graph import app as graph_app

# Create FastAPI app
app = FastAPI(title="SQL Bot")

# Add middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_hex(32),  # Generate a random secret key
    session_cookie="sqlbot_session"
)

# In-memory storage for schemas (in production, use Redis or a database)
user_schemas: Dict[str, str] = {}

class SchemaRequest(BaseModel):
    schema_def: str = Field(..., alias="schema")  # Use alias to avoid shadowing

class QueryRequest(BaseModel):
    question: str

@app.post("/set_schema")
async def set_schema(request: Request, schema_req: SchemaRequest):
    # Generate a session ID if it doesn't exist
    if not request.session.get("id"):
        request.session["id"] = secrets.token_urlsafe(16)
    
    # Store schema in memory
    user_schemas[request.session["id"]] = schema_req.schema_def
    return {"status": "Schema set successfully"}

@app.post("/query")
async def run_query(request: Request, query_req: QueryRequest):
    # Get session ID
    session_id = request.session.get("id")
    if not session_id or session_id not in user_schemas:
        raise HTTPException(status_code=400, detail="Please set the schema first using /set_schema endpoint")
    
    # Get the schema from memory
    schema = user_schemas[session_id]
    
    try:
        # Generate and return the SQL query
        result = graph_app.invoke({
            "question": query_req.question,
            "schema": schema,
            "sql_query": "",  # Initialize empty
            "validation_error": "",
            "result": None,
            "final_answer": ""
        })
        
        return {
            "sql_query": result["sql_query"],
            "result": result.get("result"),
            "final_answer": result.get("final_answer", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))