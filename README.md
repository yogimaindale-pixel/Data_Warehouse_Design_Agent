# Data Warehouse Design Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Console Only](https://img.shields.io/badge/UI-Console%20Only-black.svg)]()

A deterministic, command-line Python agent that inspects business requirements, source DDLs, metadata, and sample data to automatically generate governed, production-grade Data Warehouse design packages.

It applies Ralph Kimball dimensional-modeling rules to determine business processes, grain declarations, conformed dimensions, fact tables, slowly changing dimension (SCD) policies, enterprise bus matrix, target DDLs, Source-to-Target Mappings (STTM), data quality rules, data lineage, test cases, and review documentation.

---

## 🌟 Key Features

- **100% Console-Based Interface**: Pure Python command-line execution (`python -m dw_agent`). No web frontends or graphical dependencies required.
- **Deterministic Modeling Rules**: All modeling decisions (grain, keys, SCD types, relationship validation) use explicit, auditable rules.
- **Multi-Dialect DDL Generation**: Supports **SQLite**, **PostgreSQL**, **Snowflake**, **BigQuery**, and **Azure Synapse**.
- **Comprehensive Deliverable Suite**: Generates 27 standardized deliverables under `output/`, including CSVs, Excel workbooks, Mermaid diagrams, SQL DDLs, and Markdown reports.
- **Quality Gates & Validation Engine**: Automatically flags and blocks critical modeling defects (e.g. unstated grains, missing SCD2 validity columns, STTM-to-DDL schema drift).

---

## 📁 Repository Structure

```text
.
├── README.md                                  # Main repository documentation
├── pyproject.toml                             # Package build specification
├── requirements.txt                           # Python dependencies
├── .env.example                               # Environment variable templates
├── .gitignore                                 # Git ignore patterns
├── Makefile                                   # Command shortcuts
├── run_demo.py                                # Root demo launcher
├── config/                                    # Configuration profiles & modeling rules
│   ├── agent.yaml
│   ├── naming_standards.yaml
│   ├── modeling_rules.yaml
│   ├── type_mapping.yaml
│   ├── dq_defaults.yaml
│   └── platform_profiles/                     # Dialect adapters (sqlite, postgresql, snowflake, bigquery, synapse)
├── docs/
│   └── assumptions.md                         # Discovered gaps & architectural assumptions
├── src/dw_agent/                              # Core Python Package
│   ├── __init__.py
│   ├── __main__.py                            # Entry point for python -m dw_agent
│   ├── cli.py                                 # Command line parser
│   ├── config.py                              # Configuration loader
│   ├── contracts.py                           # Dataclasses & typed contracts
│   ├── discovery/                             # Input parsers (DDL, metadata, requirements)
│   ├── profiling/                             # Sample data profiler
│   ├── modeling/                              # Dimensional modeling rules engine
│   ├── generation/                            # Deliverable exporter & dialect DDL generator
│   ├── validation/                            # Quality gates & SQLite dry-runner
│   └── reporting/                             # Executive summary & review pack
├── knowledge-transfer/                        # Full 26-document Knowledge Transfer package
│   ├── 00_KT_INDEX.md
│   ├── ...
│   ├── diagrams/
│   └── examples/
├── scripts/                                   # Automation & seed scripts
│   ├── bootstrap.sh
│   ├── run_tests.sh
│   ├── seed_demo.py
│   ├── build_kt_package.py
│   └── package_deliverables.py
└── tests/                                     # Test Suite (Unit, Integration, Scenario)
    ├── unit/
    ├── integration/
    └── scenarios/
```

---

## 🚀 Quick Start Guide

### 1. Installation & Environment Setup

Clone the repository and run bootstrap:

```bash
# Initialize virtual environment and install dependencies
make bootstrap

# Or manually:
python3 -m venv venv
./venv/bin/pip install -e .
```

### 2. Running Demonstration Scenarios

Run the out-of-the-box seeded demonstrations:

```bash
# E-commerce order-line star schema scenario
python3 run_demo.py ecommerce

# BFS credit-risk periodic snapshot scenario
python3 run_demo.py bfs-credit-risk
```

Outputs will be generated under `./demo_ecommerce/output/` and `./demo_bfs_credit_risk/output/`.

---

## 💻 Console Command Reference

The DW Design Agent provides a clean suite of terminal commands:

| Command | Usage | Description |
|---|---|---|
| `init` | `python -m dw_agent init --project <path>` | Scaffold input directory structure |
| `inspect` | `python -m dw_agent inspect --project <path>` | Scan and hash project input files |
| `profile` | `python -m dw_agent profile --project <path>` | Profile sample CSV/SQLite data |
| `design` | `python -m dw_agent design --project <path> --dialect <dialect>` | Execute design pipeline and write outputs |
| `validate` | `python -m dw_agent validate --project <path>` | Evaluate quality gates and SQLite dry-run |
| `explain` | `python -m dw_agent explain --artifact bus-matrix` | Explain an artifact or modeling decision rule |
| `diff` | `python -m dw_agent diff --baseline <path1> --candidate <path2>` | Compare baseline and candidate project output packages |
| `demo` | `python -m dw_agent demo --scenario ecommerce` | Run seeded demonstration |
| `clean` | `python -m dw_agent clean --project <path>` | Remove generated output files |

---

## 📦 Generated Deliverables Package (`output/`)

Upon running `design` or `demo`, the agent populates the `output/` directory with 27 implementation-ready deliverables:

1. `00_EXECUTIVE_SUMMARY.md`
2. `01_INPUT_INVENTORY.csv`
3. `02_REQUIREMENTS_CATALOG.csv`
4. `03_OPEN_QUESTIONS_AND_ASSUMPTIONS.md`
5. `04_SOURCE_PROFILE.xlsx`
6. `05_BUSINESS_PROCESS_CATALOG.csv`
7. `06_GRAIN_DECLARATIONS.md`
8. `07_BUS_MATRIX.csv`
9. `08_DIMENSION_CATALOG.xlsx`
10. `09_FACT_CATALOG.xlsx`
11. `10_CONCEPTUAL_MODEL.mmd`
12. `11_LOGICAL_MODEL.mmd`
13. `12_PHYSICAL_MODEL.mmd`
14. `13_TARGET_DDL.sql`
15. `14_ROLLBACK_DDL.sql`
16. `15_STTM.xlsx`
17. `16_ETL_SPECIFICATIONS.md`
18. `17_DATA_QUALITY_RULES.xlsx`
19. `18_LINEAGE.csv`
20. `19_SECURITY_AND_PRIVACY_CONSIDERATIONS.md`
21. `20_PERFORMANCE_DESIGN.md`
22. `21_TEST_CASES.xlsx`
23. `22_REQUIREMENTS_TRACEABILITY_MATRIX.xlsx`
24. `23_ARCHITECTURE_DECISIONS.md`
25. `24_MODEL_VALIDATION_REPORT.md`
26. `25_IMPLEMENTATION_BACKLOG.csv`
27. `26_REVIEW_CHECKLIST.md`

---

## 🧪 Testing

Execute the comprehensive test suite:

```bash
# Run unit, integration, and scenario tests
make test

# Or via pytest:
PYTHONPATH=src:. ./venv/bin/pytest tests/ -v
```

---

## 📚 Knowledge Transfer & Documentation

Full step-by-step Knowledge Transfer documentation is available in the [`knowledge-transfer/`](file:///config/Desktop/Session3/knowledge-transfer/) folder, covering architecture, command reference, operations runbook, troubleshooting guide, security, and extension guides.

---

## 📄 License

This project is licensed under the MIT License.
