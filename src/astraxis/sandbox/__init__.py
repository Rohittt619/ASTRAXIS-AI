"""
ASTRAXIS-AI Sandbox Package.

Provides containerized runtime isolation for executing red-teaming tests
and simulated agent workloads via Docker Engine SDK or Synthetic Fallback.
"""
from astraxis.sandbox.runner import BaseSandbox, ExecutionResult, SandboxBackend
from astraxis.sandbox.synthetic_sandbox import SyntheticSandbox
from astraxis.sandbox.manager import SandboxManager

__all__ = [
    "BaseSandbox",
    "ExecutionResult",
    "SandboxBackend",
    "SyntheticSandbox",
    "SandboxManager",
]
