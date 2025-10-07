from langgraph.graph import StateGraph, END
from typing import TypedDict, Any
from agents.generator import generate_sql
from agents.validator import validate_or_correct_sql
from agents.executor import execute_and_summarize
from core.db import setup_demo_db

class SQLState(TypedDict):
    question: str
    schema: str
    sql_query: str
    validation_error: str
    result: Any
    final_answer: str

conn = setup_demo_db()
cursor = conn.cursor()

def node_generate(state: SQLState):
    state["sql_query"] = generate_sql(state["question"], state["schema"])
    return state

def node_validate(state: SQLState):
    state["sql_query"] = validate_or_correct_sql(state["sql_query"], state["schema"])
    return state

def node_execute(state: SQLState):
    rows, summary = execute_and_summarize(cursor, state["question"], state["sql_query"])
    state["result"] = rows
    state["final_answer"] = summary
    return state

graph = StateGraph(SQLState)
graph.add_node("generate", node_generate)
graph.add_node("validate", node_validate)
graph.add_node("execute", node_execute)

graph.set_entry_point("generate")
graph.add_edge("generate", "validate")
graph.add_edge("validate", "execute")
graph.add_edge("execute", END)

app = graph.compile()
