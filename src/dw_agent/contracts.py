# Module docstring explaining core dataclasses and contracts for Data Warehouse Design Agent
"""Typed dataclasses and contracts defining data models across discovery, modeling, validation, and generation."""

# Import dataclass decorator and field utility from standard dataclasses library
from dataclasses import dataclass, field
# Import List, Dict, Any, and Optional type hinting primitives
from typing import List, Dict, Any, Optional

# Dataclass tracking scanned input file metadata in project inventory
@dataclass
class InputFile:
    """Represents a single discovered input artifact file within the project folder."""
    file_path: str   # Relative file path within the project inventory
    file_type: str   # File classification (e.g. 'ddl', 'csv', 'markdown', 'yaml')
    file_hash: str   # SHA-256 checksum for tracking file changes and integrity
    size_bytes: int  # Total file size in bytes

# Dataclass capturing parsed business requirements and KPI definitions
@dataclass
class Requirement:
    """Represents a business requirement or KPI target parsed from input documents."""
    req_id: str             # Unique requirement identifier (e.g. 'REQ-001')
    title: str              # Short requirement headline or KPI title
    description: str        # Detailed text description of requirement
    source_file: str        # Source specification document filename
    category: str = "KPI"   # Requirement category: 'KPI', 'Dimension', 'Filter', 'Security', 'Refresh', 'History'

# Dataclass representing a column within a source database schema table
@dataclass
class SourceColumn:
    """Represents an attribute column parsed from source DDL or metadata catalog."""
    name: str                           # Column name in source database
    data_type: str                      # Source data type (e.g., 'VARCHAR(50)', 'INT')
    is_pk: bool = False                 # Flag indicating if column is part of Primary Key
    is_fk: bool = False                 # Flag indicating if column is a Foreign Key
    fk_target_table: Optional[str] = None # Foreign Key target table name if is_fk is True
    fk_target_column: Optional[str] = None # Foreign Key target column name if is_fk is True
    is_nullable: bool = True            # Flag indicating if column allows NULL values
    is_pii_candidate: bool = False      # Flag indicating if column contains Personally Identifiable Information

# Dataclass representing a table within a source system schema
@dataclass
class SourceTable:
    """Represents a source database table and its parsed columns and metadata."""
    name: str                                           # Table name in source database
    columns: List[SourceColumn] = field(default_factory=list) # List of SourceColumn objects
    system: str = "source"                              # Source system identifier
    row_count: int = 0                                  # Total row count in source dataset

# Dataclass storing data profiling results for a source table
@dataclass
class ProfileResult:
    """Captures statistical data profiling metrics computed over sample data files."""
    table_name: str                                             # Source table name
    row_count: int                                              # Profiled row count
    columns: Dict[str, Dict[str, Any]] = field(default_factory=dict) # Per-column profiling metrics (distinct count, null pct)
    candidate_natural_keys: List[str] = field(default_factory=list) # Candidate unique natural keys identified
    pii_columns: List[str] = field(default_factory=list)            # List of columns flagged as potential PII

# Dataclass representing a discovered business process
@dataclass
class BusinessProcess:
    """Defines an operational business event process suitable for dimensional modeling."""
    process_id: str                                         # Unique process identifier (e.g. 'PROC-001')
    name: str                                               # Business process name (e.g. 'Orders')
    triggering_event: str                                   # Event that triggers the process (e.g. 'Customer submits order')
    business_questions: List[str] = field(default_factory=list) # Analytical business questions answered
    kpis: List[str] = field(default_factory=list)           # List of associated KPI metrics
    source_tables: List[str] = field(default_factory=list)   # Source tables driving this process
    proposed_fact_type: str = "transaction"                 # Proposed fact table type ('transaction', 'snapshot', 'factless')

# Dataclass declaring the atomic grain of a fact table
@dataclass
class GrainDeclaration:
    """Represents a single-sentence grain declaration for a warehouse fact table."""
    process_id: str                                     # Parent business process ID
    fact_table_name: str                                # Target fact table name (e.g. 'fact_sales')
    grain_sentence: str                                 # Formal grain sentence (e.g. 'One row per order line item')
    business_keys: List[str] = field(default_factory=list) # Key components establishing grain uniqueness
    is_unique: bool = True                              # Verification status of key uniqueness in sample data

# Dataclass representing an attribute column in a target dimension table
@dataclass
class DimensionColumn:
    """Defines an attribute column within a target warehouse dimension table."""
    name: str               # Target dimension column name
    data_type: str          # Target database data type
    scd_type: int = 1       # Slowly Changing Dimension policy: 0=fixed, 1=overwrite, 2=historical, 3=current/prev
    source_mapping: str = "" # Source table and column mapping expression
    description: str = ""   # Business definition of dimension attribute

