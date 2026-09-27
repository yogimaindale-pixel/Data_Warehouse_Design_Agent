"""Generator for full 26-document Knowledge Transfer package."""

import os

KT_FILES = {
    "00_KT_INDEX.md": """# Knowledge Transfer Index & Learning Paths

Welcome to the Data Warehouse Design Agent Knowledge Transfer (KT) package.

## Role-Based Reading Paths

### 1. Junior Engineer / Data Engineer Path
1. `01_PROJECT_DESCRIPTION.md` - Scope, boundaries, and outcome.
2. `05_PREREQUISITES_AND_SETUP.md` - Environment setup.
3. `06_CONSOLE_COMMAND_REFERENCE.md` - How to run CLI commands.
4. `08_END_TO_END_EXECUTION_FLOW.md` - Pipeline execution flow.
5. `18_TESTING_GUIDE.md` - Running unit and scenario tests.

### 2. Data Architect / Modeler Path
1. `03_ARCHITECTURE.md` - System architecture.
2. `10_DIMENSIONAL_MODELING_ENGINE.md` - Modeling rules.
3. `11_GRAIN_FACTS_DIMENSIONS_AND_SCD.md` - Grain & SCD policies.
4. `12_BUS_MATRIX_AND_CONFORMANCE.md` - Enterprise bus matrix.
5. `15_MODEL_VALIDATION_AND_REVIEW.md` - Quality gates.

### 3. Support & Operations Path
1. `16_OPERATIONS_RUNBOOK.md` - Operating procedure.
2. `17_TROUBLESHOOTING_GUIDE.md` - Fixing failures.
3. `23_SUPPORT_HANDOVER_CHECKLIST.md` - Handover requirements.
""",

    "01_PROJECT_DESCRIPTION.md": """# Project Description & Scope

The Data Warehouse Design Agent is a command-line Python application that converts business requirements, source DDLs, metadata, and sample data into a governed, implementation-ready warehouse design package.

## Scope Boundaries
- **In Scope**: Console interface, deterministic modeling, multi-dialect DDL generation (SQLite, PostgreSQL, Snowflake, BigQuery, Synapse), STTM generation, data quality rules, lineage, and 27 output deliverables.
- **Out of Scope**: Web UI or browser frontends, autonomous production database execution, sensitive production data ingestion.
""",

    "02_BUSINESS_PROBLEM_AND_VALUE.md": """# Business Problem & Value Hypothesis

## Manual Modeling Pain Points
- Fragmented documentation across spreadsheets and slide decks.
- Inconsistent grain declarations leading to multi-grain join fan-out bugs.
- Manual DDL and STTM preparation taking weeks per data mart.

## Value Delivered
- **Speed**: Automates draft design preparation from weeks to seconds.
- **Consistency**: Enforces 100% deterministic dimensional modeling rules.
- **Auditability**: Records rule-level evidence for every modeling decision.
""",

    "03_ARCHITECTURE.md": """# System Architecture

```text
Requirements / Source DDL / Metadata / Sample Data
                         |
                         v
               Python Console CLI
                         |
                         v
       Discovery -> Profiling -> Rules Engine
                         |
           Facts / Dimensions / SCD / Bus Matrix
                         |
          DDL / STTM / ETL / DQ / Lineage / Tests
                         |
               Validation & Review Gate
                         |
             27 Deliverable Outputs
```
""",

    "04_REPOSITORY_WALKTHROUGH.md": """# Repository Structure Walkthrough

- `src/dw_agent/cli.py`: Command line interface.
- `src/dw_agent/discovery/`: Parsers for requirements, DDLs, metadata.
- `src/dw_agent/profiling/`: Profiler for CSV and SQLite sample data.
- `src/dw_agent/modeling/`: Dimensional design logic (grain, facts, dims, SCD, bus matrix).
- `src/dw_agent/generation/`: Deliverable generators (DDL, STTM, ETL, DQ, Lineage, Mermaid).
- `src/dw_agent/validation/`: Quality gates and model acceptance.
""",

    "05_PREREQUISITES_AND_SETUP.md": """# Prerequisites & Setup Guide

## Requirements
- Python 3.11+
- Virtualenv

## Setup Steps
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt pytest
```
""",

    "06_CONSOLE_COMMAND_REFERENCE.md": """# Console Command Reference

```bash
python -m dw_agent init --project ./my_project
python -m dw_agent inspect --project ./my_project
python -m dw_agent profile --project ./my_project
python -m dw_agent design --project ./my_project --dialect sqlite
python -m dw_agent validate --project ./my_project
python -m dw_agent report --project ./my_project
python -m dw_agent demo --scenario ecommerce
python -m dw_agent clean --project ./my_project
```
""",

    "07_INPUT_FORMATS_AND_CONFIGURATION.md": """# Input Formats & Configuration

- `inputs/requirements/`: Markdown (.md) or TXT files.
- `inputs/source_ddl/`: SQL CREATE TABLE files.
- `inputs/sample_data/`: CSV or SQLite database files.
- `config/agent.yaml`: System settings.
""",

    "08_END_TO_END_EXECUTION_FLOW.md": """# End-to-End Execution Flow

1. Scan input files and compute SHA256 hashes.
2. Parse business requirements and source DDLs.
3. Profile sample data for row count, null %, distinct values, PII candidates.
4. Identify business processes and declare single-sentence grains.
5. Design conformed dimensions and fact tables.
6. Build Enterprise Bus Matrix.
7. Generate DDL, STTM, ETL specs, DQ rules, Lineage, and Mermaid models.
8. Validate design against quality gates and execute dry-run SQL in SQLite.
""",

    "09_SOURCE_DISCOVERY_AND_PROFILING.md": """# Source Discovery & Profiling

- **DDL Parser**: Extracts table names, columns, data types, primary keys, foreign keys.
- **Profiler**: Computes uniqueness ratios, null percentages, candidate natural keys, and PII flags.
""",

    "10_DIMENSIONAL_MODELING_ENGINE.md": """# Dimensional Modeling Engine

Applies Ralph Kimball dimensional modeling principles using deterministic Python rules defined in `config/modeling_rules.yaml`.
""",

    "11_GRAIN_FACTS_DIMENSIONS_AND_SCD.md": """# Grain, Facts, Dimensions, and SCD

- **Grain**: One row per event/entity sentence rule.
- **Facts**: Transaction, Periodic Snapshot, Accumulating Snapshot, Factless.
- **Dimensions**: Conformed, Role-playing, Degenerate, Junk, Mini-dimension, Bridge.
- **SCD**: Type 0, Type 1, Type 2 (effective_date, expiration_date, is_current), Type 3.
""",

    "12_BUS_MATRIX_AND_CONFORMANCE.md": """# Enterprise Bus Matrix & Conformance

Maps business processes to conformed dimensions to prevent siloed data marts.
""",

    "13_DDL_STTM_ETL_AND_DQ_OUTPUTS.md": """# DDL, STTM, ETL, and DQ Deliverables

Describes the structure and purpose of generated `13_TARGET_DDL.sql`, `15_STTM.xlsx`, `16_ETL_SPECIFICATIONS.md`, and `17_DATA_QUALITY_RULES.xlsx`.
""",

    "14_LINEAGE_TRACEABILITY_AND_ADRS.md": """# Lineage, Traceability, & ADRs

Tracks lineage from source column -> STTM -> target column, mapped to requirements in `22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx`.
""",

    "15_MODEL_VALIDATION_AND_REVIEW.md": """# Model Validation & Quality Gates

Enforces critical rules:
- No unstated fact grains.
- No direct fact-to-fact joins.
- SCD2 validity columns present.
- STTM targets match DDL.
""",

    "16_OPERATIONS_RUNBOOK.md": """# Operations Runbook

Step-by-step procedures for running warehouse design pipelines, reviewing artifacts, and packaging outputs.
""",

    "17_TROUBLESHOOTING_GUIDE.md": """# Troubleshooting Guide

Common issues and resolutions:
- Missing inputs: Run `python -m dw_agent init`.
- Invalid SQL: Check DDL syntax in `inputs/source_ddl/`.
""",

    "18_TESTING_GUIDE.md": """# Testing Guide

Run test suite:
```bash
./venv/bin/pytest tests/
```
Includes unit, integration, and scenario tests.
""",

    "19_SECURITY_PRIVACY_AND_GOVERNANCE.md": """# Security, Privacy, & Governance

Covers safe local processing, PII candidate tagging, and masking recommendations.
""",

    "20_EXTENSION_GUIDE.md": """# Extension Guide

How to add a new SQL dialect:
1. Create `config/platform_profiles/<dialect>.yaml`.
2. Update `config/type_mapping.yaml`.
3. Add dialect tests in `tests/unit/test_ddl_generator.py`.
""",

    "21_RELEASE_DEPLOYMENT_AND_ROLLBACK.md": """# Release & Rollback Guide

Describes packaging deliverables with `scripts/package_deliverables.py` and executing `14_ROLLBACK_DDL.sql` if required.
""",

    "22_DEMO_SCRIPT.md": """# Presenter Demo Script

1. Run `python run_demo.py ecommerce`.
2. Inspect `demo_ecommerce/output/`.
3. Highlight `00_EXECUTIVE_SUMMARY.md`, `07_BUS_MATRIX.csv`, and `13_TARGET_DDL.sql`.
""",

    "23_SUPPORT_HANDOVER_CHECKLIST.md": """# Support Handover Checklist

- [x] Runnable console CLI
- [x] 27 output deliverables generated
- [x] Test suite passing
- [x] Documentation complete
""",

    "24_FAQ_AND_GLOSSARY.md": """# FAQ & Glossary

- **Grain**: The fundamental atomic level of data in a fact table.
- **Conformed Dimension**: A dimension that means the exact same thing across multiple fact tables.
- **SCD**: Slowly Changing Dimension.
""",

    "25_LIMITATIONS_AND_ROADMAP.md": """# Limitations & Future Roadmap

- **Current MVP**: CLI only, local file inputs, SQLite/PostgreSQL/Snowflake/BigQuery/Synapse DDL.
- **Future Enhancements**: Cloud object store connectors, automated dbt project scaffolding.
"""
}

def build_kt():
    kt_dir = "./knowledge-transfer"
    os.makedirs(kt_dir, exist_ok=True)
    os.makedirs(os.path.join(kt_dir, "diagrams"), exist_ok=True)
    os.makedirs(os.path.join(kt_dir, "examples"), exist_ok=True)

    for fname, content in KT_FILES.items():
        with open(os.path.join(kt_dir, fname), "w") as f:
            f.write(content)

    # Diagrams
    with open(os.path.join(kt_dir, "diagrams", "system_context.mmd"), "w") as f:
        f.write("graph TD\n    Inputs --> DW_Agent\n    DW_Agent --> Deliverables\n")

    # Examples
    with open(os.path.join(kt_dir, "examples", "sample_agent_config.yaml"), "w") as f:
        f.write("default_dialect: sqlite\n")

    print(f"Knowledge Transfer package built at {kt_dir}")

if __name__ == "__main__":
    build_kt()
