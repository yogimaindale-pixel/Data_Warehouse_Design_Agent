# Module docstring explaining SQL DDL syntax validation via in-memory SQLite execution
"""SQL validator testing generated DDL statements for syntax correctness using an in-memory SQLite engine."""

# Import sqlite3 database engine module
import sqlite3
# Import Tuple type hint
from typing import Tuple

# Function testing generated DDL script execution in SQLite
def validate_sqlite_ddl(ddl_sql: str) -> Tuple[bool, str]:
    """Execute generated DDL script against an in-memory SQLite database to verify SQL syntax correctness.

    Args:
        ddl_sql (str): Multi-statement SQL DDL script string.

    Returns:
        Tuple[bool, str]: Tuple of (success_boolean, status_message_or_error_details).
    """
    try:
        # Create an isolated in-memory SQLite connection
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        # Execute entire DDL script
        cursor.executescript(ddl_sql)
        conn.close()
        return True, "SQL DDL executed successfully in SQLite in-memory engine."
    except Exception as e:
        return False, f"SQL DDL execution error: {str(e)}"

