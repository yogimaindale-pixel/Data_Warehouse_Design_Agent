# BlueBolt Idea Details: Data Warehouse Design Agent

> Draft portal-ready content. Replace bracketed placeholders and validate benefits with the BlueBolt Champion, project manager, finance, and relevant stakeholders before submission. Do not enter sensitive client data.

## 1. Idea Title

**Data Warehouse Design Agent: Python-Based Automated Dimensional Modeling and Engineering Deliverable Generator**

## 2. Theme

**Automation, Productivity Improvement, Data Engineering, Quality and Governance**

## 3. Elevator Pitch

A command-line Python agent that converts business requirements, source DDL, metadata, KPI inventories, and safe sample data into a governed data warehouse design package. It applies deterministic dimensional-modeling rules and generates grain declarations, business-process catalog, enterprise bus matrix, fact and dimension specifications, SCD policies, physical DDL, source-to-target mappings, ETL specifications, data-quality rules, lineage, test cases, traceability, and review reports.

## 4. Problem Statement

Data warehouse design commonly requires repeated manual analysis across business requirements, source structures, data profiles, reports, KPIs, naming standards, and platform constraints. Important decisions such as business-process scope, fact-table grain, conformed dimensions, measure additivity, slowly changing dimension policy, source-to-target mapping, and data-quality controls are often documented in separate artifacts. This can create inconsistent designs, missed dependencies, weak requirements traceability, duplicated effort, and longer review cycles.

A reusable approach is required to automate evidence collection and standard deliverable generation while retaining explicit human review for ambiguous business decisions.

## 5. Business Scenario

The idea can support greenfield data warehouses, new data marts, cloud modernization, lakehouse Gold-layer design, regulatory-reporting models, and redesign of existing analytical schemas. A data architect or engineer places approved requirements and source metadata in a project folder and runs the Python console agent. The agent analyzes available evidence, proposes a dimensional model, identifies gaps, generates implementation artifacts, and blocks completion when critical design checks fail.

## 6. Proposed Solution

Build a modular Python application with a console interface and deterministic rules engine.

### Core workflow

1. Discover requirements, source DDL, metadata, KPI definitions, and sample data.
2. Profile local data and identify candidate keys, relationships, quality issues, and source constraints.
3. Identify measurable business processes.
4. Declare the grain for every proposed fact table.
5. Design conformed dimensions, role-playing dimensions, bridges, facts, and SCD policies.
6. Generate an enterprise bus matrix.
7. Generate platform-aware DDL, STTM, ETL specifications, DQ rules, lineage, test cases, ADRs, and traceability.
8. Validate the model using deterministic quality gates.
9. Package deliverables for architect, ETL, testing, BI, and governance review.

### Console-only design

The minimum viable product has no frontend. It runs through commands such as:

```bash
python -m dw_agent inspect --project ./sample_project
python -m dw_agent profile --project ./sample_project
python -m dw_agent design --project ./sample_project --dialect postgresql
python -m dw_agent validate --project ./sample_project
python -m dw_agent report --project ./sample_project
```

## 7. High-Level Architecture

```text
Requirements / KPI Inventory / Source DDL / Metadata / Sample Data
                              |
                              v
                    Python Console Interface
                              |
                              v
      Discovery -> Profiling -> Deterministic Modeling Rules
                              |
                  Business Process and Grain
                              |
          Dimensions / Facts / SCD / Bus Matrix
                              |
        DDL / STTM / ETL / DQ / Lineage / Tests
                              |
                 Validation and Review Gate
                              |
                    Deliverable Package
```

## 8. Key Features

- Python command-line execution with no web interface
- configuration-driven deterministic rules
- source DDL and metadata inspection
- safe local data profiling
- candidate key and relationship discovery
- business-process and grain definition
- transaction, periodic snapshot, accumulating snapshot, and factless fact support
- conformed, role-playing, degenerate, junk, mini-dimension, and bridge patterns
- SCD Types 0, 1, 2, and 3
- measure additivity classification
- enterprise bus matrix
- multi-dialect DDL generation
- STTM and ETL specification generation
- data-quality and reconciliation rule generation
- lineage and requirements traceability
- architecture decision records
- model-quality gates
- deterministic demos and automated tests
- complete knowledge-transfer package

## 9. Uniqueness and Innovativeness

The proposal combines data profiling, dimensional-modeling governance, engineering artifact generation, and validation in one console-based workflow. The differentiator is not simply generating SQL. It preserves a traceable chain from requirement and source evidence to grain, model, mapping, validation rule, and test case. It also treats unresolved business decisions as review items rather than silently inventing answers.

The solution is reusable across industries because business rules, naming conventions, data types, modeling checks, and SQL dialects are externalized through configuration and adapters.

