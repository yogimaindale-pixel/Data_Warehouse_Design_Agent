# Line-by-Line Breakdown: src/dw_agent/cli.py

- **L1-L20**: Import system modules (`argparse`, `sys`, `pathlib`, `logging`) and core `dw_agent` components.
- **L62-L80**: Define `run_design_pipeline(input_dir, platform_profile)`. Initialize logging, load configuration profiles from `ConfigManager`, and resolve input paths.
- **L81-L110**: Stage 1 Discovery: Invoke `scan_input_inventory()`, `parse_requirements()`, and `parse_source_ddl()` to populate source tables.
- **L111-L140**: Stage 2 Profiling: Profile sample data, detect primary keys, candidate foreign keys, and candidate PII columns.
- **L141-L180**: Stage 3 Modeling: Identify business processes, formulate grain declarations, design conformed dimensions (`design_dimensions()`), facts (`design_facts()`), and SCD2 policies.
- **L181-L210**: Stage 4 Generation & Stage 5 Validation: Generate target DDLs, STTM workbooks, ERDs, validate warehouse model integrity, and export 27 deliverables via `export_all_deliverables()`.
- **L230-L420**: Define CLI argument parser handles `--input-dir`, `--platform`, `--validate-only`, and `--version`.