# Dataclass representing a target dimension table specification
@dataclass
class DimensionSpec:
    """Specification for a target warehouse dimension table."""
    table_name: str                                             # Dimension table name (e.g. 'dim_customer')
    grain: str                                                  # Grain declaration sentence for dimension
    surrogate_key: str                                          # Primary surrogate key column name (e.g. 'customer_key')
    business_key: str                                           # Natural business key column name (e.g. 'customer_id')
    columns: List[DimensionColumn] = field(default_factory=list) # List of dimension attributes
    dim_type: str = "conformed"                                 # Dimension type: 'conformed', 'role-playing', 'junk', 'bridge'
    is_scd2: bool = False                                       # Flag indicating if dimension uses SCD Type 2 validity tracking

# Dataclass defining a numerical measure in a fact table
@dataclass
class FactMeasure:
    """Defines a numerical measure metric within a target warehouse fact table."""
    name: str               # Target measure column name (e.g. 'net_amount')
    formula: str            # Calculation formula or source mapping
    source_column: str      # Source column feeding this measure
    additivity: str = "additive" # Additivity behavior: 'additive', 'semi-additive', 'non-additive'
    agg_guidance: str = "SUM" # Default aggregation function guidance

# Dataclass representing a target fact table specification
@dataclass
class FactSpec:
    """Specification for a target warehouse fact table."""
    table_name: str                                                 # Fact table name (e.g. 'fact_sales')
    process_id: str                                                 # Parent business process ID
    grain_sentence: str                                             # Grain declaration text
    fact_type: str                                                  # Fact type: 'transaction', 'snapshot', 'factless'
    foreign_keys: List[Dict[str, str]] = field(default_factory=list) # Foreign key list [{col, target_dim}]
    degenerate_dimensions: List[str] = field(default_factory=list)  # Degenerate dimension keys retained on fact table
    measures: List[FactMeasure] = field(default_factory=list)       # List of numerical measures

# Dataclass representing a row in the Enterprise Bus Matrix
@dataclass
class BusMatrixRow:
    """Represents one row in the Enterprise Bus Matrix mapping a process to conformed dimensions."""
    process_name: str                                   # Business process name
    process_id: str                                     # Business process ID
    fact_type: str                                      # Fact table type
    dimensions: Dict[str, str] = field(default_factory=dict) # Map of dimension_name -> "Y" or role name

# Dataclass defining a Source-to-Target Mapping (STTM) entry
@dataclass
class STTMRow:
    """Represents a detailed column mapping row in Source-to-Target Mappings."""
    mapping_id: str         # Unique STTM row identifier
    target_table: str       # Target warehouse table name
    target_column: str      # Target warehouse column name
    source_system: str      # Source system name
    source_table: str       # Source table name
    source_column: str      # Source column name
    transformation: str     # Transformation logic or expression
    lookup_rule: str        # Surrogate key lookup logic
    default_rule: str       # Default fallback rule for missing values
    rejection_behavior: str # Rejection behavior if lookup or parsing fails
    dq_rule_ids: str        # Associated Data Quality rule IDs
    scd_behavior: str       # SCD behavior code
    req_id: str             # Associated requirement ID

# Dataclass defining an automated Data Quality control rule
@dataclass
class DQRule:
    """Defines an automated Data Quality check rule for validation during ETL execution."""
    rule_id: str        # Unique DQ rule identifier (e.g. 'DQ-NULL-001')
    category: str       # DQ category: 'uniqueness', 'referential', 'null_check', 'range'
    target_table: str   # Target warehouse table
    target_column: str  # Target column evaluated
    condition: str      # SQL validation condition expression
    severity: str       # Severity level: 'critical', 'warning'
    threshold: str      # Tolerance threshold (e.g. '0% nulls')
    action: str         # Failure action: 'quarantine', 'alert', 'block'

# Dataclass capturing an architectural decision record (ADR)
@dataclass
class DecisionRecord:
    """Records an architectural design decision with timestamp, status, and evidence pointers."""
    decision_id: str            # Decision ID (e.g. 'DEC-001')
    rule_id: str                # Rule ID evaluated
    rule_version: int           # Rule version number
    evidence_refs: List[str]    # Pointers to evidence supporting decision
    artifact_refs: List[str]    # Affected artifact file paths
    status: str                 # Decision status: 'proposed', 'accepted', 'rejected'
    reviewer: str = "agent"     # System or human reviewer
    timestamp: str = ""         # ISO UTC timestamp

# Dataclass capturing a validation check result
@dataclass
class ValidationItem:
    """Captures the pass/fail outcome of a quality gate architectural validation rule."""
    rule_id: str        # Evaluated rule ID (e.g. 'GRAIN-001')
    category: str       # Validation category
    severity: str       # Severity level: 'critical', 'warning', 'info'
    message: str        # Human-readable result message
    is_pass: bool       # Flag indicating pass (True) or failure (False)
    action: str = "none" # Recommended corrective action if rule fails

