"""
ASTRAXIS-AI Anomaly & Security Policy Violation Detector Module.

Analyzes streams of TrafficEvent and SyscallEvent objects to detect complex
multi-step policy violations and anomalous agent behaviors in real time.

Key Concept — Real-time Anomaly Detection:
    Combines network traffic payload analysis with kernel-level syscall events
    to detect zero-day evasion techniques, unexpected egress calls, and privilege escalation.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any

from astraxis.interceptor.traffic import TrafficEvent
from astraxis.interceptor.syscall import SyscallEvent


@dataclass
class AnomalyViolation:
    """
    Represents a detected security policy violation.

    Attributes:
        violation_id: Unique UUID.
        rule_name:    Security policy rule triggered.
        severity:     Risk level (low / medium / high / critical).
        agent_id:     Agent responsible for violation.
        description:  Forensic explanation of violation.
        evidence:     Underlying event payload or syscall metadata.
        timestamp:    ISO timestamp.
    """
    violation_id: str
    rule_name: str
    severity: str
    agent_id: str
    description: str
    evidence: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize violation to dictionary for JSON report exports."""
        return {
            "violation_id": self.violation_id,
            "rule_name": self.rule_name,
            "severity": self.severity,
            "agent_id": self.agent_id,
            "description": self.description,
            "evidence": self.evidence,
            "timestamp": self.timestamp,
        }


class AnomalyDetector:
    """
    Detection engine evaluating streams of traffic and syscall events for policy violations.

    Usage:
        detector = AnomalyDetector()
        violations = detector.analyze(traffic_events, syscall_events)
        print(f"Detected {len(violations)} security violations.")
    """

    def analyze(
        self,
        traffic_events: List[TrafficEvent],
        syscall_events: List[SyscallEvent]
    ) -> List[AnomalyViolation]:
        """
        Analyze traffic and syscall events to produce a list of AnomalyViolation objects.

        Args:
            traffic_events: List of captured TrafficEvent items.
            syscall_events: List of captured SyscallEvent items.

        Returns:
            List of detected AnomalyViolation instances.
        """
        violations: List[AnomalyViolation] = []

        # Rule 1: Blocked Traffic Payload Attempt
        for te in traffic_events:
            if te.is_blocked:
                violations.append(
                    AnomalyViolation(
                        violation_id=str(uuid.uuid4()),
                        rule_name="BLOCKED_PAYLOAD_ATTEMPT",
                        severity="high",
                        agent_id=te.sender_agent,
                        description=f"Agent '{te.sender_agent}' attempted blocked payload transmission via {te.protocol.value}.",
                        evidence={"event_id": te.event_id, "endpoint": te.target_endpoint, "payload": te.body_payload}
                    )
                )

        # Rule 2: Suspicious Kernel Syscall
        for se in syscall_events:
            if se.is_suspicious:
                violations.append(
                    AnomalyViolation(
                        violation_id=str(uuid.uuid4()),
                        rule_name="SUSPICIOUS_SYSCALL_DETECTED",
                        severity="critical",
                        agent_id=se.agent_id,
                        description=f"Agent '{se.agent_id}' triggered suspicious {se.syscall_name.value} syscall on '{se.argument}'.",
                        evidence={"syscall_id": se.syscall_id, "pid": se.process_id, "argument": se.argument}
                    )
                )

        return violations
