from fastapi import FastAPI
from pydantic import BaseModel
from core.graph import app

class QueryRequest(BaseModel):
    question: str
    schema: str

api = FastAPI(title="LangGraph SQL Assistant")

@api.post("/query")
async def run_query(request: QueryRequest):
    result = app.invoke({
        "question": request.question,
        "schema": request.schema,
    })
    return {
        "sql_query": result["sql_query"],
        "result": result["result"],
        "final_answer": result["final_answer"],
    }