## 10. Target Users

- data architects
- data modelers
- data engineers
- ETL developers
- BI developers
- data-quality engineers
- testers
- governance reviewers
- junior engineers learning warehouse design

## 11. Proposed MVP Scope

### In scope

- Python CLI
- Markdown, SQL, CSV, JSON, YAML, SQLite, and safe local sample inputs
- deterministic modeling and validation
- e-commerce demo
- BFS credit-risk demo
- SQLite and PostgreSQL DDL adapters for the first MVP
- complete design deliverable package
- tests and KT documentation

### Out of scope for the first MVP

- graphical frontend
- autonomous production deployment
- unrestricted database execution
- proprietary modeling-tool integration
- automatic approval of business definitions
- automatic use of sensitive production datasets
- ungoverned LLM-based design decisions

## 12. Expected Deliverables

- working Python console application
- source code and configuration
- seeded demonstrations
- business-process catalog
- grain declarations
- enterprise bus matrix
- fact and dimension catalogs
- conceptual, logical, and physical Mermaid models
- DDL and rollback DDL
- STTM workbook
- ETL design specification
- DQ rule catalog
- lineage report
- requirements traceability matrix
- test cases and validation report
- operations and security documentation
- knowledge-transfer package
- demonstration script and evidence

## 13. Implementation Approach

### Phase 1: Discovery and standards
Collect approved requirements, source metadata, modeling standards, expected deliverables, security constraints, and target-platform needs.

### Phase 2: Core Python framework
Build the CLI, configuration validation, evidence model, logging, error handling, and artifact manifest.

### Phase 3: Source discovery and profiling
Implement DDL parsing, metadata loading, local profiling, candidate-key analysis, relationship checks, and input-gap reporting.

### Phase 4: Dimensional design engine
Implement business-process, grain, fact, dimension, SCD, bridge, additivity, and conformance rules.

### Phase 5: Deliverable generation
Generate bus matrix, catalogs, diagrams, DDL, STTM, ETL, DQ, lineage, tests, ADRs, and traceability.

### Phase 6: Validation and demonstrations
Implement quality gates, scenario tests, deterministic output comparison, e-commerce demonstration, and BFS credit-risk demonstration.

### Phase 7: Handover and adoption
Complete setup, operating runbook, troubleshooting, extension guidance, KT, support checklist, and reusable project templates.

## 14. Suggested Milestones

Enter actual dates in the portal only after team and sponsor agreement.

| Milestone | Planned Evidence |
|---|---|
| Requirements and architecture baseline | Approved scope, assumptions, architecture, acceptance criteria |
| CLI and discovery complete | Runnable console commands and input inventory |
| Profiling and modeling complete | Profile, grains, facts, dimensions, SCD, bus matrix |
| Deliverable generation complete | DDL, STTM, ETL, DQ, lineage, traceability |
| Validation and demos complete | Test report, demo evidence, review findings |
| KT and handover complete | KT pack, runbook, support checklist, sign-off |

## 15. Benefits and Measurement Plan

Do not enter unvalidated percentages or dollar values. Establish a manual baseline and compare equivalent projects.

### Proposed benefit hypotheses

- reduced manual effort for initial profiling and draft modeling artifacts
- faster creation of DDL, STTM, DQ, test, and traceability documents
- improved consistency of grain, key, SCD, and naming decisions
- earlier detection of model defects
- improved reuse across projects and technology platforms
- faster onboarding through standardized KT artifacts
- improved governance and audit readiness

### Baseline measures

- hours spent preparing each deliverable manually
- elapsed time from requirements receipt to first model review
- number of review comments by defect category
- number of iterations before architecture approval
- percentage of requirements traced to model and tests
- number of design defects found after development begins

### Pilot measures

- hours spent with the agent plus human review
- deliverable completion rate
- validation pass, warning, and failure counts
- reviewer acceptance rate by artifact
- rework hours
- defect escape count
- number of reusable rules and templates

### Benefit formula examples

```text
Time saved = Manual baseline hours - Agent-assisted total hours
Effort saving percentage = Time saved / Manual baseline hours * 100
Annual soft-dollar benefit = Verified annual hours saved * Approved blended hourly rate
Defect avoidance = Baseline post-design defects - Pilot post-design defects
```

All values require review by the BlueBolt Champion and the appropriate financial or project approver.

## 16. BlueBolt Benefit Category Suggestions

Select only the category confirmed by the BlueBolt Champion:

- Client Cost Saving Soft Dollar
- Cognizant Cost Saving Soft Dollar
- Client Cost Saving Hard Dollar
- Cognizant Cost Saving Hard Dollar
- Client Revenue
- Cognizant Revenue

