"""
ASTRAXIS-AI Attack Graph Edge Specifications.

Defines directed edge relationships between architectural components
(e.g., Agent -> Calls Tool -> Exfiltrates Data -> Credential Store).

Key Concept — Directed Edges & Threat Propagation:
    An edge (A -> B) means data or control flows from component A to component B.
    If A is compromised by prompt injection, the attack can propagate to B.
    Edges carry weights (0.0 to 1.0) representing attack feasibility / probability.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any


class EdgeType(str, Enum):
    """Taxonomy of relationship edge types between graph nodes."""
    CALLS_TOOL = "calls_tool"
    PASSES_MESSAGE = "passes_message"
    READS_DATA = "reads_data"
    WRITES_DATA = "writes_data"
    EXPLOITS = "exploits"
    ACCESSES_CREDENTIAL = "accesses_credential"


@dataclass
class GraphEdge:
    """
    Represents a directed connection between two nodes in the attack graph.

    Attributes:
        source_id:   Originating node ID (e.g. "agent_web_scraper").
        target_id:   Destination node ID (e.g. "tool_file_writer").
        edge_type:   Type classification from EdgeType enum.
        weight:      Risk factor or exploit probability (0.1 = hard, 1.0 = automatic).
        description: Description of the relationship or vulnerability vector.
        metadata:    Additional metadata.
    """
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 1.0
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize edge to dictionary for JSON exports and NetworkX ingestion."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type.value if isinstance(self.edge_type, Enum) else self.edge_type,
            "weight": self.weight,
            "description": self.description,
            "metadata": self.metadata,
        }
