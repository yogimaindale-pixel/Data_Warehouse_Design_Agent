# Module docstring explaining data profiling logic for CSV and SQLite sample datasets
"""Main profiler computing row counts, column metrics, null ratios, min/max values, candidate natural keys, and PII flags."""

# Import os module for path joining and directory scanning
import os
# Import csv module for reading sample CSV files
import csv
# Import sqlite3 module for profiling SQLite database files
import sqlite3
# Import List and Dict type hints
from typing import List, Dict
# Import ProfileResult dataclass contract
from dw_agent.contracts import ProfileResult
# Import key discovery helper function
from dw_agent.profiling.key_discovery import discover_candidate_keys
# Import PII detection helper function
from dw_agent.profiling.quality_profiler import detect_pii_candidates

# Master profiling function scanning 'inputs/sample_data/' directory
def profile_sample_data(project_path: str) -> List[ProfileResult]:
    """Profile sample datasets (CSV files and SQLite DBs) in 'inputs/sample_data/'.

    Args:
        project_path (str): Root path of the project.

    Returns:
        List[ProfileResult]: List of ProfileResult objects containing table-level and column-level metrics.
    """
    sample_dir = os.path.join(project_path, "inputs", "sample_data")
    results: List[ProfileResult] = []

    # Return empty list if sample_data folder does not exist
    if not os.path.exists(sample_dir):
        return results

    # Iterate through sample data files
    for fname in os.listdir(sample_dir):
        fpath = os.path.join(sample_dir, fname)
        
        # 1. Profile CSV sample data files
        if fname.endswith(".csv"):
            tbl_name = os.path.splitext(fname)[0]
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                if not headers:
                    continue
                rows = list(reader)
                total_rows = len(rows)

                col_stats = {}
                # Calculate per-column profiling statistics
                for idx, h in enumerate(headers):
                    col_vals = [r[idx] for r in rows if idx < len(r)]
                    null_cnt = sum(1 for v in col_vals if v is None or v.strip() == "")
                    non_nulls = [v for v in col_vals if v is not None and v.strip() != ""]
                    distinct_cnt = len(set(col_vals))
                    min_val = min(non_nulls) if non_nulls else None
                    max_val = max(non_nulls) if non_nulls else None

                    col_stats[h] = {
                        "distinct_count": distinct_cnt,
                        "null_count": null_cnt,
                        "null_pct": round((null_cnt / total_rows * 100), 2) if total_rows > 0 else 0,
                        "min_val": min_val,
                        "max_val": max_val
                    }

                # Discover candidate unique natural keys
                keys = discover_candidate_keys(col_stats, total_rows)
                # Detect PII candidate columns
                pii = detect_pii_candidates(headers)

                results.append(
                    ProfileResult(
                        table_name=tbl_name,
                        row_count=total_rows,
                        columns=col_stats,
                        candidate_natural_keys=keys,
                        pii_columns=pii
                    )
                )

        # 2. Profile SQLite sample database files
        elif fname.endswith(".db") or fname.endswith(".sqlite"):
            try:
                conn = sqlite3.connect(fpath)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [r[0] for r in cursor.fetchall()]

                for tbl_name in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {tbl_name};")
                    total_rows = cursor.fetchone()[0]

                    cursor.execute(f"PRAGMA table_info({tbl_name});")
                    col_info = cursor.fetchall()  # (cid, name, type, notnull, dflt_value, pk)

                    col_stats = {}
                    col_names = [c[1] for c in col_info]

                    for c in col_info:
                        col_name = c[1]
                        cursor.execute(f"SELECT COUNT(DISTINCT {col_name}), COUNT(*) - COUNT({col_name}) FROM {tbl_name};")
                        row = cursor.fetchone()
                        distinct_cnt = row[0] if row else 0
                        null_cnt = row[1] if row else 0

                        col_stats[col_name] = {
                            "distinct_count": distinct_cnt,
                            "null_count": null_cnt,
                            "null_pct": round((null_cnt / total_rows * 100), 2) if total_rows > 0 else 0
                        }

                    keys = discover_candidate_keys(col_stats, total_rows)
                    pii = detect_pii_candidates(col_names)

                    results.append(
                        ProfileResult(
                            table_name=tbl_name,
                            row_count=total_rows,
                            columns=col_stats,
                            candidate_natural_keys=keys,
                            pii_columns=pii
                        )
                    )
                conn.close()
            except Exception:
                pass

    return results