For an internal reusable accelerator without contracted savings, soft-dollar productivity is likely the first category to evaluate, but the final selection must be confirmed through governance.

## 17. Success Criteria

- clean console setup succeeds
- sample project runs without a frontend
- at least two domain demonstrations generate a complete design package
- critical grain and relationship defects are blocked
- generated DDL executes in a safe local database for the demo
- design artifacts trace back to requirements or documented assumptions
- repeated runs with identical inputs produce equivalent normalized outputs
- reviewer approves the usefulness of generated artifacts
- baseline and pilot evidence are retained

## 18. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Incomplete requirements | Generate open questions and block unsupported decisions |
| Incorrect inferred grain | Validate against source uniqueness and require human review |
| Poor or limited sample data | Label profile confidence and avoid treating samples as full truth |
| Platform-specific SQL differences | Isolate dialect adapters and run dialect tests |
| Sensitive data exposure | Use safe samples, masking, local processing, and artifact classification |
| Overreliance on generated design | Require architecture review and draft status |
| Duplicate existing accelerator | Perform KnowHub and account-level reuse review before claiming uniqueness |
| Unverified savings | Use baseline/pilot measurements and financial validation |
| Scope expansion | Keep MVP console-only and configuration-driven |

## 19. Responsible AI and Governance Position

The core MVP is deterministic. Optional AI can assist with explanations or draft summaries, but all architectural decisions remain rule-based, evidence-backed, and reviewable. Inputs and outputs must be moderated for sensitive information. Human approval remains mandatory for business definitions, security classifications, target-platform decisions, and production adoption.

## 20. Reusability and Scaling

Reusable elements include:

- input contracts
- modeling-rule library
- naming standards
- type mappings
- dimensional patterns
- SQL dialect adapters
- deliverable templates
- validation rules
- demonstration scenarios
- KT package

Future adapters may include Oracle, SQL Server, Snowflake, BigQuery, Synapse, Fabric Warehouse, and Databricks SQL, subject to project demand and governance.

## 21. Evidence to Attach for Implementation Submission

- source repository or approved internal location
- architecture and design document
- sample input package
- console execution transcript
- generated deliverables
- automated test report
- model validation report
- before-and-after effort baseline
- reviewer feedback or approval evidence
- benefit calculation with assumptions
- security and data-handling review
- demo recording or screenshots if permitted
- KT and operations package

## 22. Portal-Ready Short Description

**Develop a reusable Python command-line agent that automates evidence-based data warehouse design. The solution analyzes requirements, source DDL, metadata, KPI inventories, and safe sample data; applies deterministic dimensional-modeling rules; and generates grain declarations, fact and dimension models, SCD policies, a conformed-dimension bus matrix, target DDL, STTM, ETL specifications, data-quality rules, lineage, tests, and traceability. It improves consistency and accelerates design preparation while retaining human review for ambiguous or high-impact decisions.**

## 23. Portal-Ready Business Scenario

**Data warehouse teams repeatedly perform manual analysis and prepare separate modeling, mapping, DDL, quality, testing, and governance artifacts. This creates avoidable effort and can lead to inconsistent grain, key, SCD, and conformance decisions. The proposed console-based Python agent standardizes the workflow and generates a review-ready design package from approved project evidence.**

## 24. Portal-Ready Solution

**The agent scans a project input folder, profiles safe local data, identifies business processes, validates fact grain, designs dimensions and facts, assigns configurable SCD policies, builds the enterprise bus matrix, and generates implementation artifacts. A deterministic validation engine blocks critical issues such as mixed grains, fact-to-fact joins, missing business keys, invalid SCD2 periods, and STTM-to-DDL inconsistencies. The MVP runs entirely from the console and does not require a frontend.**

## 25. Portal Submission Checklist

- [ ] Confirm idea is not a duplicate of an existing account or KnowHub asset.
- [ ] Confirm project/customer/department fields.
- [ ] Confirm contributors.
- [ ] Remove all client-sensitive information.
- [ ] Validate problem statement, title, description, business scenario, solution, uniqueness, and benefits.
- [ ] Confirm whether existing assets are reused and record approved asset details.
- [ ] Agree planned milestones if proposal details are required.
- [ ] Select benefit metric with BlueBolt Champion.
- [ ] Enter only approved annualized benefit value.
- [ ] Retain evidence for calculations.
- [ ] Obtain stakeholder validation before implementation submission.
- [ ] Attach implementation deck and evidence when required.
- [ ] Complete actual milestones and benefit data after implementation.
- [ ] Select reviewers and approvers as advised by governance.
- [ ] Do not mark the idea implemented before required approval.
