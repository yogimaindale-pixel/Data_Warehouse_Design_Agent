# Repository Structure Walkthrough

- `src/dw_agent/cli.py`: Command line interface.
- `src/dw_agent/discovery/`: Parsers for requirements, DDLs, metadata.
- `src/dw_agent/profiling/`: Profiler for CSV and SQLite sample data.
- `src/dw_agent/modeling/`: Dimensional design logic (grain, facts, dims, SCD, bus matrix).
- `src/dw_agent/generation/`: Deliverable generators (DDL, STTM, ETL, DQ, Lineage, Mermaid).
- `src/dw_agent/validation/`: Quality gates and model acceptance.
