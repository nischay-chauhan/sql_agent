from core.llm import llm
import json

def generate_sql(question, schema):
    prompt = f"""
You are an expert SQL query generator.
You will receive:
1. A database schema.
2. A natural language question.

Your job:
- Return a valid SQL query that can be executed directly.
- The output must be in strict JSON format only.

### Rules
- Do NOT include explanations, comments, or markdown.
- Only return JSON in this exact format:
{{
  "sql": "<SQL query>"
}}

Schema:
{schema}

Question:
{question}
"""
    response = llm.invoke(prompt)
    text = response.content.strip()

    # Try to extract JSON from the LLM response
    try:
        json_data = json.loads(text)
        sql_query = json_data.get("sql", "").strip()
    except Exception:
        # fallback: try to clean the text manually
        sql_query = text.replace("```json", "").replace("```", "").strip()

    return sql_query