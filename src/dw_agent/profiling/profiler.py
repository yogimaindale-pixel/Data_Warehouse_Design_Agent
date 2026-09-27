"""Main profiler for sample CSV and SQLite files."""

import os
import csv
import sqlite3
from typing import List, Dict
from dw_agent.contracts import ProfileResult
from dw_agent.profiling.key_discovery import discover_candidate_keys
from dw_agent.profiling.quality_profiler import detect_pii_candidates

def profile_sample_data(project_path: str) -> List[ProfileResult]:
    sample_dir = os.path.join(project_path, "inputs", "sample_data")
    results: List[ProfileResult] = []

    if not os.path.exists(sample_dir):
        return results

    for fname in os.listdir(sample_dir):
        fpath = os.path.join(sample_dir, fname)
        
        # CSV Profiling
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

                keys = discover_candidate_keys(col_stats, total_rows)
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

        # SQLite Profiling
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
