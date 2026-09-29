# Module docstring explaining source SQL DDL parsing and table schema extraction
"""DDL parser extracting source table definitions, primary keys, foreign keys, and PII flags from SQL DDL files."""

# Import os module for directory listing and path joining
import os
# Import re module for regex parsing of SQL statements
import re
# Import List type hint
from typing import List
# Import SourceTable and SourceColumn contract dataclasses
from dw_agent.contracts import SourceTable, SourceColumn

# List of regex patterns identifying potential Personally Identifiable Information (PII) columns
PII_PATTERNS = [r"email", r"ssn", r"phone", r"credit_card", r"password", r"first_name", r"last_name", r"address", r"dob", r"tax_id"]

# Main function parsing all SQL DDL files in 'inputs/source_ddl/'
def parse_source_ddl(project_path: str) -> List[SourceTable]:
    """Parse source SQL DDL schema files and construct typed SourceTable objects.

    Args:
        project_path (str): Root path of the project.

    Returns:
        List[SourceTable]: List of parsed source tables with columns, primary keys, and foreign keys.
    """
    ddl_dir = os.path.join(project_path, "inputs", "source_ddl")
    tables: List[SourceTable] = []
    
    # Return empty list if source_ddl directory is absent
    if not os.path.exists(ddl_dir):
        return tables

    # Iterate through all SQL files in the ddl_dir
    for fname in os.listdir(ddl_dir):
        if fname.endswith(".sql"):
            fpath = os.path.join(ddl_dir, fname)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                sql_content = f.read()

            # Split SQL file content into individual statements by semicolon
            statements = sql_content.split(";")
            for stmt in statements:
                stmt_clean = stmt.strip()
                # Skip empty statements or non-CREATE TABLE statements
                if not stmt_clean or not re.search(r"CREATE\s+TABLE", stmt_clean, re.IGNORECASE):
                    continue

                # Match table name using regex
                table_match = re.search(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`\"\w]+)", stmt_clean, re.IGNORECASE)
                if not table_match:
                    continue

                # Strip quotes or backticks from table name
                raw_table_name = table_match.group(1).replace("`", "").replace('"', "")
                
                # Extract CREATE TABLE body enclosed in parentheses
                body_match = re.search(r"\((.*)\)", stmt_clean, re.DOTALL)
                if not body_match:
                    continue

                body = body_match.group(1)
                lines = [l.strip() for l in body.split(",") if l.strip()]

                cols: List[SourceColumn] = []
                pks = []
                fks = []

                # Parse each column line or table constraint line
                for line in lines:
                    line_upper = line.upper()
                    # Parse standalone PRIMARY KEY constraint
                    if line_upper.startswith("PRIMARY KEY"):
                        pk_match = re.search(r"PRIMARY\s+KEY\s*\(([^)]+)\)", line, re.IGNORECASE)
                        if pk_match:
                            pks.extend([p.strip().replace("`", "").replace('"', "") for p in pk_match.group(1).split(",")])
                        continue
                    # Parse FOREIGN KEY constraint
                    if line_upper.startswith("FOREIGN KEY") or "REFERENCES" in line_upper:
                        fk_match = re.search(r"FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+([`\"\w]+)\s*\(([^)]+)\)", line, re.IGNORECASE)
                        if fk_match:
                            fks.append({
                                "col": fk_match.group(1).strip().replace("`", "").replace('"', ""),
                                "target_table": fk_match.group(2).strip().replace("`", "").replace('"', ""),
                                "target_col": fk_match.group(3).strip().replace("`", "").replace('"', "")
                            })
                        continue

                    # Parse column definition line
                    parts = line.split()
                    if len(parts) >= 2:
                        col_name = parts[0].replace("`", "").replace('"', "")
                        col_type = parts[1].upper()
                        
                        is_pk = "PRIMARY KEY" in line_upper
                        if is_pk:
                            pks.append(col_name)

                        # Flag potential PII columns
                        is_pii = any(re.search(pat, col_name, re.IGNORECASE) for pat in PII_PATTERNS)
                        
                        cols.append(
                            SourceColumn(
                                name=col_name,
                                data_type=col_type,
                                is_pk=is_pk,
                                is_nullable="NOT NULL" not in line_upper,
                                is_pii_candidate=is_pii
                            )
                        )

                # Attach parsed PK and FK metadata to matching columns
                for c in cols:
                    if c.name in pks:
                        c.is_pk = True
                    for fk in fks:
                        if fk["col"] == c.name:
                            c.is_fk = True
                            c.fk_target_table = fk["target_table"]
                            c.fk_target_column = fk["target_col"]

                # Append parsed table object
                tables.append(SourceTable(name=raw_table_name, columns=cols))

    return tables

