"""
ASTRAXIS-AI Red-Teaming Package.

Contains modules for simulating multi-step adversarial attacks
against AI agent applications.
"""
from astraxis.redteam.payloads import PayloadGenerator, InjectionPayload, AttackCategory
from astraxis.redteam.hijack import ToolHijacker, HijackResult
from astraxis.redteam.collusion import AgentCollusionSimulator, CollusionResult

__all__ = [
    "PayloadGenerator", "InjectionPayload", "AttackCategory",
    "ToolHijacker", "HijackResult",
    "AgentCollusionSimulator", "CollusionResult"
]
