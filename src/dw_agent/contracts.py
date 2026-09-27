"""Typed dataclasses and contracts for Data Warehouse Design Agent."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class InputFile:
    file_path: str
    file_type: str
    file_hash: str
    size_bytes: int

@dataclass
class Requirement:
    req_id: str
    title: str
    description: str
    source_file: str
    category: str = "KPI"  # KPI, Dimension, Filter, Security, Refresh, History

@dataclass
class SourceColumn:
    name: str
    data_type: str
    is_pk: bool = False
    is_fk: bool = False
    fk_target_table: Optional[str] = None
    fk_target_column: Optional[str] = None
    is_nullable: bool = True
    is_pii_candidate: bool = False

@dataclass
class SourceTable:
    name: str
    columns: List[SourceColumn] = field(default_factory=list)
    system: str = "source"
    row_count: int = 0

@dataclass
class ProfileResult:
    table_name: str
    row_count: int
    columns: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    candidate_natural_keys: List[str] = field(default_factory=list)
    pii_columns: List[str] = field(default_factory=list)

@dataclass
class BusinessProcess:
    process_id: str
    name: str
    triggering_event: str
    business_questions: List[str] = field(default_factory=list)
    kpis: List[str] = field(default_factory=list)
    source_tables: List[str] = field(default_factory=list)
    proposed_fact_type: str = "transaction"

@dataclass
class GrainDeclaration:
    process_id: str
    fact_table_name: str
    grain_sentence: str
    business_keys: List[str] = field(default_factory=list)
    is_unique: bool = True

@dataclass
class DimensionColumn:
    name: str
    data_type: str
    scd_type: int = 1  # 0, 1, 2, 3
    source_mapping: str = ""
    description: str = ""

@dataclass
class DimensionSpec:
    table_name: str
    grain: str
    surrogate_key: str
    business_key: str
    columns: List[DimensionColumn] = field(default_factory=list)
    dim_type: str = "conformed"  # conformed, role-playing, degenerate, junk, mini, bridge
    is_scd2: bool = False

@dataclass
class FactMeasure:
    name: str
    formula: str
    source_column: str
    additivity: str = "additive"  # additive, semi-additive, non-additive
    agg_guidance: str = "SUM"

@dataclass
class FactSpec:
    table_name: str
    process_id: str
    grain_sentence: str
    fact_type: str  # transaction, periodic_snapshot, accumulating_snapshot, factless
    foreign_keys: List[Dict[str, str]] = field(default_factory=list)  # {col, target_dim}
    degenerate_dimensions: List[str] = field(default_factory=list)
    measures: List[FactMeasure] = field(default_factory=list)

@dataclass
class BusMatrixRow:
    process_name: str
    process_id: str
    fact_type: str
    dimensions: Dict[str, str] = field(default_factory=dict)  # dim_name -> "Y" or role name

@dataclass
class STTMRow:
    mapping_id: str
    target_table: str
    target_column: str
    source_system: str
    source_table: str
    source_column: str
    transformation: str
    lookup_rule: str
    default_rule: str
    rejection_behavior: str
    dq_rule_ids: str
    scd_behavior: str
    req_id: str

@dataclass
class DQRule:
    rule_id: str
    category: str
    target_table: str
    target_column: str
    condition: str
    severity: str  # critical, warning
    threshold: str
    action: str

@dataclass
class DecisionRecord:
    decision_id: str
    rule_id: str
    rule_version: int
    evidence_refs: List[str]
    artifact_refs: List[str]
    status: str  # proposed, accepted, rejected, superseded
    reviewer: str = "agent"
    timestamp: str = ""

@dataclass
class ValidationItem:
    rule_id: str
    category: str
    severity: str  # critical, warning, info
    message: str
    is_pass: bool
    action: str = "none"
