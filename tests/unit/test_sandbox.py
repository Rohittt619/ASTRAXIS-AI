"""
Unit tests for ASTRAXIS-AI Sandbox Manager & Synthetic Fallback Engine.
"""
import pytest
from astraxis.sandbox import (
    SandboxManager,
    SyntheticSandbox,
    SandboxBackend,
    ExecutionResult
)

def test_synthetic_sandbox_execution():
    sandbox = SyntheticSandbox()
    assert sandbox.is_available() is True

    res = sandbox.execute("python -c 'print(10)'")
    assert res.is_success is True
    assert res.backend == SandboxBackend.SYNTHETIC
    assert res.duration_ms > 0

def test_synthetic_sandbox_blocked_command():
    sandbox = SyntheticSandbox()
    res = sandbox.execute("rm -rf /")
    assert res.is_success is False
    assert res.exit_code == 126
    assert "Destructive" in res.stderr

def test_sandbox_manager_fallback():
    manager = SandboxManager(force_backend=SandboxBackend.SYNTHETIC)
    active = manager.get_active_sandbox()
    assert isinstance(active, SyntheticSandbox)

    res = manager.execute_payload("cat /etc/passwd")
    assert res.backend == SandboxBackend.SYNTHETIC
    assert "Path traversal" in res.stdout or res.exit_code != 0
