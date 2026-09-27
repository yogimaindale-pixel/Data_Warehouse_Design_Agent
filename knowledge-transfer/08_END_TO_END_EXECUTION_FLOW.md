# End-to-End Execution Flow

1. Scan input files and compute SHA256 hashes.
2. Parse business requirements and source DDLs.
3. Profile sample data for row count, null %, distinct values, PII candidates.
4. Identify business processes and declare single-sentence grains.
5. Design conformed dimensions and fact tables.
6. Build Enterprise Bus Matrix.
7. Generate DDL, STTM, ETL specs, DQ rules, Lineage, and Mermaid models.
8. Validate design against quality gates and execute dry-run SQL in SQLite.
