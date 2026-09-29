# Module docstring explaining architectural decision record (ADR) and evidence tracking
"""Evidence Tracker module capturing architectural decisions, rule references, and evidence lineage."""

# Import datetime module for generating ISO-8601 UTC timestamps
import datetime
# Import List type hinting for typing decision records and reference lists
from typing import List
# Import DecisionRecord dataclass contract
from dw_agent.contracts import DecisionRecord

# EvidenceTracker class managing in-memory decision audit history
class EvidenceTracker:
    """Tracks architectural decisions made during modeling, linking rules, evidence, and deliverables."""

    # Constructor initializing empty decision records list
    def __init__(self):
        """Initialize EvidenceTracker with an empty decision list."""
        self.decisions: List[DecisionRecord] = []

    # Function recording a new architectural decision record
    def record_decision(
        self,
        decision_id: str,
        rule_id: str,
        evidence_refs: List[str],
        artifact_refs: List[str],
        status: str = "proposed",
        rule_version: int = 1,
        reviewer: str = "agent_rule_engine"
    ) -> DecisionRecord:
        """Record an architectural design decision with timestamp, status, and evidence pointers.

        Args:
            decision_id (str): Unique identifier for the decision (e.g., 'DEC-GRAIN-001').
            rule_id (str): Rule identifier triggering the decision (e.g., 'GRAIN-001').
            evidence_refs (List[str]): List of evidence pointers (e.g., source table names, requirements).
            artifact_refs (List[str]): List of generated artifact file paths affected by this decision.
            status (str): Decision status ('proposed', 'accepted', 'rejected', 'superseded').
            rule_version (int): Version of the rule evaluated.
            reviewer (str): System or human reviewer recording the decision.

        Returns:
            DecisionRecord: Created decision record instance.
        """
        # Construct typed DecisionRecord instance with current UTC timestamp
        record = DecisionRecord(
            decision_id=decision_id,
            rule_id=rule_id,
            rule_version=rule_version,
            evidence_refs=evidence_refs,
            artifact_refs=artifact_refs,
            status=status,
            reviewer=reviewer,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
        )
        # Append decision record to internal tracking history list
        self.decisions.append(record)
        return record

