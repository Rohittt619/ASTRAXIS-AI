"""
Unit tests for ASTRAXIS-AI Attack Graph Builder & Analysis Engine.
"""
import pytest
from astraxis.graph import (
    AttackGraphBuilder,
    AttackGraphAnalyzer,
    GraphNode,
    NodeType,
    GraphEdge,
    EdgeType
)

def test_graph_builder_custom():
    builder = AttackGraphBuilder()
    n1 = GraphNode(node_id="ui", label="UI", node_type=NodeType.USER_INTERFACE, is_entry=True)
    n2 = GraphNode(node_id="agent", label="Agent", node_type=NodeType.AGENT)
    n3 = GraphNode(node_id="db", label="DB", node_type=NodeType.DATABASE, is_target=True)

    builder.add_node(n1)
    builder.add_node(n2)
    builder.add_node(n3)

    builder.add_edge(GraphEdge(source_id="ui", target_id="agent", edge_type=EdgeType.PASSES_MESSAGE))
    builder.add_edge(GraphEdge(source_id="agent", target_id="db", edge_type=EdgeType.READS_DATA))

    assert len(builder.get_entries()) == 1
    assert len(builder.get_targets()) == 1

def test_graph_builder_default_arch():
    builder = AttackGraphBuilder()
    graph = builder.build_default_architecture()
    assert graph.number_of_nodes() == 8
    assert graph.number_of_edges() == 7

def test_graph_analyzer_paths():
    builder = AttackGraphBuilder()
    builder.build_default_architecture()
    analyzer = AttackGraphAnalyzer(builder)

    paths = analyzer.find_exploit_paths()
    assert len(paths) >= 2
    for p in paths:
        assert p.hops > 0
        assert p.path_score > 0.0

def test_graph_analyzer_summary():
    builder = AttackGraphBuilder()
    builder.build_default_architecture()
    analyzer = AttackGraphAnalyzer(builder)

    summary = analyzer.summary()
    assert summary["total_nodes"] == 8
    assert summary["overall_risk_score"] > 0.0
    assert "bottlenecks" in summary
