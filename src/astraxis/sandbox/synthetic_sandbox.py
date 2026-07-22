"""
ASTRAXIS-AI Synthetic Fallback Sandbox Backend.

Provides a lightweight, zero-dependency, deterministic sandbox simulator.
Used when Docker is not installed or when running in local development mode.

Key Concept — Synthetic Sandbox:
    Simulates command execution safely in memory by intercepting known malicious payloads
    (e.g., path traversal, rm -rf, SQL injections) and returning predictable stdout/stderr outputs
    without touching system files or network interfaces.
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any

from astraxis.sandbox.runner import BaseSandbox, ExecutionResult, SandboxBackend


class SyntheticSandbox(BaseSandbox):
    """
    Synthetic Sandbox Engine for offline/mock red-teaming simulations.

    Usage:
        sandbox = SyntheticSandbox()
        res = sandbox.execute("cat /etc/passwd")
        print(res.exit_code, res.stdout)
    """

    def is_available(self) -> bool:
        """Synthetic sandbox is always available on any operating system."""
        return True

    def execute(self, command: str, timeout: int = 30) -> ExecutionResult:
        """
        Simulate command execution inside an isolated synthetic container sandbox.
        """
        exec_id = str(uuid.uuid4())
        start_time = time.time()

        cmd_lower = command.lower()

        # Intercept known threat patterns for red-teaming simulation
        if "rm -rf" in cmd_lower or "drop table" in cmd_lower:
            stdout = ""
            stderr = "[SYNTHETIC SANDBOX GUARD] Command blocked: Destructive file/DB deletion forbidden."
            exit_code = 126
        elif "cat /etc/passwd" in cmd_lower or "../../" in cmd_lower:
            stdout = "[SYNTHETIC SANDBOX GUARD] Path traversal detected. Access denied."
            stderr = ""
            exit_code = 1
        elif "curl" in cmd_lower or "wget" in cmd_lower:
            stdout = "[SYNTHETIC SANDBOX GUARD] Network access disabled (network_mode=none)."
            stderr = ""
            exit_code = 1
        else:
            stdout = f"[SYNTHETIC SANDBOX] Executed successfully: '{command}'"
            stderr = ""
            exit_code = 0

        duration_ms = round((time.time() - start_time) * 1000 + 4.2, 2)

        return ExecutionResult(
            execution_id=exec_id,
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration_ms=duration_ms,
            backend=SandboxBackend.SYNTHETIC,
            resource_usage={
                "cpu_cores": 1,
                "memory_mb": 64,
                "virtualized": True,
                "status": "SANDBOX_PROTECTED"
            }
        )
