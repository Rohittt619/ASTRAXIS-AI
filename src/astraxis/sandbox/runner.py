"""
ASTRAXIS-AI Base Sandbox & Execution Specifications.

Defines abstract sandbox interfaces and standardized execution output objects.

Key Concept — Defensive Isolation:
    When red-teaming AI agents, running adversarial payloads directly on the host system
    is extremely dangerous. A sandbox enforces strict compute, memory, and filesystem boundaries.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class SandboxBackend(str, Enum):
    """Supported sandbox execution backends."""
    DOCKER = "docker"
    SYNTHETIC = "synthetic"


@dataclass
class ExecutionResult:
    """
    Standardized result returned after executing a command or payload inside a sandbox.

    Attributes:
        execution_id:    Unique UUID for tracking this run.
        command:         The command or payload executed.
        exit_code:       Process exit code (0 = success, non-zero = error).
        stdout:          Standard output produced.
        stderr:          Standard error produced.
        duration_ms:     Execution time in milliseconds.
        backend:         The SandboxBackend used (docker or synthetic).
        resource_usage:  CPU/Memory metrics captured during run.
    """
    execution_id: str
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    backend: SandboxBackend
    resource_usage: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_success(self) -> bool:
        """True if execution completed with exit code 0."""
        return self.exit_code == 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize result object for JSON forensic report generation."""
        return {
            "execution_id": self.execution_id,
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_ms": self.duration_ms,
            "backend": self.backend.value if isinstance(self.backend, Enum) else self.backend,
            "resource_usage": self.resource_usage,
        }


class BaseSandbox(ABC):
    """Abstract Base Class for all ASTRAXIS-AI sandbox implementations."""

    @abstractmethod
    def execute(self, command: str, timeout: int = 30) -> ExecutionResult:
        """
        Execute a command or payload inside the isolated sandbox environment.

        Args:
            command: The command string or payload to execute.
            timeout: Maximum allowed execution time in seconds.

        Returns:
            ExecutionResult object containing stdout, stderr, and exit code.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this sandbox backend is available on the system."""
        pass
