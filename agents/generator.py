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

    try:
        json_data = json.loads(text)
        sql_query = json_data.get("sql", "").strip()
    except json.JSONDecodeError:
        sql_query = text.replace("```sql", "").replace("```", "").strip()
        if not sql_query.endswith(';'):
            sql_query += ';'
    except Exception:
        sql_query = text

    return sql_query