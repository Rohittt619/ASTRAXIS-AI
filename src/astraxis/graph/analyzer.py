"""
ASTRAXIS-AI Attack Graph Analyzer.

Analyzes NetworkX directed attack graphs to trace multi-hop exploit paths,
compute graph centrality metrics, calculate vulnerability scores,
and identify critical bottleneck components requiring defensive hardening.

Key Concept — Multi-Hop Exploit Paths:
    An exploit path is a sequence of connected nodes starting from an untrusted entry point
    (e.g., Web Chat UI) and reaching a high-value security target (e.g., Production DB or Root Credentials).
    Path risk score = product of edge weights along the path.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple
import networkx as nx

from astraxis.graph.builder import AttackGraphBuilder


@dataclass
class ExploitPath:
    """
    Represents a multi-hop exploit path discovered by the analyzer.

    Attributes:
        path_id:       Identifier for this path.
        nodes:         List of node IDs in sequence from entry to target.
        hops:          Total number of hops (edges traversed).
        entry_node:    Starting entry node ID.
        target_node:   Destination target node ID.
        path_score:    Calculated exploit probability / severity score (0.0 to 1.0).
        description:   Human-readable summary of the attack path.
    """
    path_id: str
    nodes: List[str]
    hops: int
    entry_node: str
    target_node: str
    path_score: float
    description: str


class AttackGraphAnalyzer:
    """
    Analyzer engine that evaluates NetworkX attack graphs for security vulnerabilities.

    Usage:
        builder = AttackGraphBuilder()
        graph = builder.build_default_architecture()

        analyzer = AttackGraphAnalyzer(builder)

        # Trace all exploit paths from entry to target
        paths = analyzer.find_exploit_paths()

        # Compute overall architecture vulnerability score
        risk_score = analyzer.calculate_risk_score()

        # Get central bottleneck components
        bottlenecks = analyzer.get_centrality_bottlenecks()
    """

    def __init__(self, builder: AttackGraphBuilder) -> None:
        self.builder = builder
        self.nx_graph = builder.graph

    def find_exploit_paths(self) -> List[ExploitPath]:
        """
        Find all simple directed paths from every entry node to every target node.

        Returns:
            List of ExploitPath objects sorted by path_score in descending order (highest risk first).
        """
        entries = [n.node_id for n in self.builder.get_entries()]
        targets = [n.node_id for n in self.builder.get_targets()]

        exploit_paths: List[ExploitPath] = []
        path_count = 0

        for entry in entries:
            for target in targets:
                if not nx.has_path(self.nx_graph, entry, target):
                    continue

                # Find all simple paths (no cycles)
                all_paths = list(nx.all_simple_paths(self.nx_graph, source=entry, target=target))
                for node_seq in all_paths:
                    path_count += 1
                    
                    # Calculate cumulative path weight score
                    cumulative_score = 1.0
                    for i in range(len(node_seq) - 1):
                        edge_data = self.nx_graph.get_edge_data(node_seq[i], node_seq[i+1])
                        weight = edge_data.get("weight", 1.0) if edge_data else 1.0
                        cumulative_score *= weight

                    hops = len(node_seq) - 1
                    exploit_paths.append(
                        ExploitPath(
                            path_id=f"path_{path_count:03d}",
                            nodes=node_seq,
                            hops=hops,
                            entry_node=entry,
                            target_node=target,
                            path_score=round(cumulative_score, 3),
                            description=f"{hops}-hop exploit path: {' -> '.join(node_seq)}"
                        )
                    )

        # Sort highest risk score first
        exploit_paths.sort(key=lambda p: p.path_score, reverse=True)
        return exploit_paths

    def get_centrality_bottlenecks(self) -> Dict[str, float]:
        """
        Compute degree centrality to find critical bottleneck nodes in the architecture.
        Nodes with high degree centrality participate in the most attack paths.

        Returns:
            Dictionary mapping node_id -> degree_centrality score (0.0 to 1.0).
        """
        if self.nx_graph.number_of_nodes() == 0:
            return {}
        centrality = nx.degree_centrality(self.nx_graph)
        return {k: round(v, 3) for k, v in sorted(centrality.items(), key=lambda x: x[1], reverse=True)}

    def calculate_risk_score(self) -> float:
        """
        Compute an aggregate risk score (0.0 to 1.0) for the whole architecture.

        Formulated as:
            risk = max(path_scores) * (1 - 1 / (1 + len(paths)))
        Higher if there are multiple short, high-probability exploit paths.
        """
        paths = self.find_exploit_paths()
        if not paths:
            return 0.0

        max_score = max(p.path_score for p in paths)
        path_factor = 1.0 - (1.0 / (1.0 + len(paths)))
        aggregate = max_score * (0.7 + 0.3 * path_factor)
        return round(min(1.0, aggregate), 2)

    def summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive forensic analysis summary.

        Returns:
            Dictionary containing node count, edge count, exploit paths, risk score, and bottlenecks.
        """
        paths = self.find_exploit_paths()
        return {
            "total_nodes": self.nx_graph.number_of_nodes(),
            "total_edges": self.nx_graph.number_of_edges(),
            "total_exploit_paths": len(paths),
            "overall_risk_score": self.calculate_risk_score(),
            "highest_risk_path": paths[0].description if paths else "None",
            "bottlenecks": self.get_centrality_bottlenecks(),
        }
