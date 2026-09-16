import sqlite3
import pandas as pd

def get_schema_context(db_path: str = "demo_analytics.db") -> str:
    """Extracts database schema and sample rows for the LLM prompt."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schema_strings = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [f"{col[1]} ({col[2]})" for col in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM {table} LIMIT 2;")
        samples = cursor.fetchall()
        
        table_fmt = (
            f"Table: {table}\n"
            f"Columns: {', '.join(columns)}\n"
            f"Sample Rows: {samples}\n"
        )
        schema_strings.append(table_fmt)
        
    conn.close()
    return "\n".join(schema_strings)

def execute_sql_query(query: str, db_path: str = "demo_analytics.db") -> pd.DataFrame:
    """Executes a generated SQL query safely for the backend."""
    conn = sqlite3.connect(db_path)
    try:
        clean_query = query.replace("```sql", "").replace("```", "").strip()
        df = pd.read_sql_query(clean_query, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        raise e
