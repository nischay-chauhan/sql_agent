import sqlglot
from core.llm import llm

def validate_or_correct_sql(sql_query: str, schema: str) -> str:
    try:
        sqlglot.parse_one(sql_query)
        return sql_query  # valid
    except Exception as e:
        correction_prompt = f"""
        SQL invalid: {sql_query}
        Error: {str(e)}
        Fix this SQL based on schema:
        {schema}
        """
        correction = llm.invoke(correction_prompt)
        return correction.content.strip()
