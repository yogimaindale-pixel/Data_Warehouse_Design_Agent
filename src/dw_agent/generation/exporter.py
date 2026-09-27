"""Exporter module for generating all 27 required deliverables in output/ directory."""

import os
import csv
import json
from typing import List, Dict, Any

try:
    import openpyxl
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

def write_csv(filepath: str, headers: List[str], rows: List[List[Any]]):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def write_excel(filepath: str, headers: List[str], rows: List[List[Any]]):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if HAS_OPENPYXL:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for r in rows:
            ws.append([str(item) if item is not None else "" for item in r])
        wb.save(filepath)
    else:
        # Fallback to CSV if openpyxl is not available
        csv_path = filepath.replace(".xlsx", ".csv")
        write_csv(csv_path, headers, rows)

def write_file(filepath: str, content: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def export_all_deliverables(
    output_dir: str,
    exec_summary_md: str,
    inventory_rows: List[List[Any]],
    req_rows: List[List[Any]],
    assumptions_md: str,
    profile_rows: List[List[Any]],
    process_rows: List[List[Any]],
    grain_md: str,
    bus_matrix_headers: List[str],
    bus_matrix_rows: List[List[Any]],
    dim_rows: List[List[Any]],
    fact_rows: List[List[Any]],
    conceptual_mmd: str,
    logical_mmd: str,
    physical_mmd: str,
    target_ddl_sql: str,
    rollback_sql: str,
    sttm_rows: List[List[Any]],
    etl_spec_md: str,
    dq_rows: List[List[Any]],
    lineage_rows: List[List[Any]],
    security_md: str,
    performance_md: str,
    test_rows: List[List[Any]],
    traceability_rows: List[List[Any]],
    adrs_md: str,
    validation_report_md: str,
    backlog_rows: List[List[Any]],
    review_checklist_md: str,
    manifest_data: Dict[str, Any]
):
    os.makedirs(output_dir, exist_ok=True)

    # 00
    write_file(os.path.join(output_dir, "00_EXECUTIVE_SUMMARY.md"), exec_summary_md)
    # 01
    write_csv(os.path.join(output_dir, "01_INPUT_INVENTORY.csv"), ["file_path", "file_type", "file_hash", "size_bytes"], inventory_rows)
    # 02
    write_csv(os.path.join(output_dir, "02_REQUIREMENTS_CATALOG.csv"), ["req_id", "category", "title", "description", "source_file"], req_rows)
    # 03
    write_file(os.path.join(output_dir, "03_OPEN_QUESTIONS_AND_ASSUMPTIONS.md"), assumptions_md)
    # 04
    write_excel(os.path.join(output_dir, "04_SOURCE_PROFILE.xlsx"), ["table_name", "row_count", "column", "distinct_count", "null_pct", "pii_candidate"], profile_rows)
    # 05
    write_csv(os.path.join(output_dir, "05_BUSINESS_PROCESS_CATALOG.csv"), ["process_id", "name", "triggering_event", "fact_type", "source_tables"], process_rows)
    # 06
    write_file(os.path.join(output_dir, "06_GRAIN_DECLARATIONS.md"), grain_md)
    # 07
    write_csv(os.path.join(output_dir, "07_BUS_MATRIX.csv"), bus_matrix_headers, bus_matrix_rows)
    # 08
    write_excel(os.path.join(output_dir, "08_DIMENSION_CATALOG.xlsx"), ["table_name", "surrogate_key", "business_key", "column_name", "data_type", "scd_type"], dim_rows)
    # 09
    write_excel(os.path.join(output_dir, "09_FACT_CATALOG.xlsx"), ["table_name", "process_id", "fact_type", "grain_sentence", "measure_or_fk", "type_or_formula", "additivity"], fact_rows)
    # 10
    write_file(os.path.join(output_dir, "10_CONCEPTUAL_MODEL.mmd"), conceptual_mmd)
    # 11
    write_file(os.path.join(output_dir, "11_LOGICAL_MODEL.mmd"), logical_mmd)
    # 12
    write_file(os.path.join(output_dir, "12_PHYSICAL_MODEL.mmd"), physical_mmd)
    # 13
    write_file(os.path.join(output_dir, "13_TARGET_DDL.sql"), target_ddl_sql)
    # 14
    write_file(os.path.join(output_dir, "14_ROLLBACK_DDL.sql"), rollback_sql)
    # 15
    write_excel(os.path.join(output_dir, "15_STTM.xlsx"), ["mapping_id", "target_table", "target_column", "source_system", "source_table", "source_column", "transformation", "lookup_rule", "default_rule", "rejection_behavior", "dq_rule_ids", "scd_behavior", "req_id"], sttm_rows)
    # 16
    write_file(os.path.join(output_dir, "16_ETL_SPECIFICATIONS.md"), etl_spec_md)
    # 17
    write_excel(os.path.join(output_dir, "17_DATA_QUALITY_RULES.xlsx"), ["rule_id", "category", "target_table", "target_column", "condition", "severity", "threshold", "action"], dq_rows)
    # 18
    write_csv(os.path.join(output_dir, "18_LINEAGE.csv"), ["source_system", "source_table", "source_column", "target_table", "target_column", "transformation"], lineage_rows)
    # 19
    write_file(os.path.join(output_dir, "19_SECURITY_AND_PRIVACY_CONSIDERATIONS.md"), security_md)
    # 20
    write_file(os.path.join(output_dir, "20_PERFORMANCE_DESIGN.md"), performance_md)
    # 21
    write_excel(os.path.join(output_dir, "21_TEST_CASES.xlsx"), ["test_id", "category", "target_object", "test_description", "expected_result"], test_rows)
    # 22
    write_excel(os.path.join(output_dir, "22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx"), ["requirement_id", "category", "title", "mapped_target_object", "validation_status"], traceability_rows)
    # 23
    write_file(os.path.join(output_dir, "23_ARCHITECTURE_DECISIONS.md"), adrs_md)
    # 24
    write_file(os.path.join(output_dir, "24_MODEL_VALIDATION_REPORT.md"), validation_report_md)
    # 25
    write_csv(os.path.join(output_dir, "25_IMPLEMENTATION_BACKLOG.csv"), ["task_id", "work_stream", "description", "priority", "estimated_hours"], backlog_rows)
    # 26
    write_file(os.path.join(output_dir, "26_REVIEW_CHECKLIST.md"), review_checklist_md)
    # manifest.json
    write_file(os.path.join(output_dir, "manifest.json"), json.dumps(manifest_data, indent=2))
