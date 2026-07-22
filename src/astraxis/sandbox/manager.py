"""
ASTRAXIS-AI Sandbox Manager.

Orchestrates sandbox backend selection (Docker vs. Synthetic Fallback),
enforcing safety policies and environment-driven defaults.

Key Concept — Seamless Fallback:
    If settings.enable_docker_sandbox is True and Docker is running, use DockerSandbox.
    Otherwise, automatically fall back to SyntheticSandbox without breaking execution or failing.
"""
from __future__ import annotations

from typing import Optional
from astraxis.core.config import settings
from astraxis.sandbox.runner import BaseSandbox, ExecutionResult, SandboxBackend
from astraxis.sandbox.docker_sandbox import DockerSandbox
from astraxis.sandbox.synthetic_sandbox import SyntheticSandbox


class SandboxManager:
    """
    Centralized manager for acquiring active sandbox instances.

    Usage:
        manager = SandboxManager()
        sandbox = manager.get_active_sandbox()
        res = sandbox.execute("echo test")
        print(f"Executed on backend: {res.backend}")
    """

    def __init__(self, force_backend: Optional[SandboxBackend] = None) -> None:
        self.force_backend = force_backend
        self._docker_sandbox = DockerSandbox()
        self._synthetic_sandbox = SyntheticSandbox()

    def get_active_sandbox(self) -> BaseSandbox:
        """
        Determine and return the best available sandbox backend.

        Selection Priority:
        1. If force_backend is set to DOCKER and Docker is available -> DockerSandbox.
        2. If force_backend is set to SYNTHETIC -> SyntheticSandbox.
        3. If settings.enable_docker_sandbox is True and Docker is available -> DockerSandbox.
        4. Otherwise -> SyntheticSandbox (safe default).
        """
        if self.force_backend == SandboxBackend.DOCKER:
            if self._docker_sandbox.is_available():
                return self._docker_sandbox
            raise RuntimeError("Forced Docker backend, but Docker is not available.")

        if self.force_backend == SandboxBackend.SYNTHETIC:
            return self._synthetic_sandbox

        if settings.enable_docker_sandbox and self._docker_sandbox.is_available():
            return self._docker_sandbox

        return self._synthetic_sandbox

    def execute_payload(self, payload_command: str, timeout: int = 30) -> ExecutionResult:
        """
        Execute a payload in the active sandbox environment.

        Args:
            payload_command: Command string to execute.
            timeout: Execution timeout in seconds.

        Returns:
            ExecutionResult from active sandbox backend.
        """
        sandbox = self.get_active_sandbox()
        return sandbox.execute(payload_command, timeout=timeout)
