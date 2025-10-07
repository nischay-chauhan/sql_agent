from core.llm import llm

def generate_sql(question: str, schema: str) -> str:
    prompt = f"""
    You are a SQL expert. Generate a SQL query for the question below.
    Question: "{question}"
    Schema:
    {schema}
    Output only the SQL query.
    """
    response = llm.invoke(prompt)
    return response.content.strip()
