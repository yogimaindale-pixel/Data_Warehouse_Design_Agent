"""SQL validator using local SQLite in-memory execution."""

import sqlite3
from typing import Tuple

def validate_sqlite_ddl(ddl_sql: str) -> Tuple[bool, str]:
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.executescript(ddl_sql)
        conn.close()
        return True, "SQL DDL executed successfully in SQLite in-memory engine."
    except Exception as e:
        return False, f"SQL DDL execution error: {str(e)}"
