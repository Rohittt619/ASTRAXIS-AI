"""
Unit tests for ASTRAXIS-AI Orchestrator Engine.
"""
import pytest
from astraxis.orchestrator import OrchestratorEngine, AuditScanResult
from astraxis.sandbox import SandboxBackend

def test_orchestrator_full_audit():
    orchestrator = OrchestratorEngine(force_sandbox_backend=SandboxBackend.SYNTHETIC)
    result = orchestrator.run_full_audit()

    assert isinstance(result, AuditScanResult)
    assert len(result.scan_id) > 0
    assert 0.0 <= result.risk_score <= 1.0
    assert result.total_payloads > 0
    assert result.exploit_paths > 0
    assert len(result.sha256_hash) == 64
    assert result.scan_duration_ms > 0
