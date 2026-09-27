"""Decision and evidence tracker."""

import datetime
from typing import List
from dw_agent.contracts import DecisionRecord

class EvidenceTracker:
    def __init__(self):
        self.decisions: List[DecisionRecord] = []

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
        self.decisions.append(record)
        return record
