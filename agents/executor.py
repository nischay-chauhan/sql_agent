from core.llm import llm

def execute_and_summarize(cursor, question: str, sql_query: str):
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        summary_prompt = f"""
        User asked: {question}
        Query Result: {rows}
        Provide a clear human-readable summary.
        """
        summary = llm.invoke(summary_prompt)
        return rows, summary.content.strip()
    except Exception as e:
        return None, f"Execution error: {str(e)}"
