"""
ASTRAXIS-AI Attack Graph Node Specifications.

Defines node types and models representing architectural components
in an AI agent network (Agents, Tools, Databases, Credentials, Endpoints).

Key Concept — Graph Nodes in Red-Teaming:
    In graph theory, a node (or vertex) represents an entity.
    In ASTRAXIS-AI attack graphs:
    - USER_INTERFACE: The entry point where user prompts enter (e.g. web chat UI).
    - AGENT: An AI decision engine (e.g. DataFetcher, Supervisor, CodeRunner).
    - TOOL: An executable function accessible by an agent (e.g. bash_exec, sql_query).
    - DATABASE: Data storage containing sensitive assets (e.g. PostgreSQL, Redis).
    - CREDENTIAL: High-value access keys or tokens (e.g. AWS_SECRET_KEY, DB_PASSWORD).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any


class NodeType(str, Enum):
    """Taxonomy of node types in an AI agent architecture attack graph."""
    USER_INTERFACE = "user_interface"
    AGENT = "agent"
    TOOL = "tool"
    DATABASE = "database"
    CREDENTIAL = "credential"
    EXTERNAL_API = "external_api"


@dataclass
class GraphNode:
    """
    Represents a single node in the attack graph.

    Attributes:
        node_id:     Unique identifier (e.g., "agent_supervisor", "tool_bash").
        label:       Human-readable display name for visual dashboards.
        node_type:   Type classification from NodeType enum.
        is_target:   True if this node represents a high-value security asset.
        is_entry:    True if this node is an untrusted entry point for user input.
        metadata:    Arbitrary component details (e.g., permissions, OS, model_name).
    """
    node_id: str
    label: str
    node_type: NodeType
    is_target: bool = False
    is_entry: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize node to a dictionary for JSON exports and graph visualizations."""
        return {
            "node_id": self.node_id,
            "label": self.label,
            "node_type": self.node_type.value if isinstance(self.node_type, Enum) else self.node_type,
            "is_target": self.is_target,
            "is_entry": self.is_entry,
            "metadata": self.metadata,
        }
