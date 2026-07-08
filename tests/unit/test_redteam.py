"""
Unit tests for ASTRAXIS-AI Red-Teaming Payload Engine.
"""
import pytest
from astraxis.redteam.payloads import PayloadGenerator, AttackCategory
from astraxis.redteam.hijack import ToolHijacker, ToolType
from astraxis.redteam.collusion import AgentCollusionSimulator, CollusionType

def test_payload_generator():
    gen = PayloadGenerator()
    payloads = gen.generate_all()
    assert len(payloads) > 0
    direct = gen.generate_by_category(AttackCategory.DIRECT_INJECTION)
    assert len(direct) > 0
    summary = gen.summary()
    assert summary["total_payloads"] > 0

def test_tool_hijacker():
    hijacker = ToolHijacker()
    all_attacks = hijacker.simulate_all()
    assert len(all_attacks) > 0
    successful = hijacker.get_successful_attacks()
    assert len(successful) > 0
    summary = hijacker.risk_summary()
    assert "success_rate" in summary

def test_agent_collusion_simulator():
    sim = AgentCollusionSimulator()
    all_collusions = sim.simulate_all()
    assert len(all_collusions) > 0
    high_risk = sim.get_high_risk()
    assert len(high_risk) > 0
    summary = sim.risk_summary()
    assert "average_bypass_probability" in summary
