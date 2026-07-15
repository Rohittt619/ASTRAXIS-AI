"""
ASTRAXIS-AI Attack Graph Builder.

Constructs NetworkX directed graphs (DiGraph) representing AI agent architectures,
their component tool dependencies, data paths, and potential exploit vectors.

Key Concept — NetworkX DiGraph:
    A NetworkX `DiGraph` (Directed Graph) holds nodes and directed edges with attributes.
    This allows algorithms like Dijkstra's shortest path, NetworkX centrality, and
    all-simple-paths graph traversal to find vulnerabilities instantly.
"""
from __future__ import annotations

from typing import Dict, List, Optional
import networkx as nx

from astraxis.graph.nodes import GraphNode, NodeType
from astraxis.graph.edges import GraphEdge, EdgeType


class AttackGraphBuilder:
    """
    Builder engine for creating, populating, and managing NetworkX attack graphs.

    Usage:
        builder = AttackGraphBuilder()

        # Add nodes
        builder.add_node(GraphNode(node_id="ui", label="Chat UI", node_type=NodeType.USER_INTERFACE, is_entry=True))
        builder.add_node(GraphNode(node_id="agent1", label="Planner Agent", node_type=NodeType.AGENT))
        builder.add_node(GraphNode(node_id="db", label="Prod DB", node_type=NodeType.DATABASE, is_target=True))

        # Add edge
        builder.add_edge(GraphEdge(source_id="ui", target_id="agent1", edge_type=EdgeType.PASSES_MESSAGE))

        # Or build a default synthetic architecture benchmark
        graph = builder.build_default_architecture()
    """

    def __init__(self) -> None:
        self._nx_graph = nx.DiGraph()
        self._nodes: Dict[str, GraphNode] = {}
        self._edges: List[GraphEdge] = []

    @property
    def graph(self) -> nx.DiGraph:
        """Return underlying NetworkX DiGraph instance."""
        return self._nx_graph

    def add_node(self, node: GraphNode) -> None:
        """Add a GraphNode to the network."""
        self._nodes[node.node_id] = node
        self._nx_graph.add_node(
            node.node_id,
            label=node.label,
            node_type=node.node_type.value if isinstance(node.node_type, NodeType) else node.node_type,
            is_target=node.is_target,
            is_entry=node.is_entry,
            obj=node
        )

    def add_edge(self, edge: GraphEdge) -> None:
        """Add a GraphEdge connecting source_id to target_id."""
        if edge.source_id not in self._nodes or edge.target_id not in self._nodes:
            raise ValueError(
                f"Cannot connect edge ({edge.source_id} -> {edge.target_id}): "
                f"Both nodes must be added to graph first."
            )
        self._edges.append(edge)
        self._nx_graph.add_edge(
            edge.source_id,
            edge.target_id,
            edge_type=edge.edge_type.value if isinstance(edge.edge_type, EdgeType) else edge.edge_type,
            weight=edge.weight,
            description=edge.description,
            obj=edge
        )

    def get_entries(self) -> List[GraphNode]:
        """Return all entry nodes in the graph."""
        return [n for n in self._nodes.values() if n.is_entry]

    def get_targets(self) -> List[GraphNode]:
        """Return all target high-value security nodes in the graph."""
        return [n for n in self._nodes.values() if n.is_target]

    def build_default_architecture(self) -> nx.DiGraph:
        r"""
        Build a comprehensive, synthetic 7-node AI agent architecture benchmark.

        Architecture Layout:
        [ChatUI (Entry)] -> [SupervisorAgent] -> [DataFetcherAgent] -> [SQLTool] -> [ProdDatabase (Target)]
                                            \-> [CodeRunnerAgent] -> [BashTool] -> [RootCredentials (Target)]
        """
        self._nx_graph.clear()
        self._nodes.clear()
        self._edges.clear()

        # Define Nodes
        nodes = [
            GraphNode(node_id="ui_chat", label="Web Chat UI", node_type=NodeType.USER_INTERFACE, is_entry=True),
            GraphNode(node_id="agent_supervisor", label="Supervisor Agent", node_type=NodeType.AGENT),
            GraphNode(node_id="agent_fetcher", label="Data Fetcher Agent", node_type=NodeType.AGENT),
            GraphNode(node_id="agent_coder", label="Code Execution Agent", node_type=NodeType.AGENT),
            GraphNode(node_id="tool_sql", label="SQL Query Tool", node_type=NodeType.TOOL),
            GraphNode(node_id="tool_bash", label="Bash Execution Tool", node_type=NodeType.TOOL),
            GraphNode(node_id="db_production", label="Production DB", node_type=NodeType.DATABASE, is_target=True),
            GraphNode(node_id="cred_root", label="Root Credentials", node_type=NodeType.CREDENTIAL, is_target=True),
        ]

        for n in nodes:
            self.add_node(n)

        # Define Edges
        edges = [
            GraphEdge("ui_chat", "agent_supervisor", EdgeType.PASSES_MESSAGE, weight=0.9, description="User prompt input"),
            GraphEdge("agent_supervisor", "agent_fetcher", EdgeType.PASSES_MESSAGE, weight=0.8, description="Sub-task delegation"),
            GraphEdge("agent_supervisor", "agent_coder", EdgeType.PASSES_MESSAGE, weight=0.85, description="Code generation request"),
            GraphEdge("agent_fetcher", "tool_sql", EdgeType.CALLS_TOOL, weight=0.95, description="Execute DB query"),
            GraphEdge("agent_coder", "tool_bash", EdgeType.CALLS_TOOL, weight=0.9, description="Run shell script"),
            GraphEdge("tool_sql", "db_production", EdgeType.READS_DATA, weight=1.0, description="Read/Write tables"),
            GraphEdge("tool_bash", "cred_root", EdgeType.ACCESSES_CREDENTIAL, weight=0.95, description="Exfiltrate environment keys"),
        ]

        for e in edges:
            self.add_edge(e)

        return self._nx_graph
