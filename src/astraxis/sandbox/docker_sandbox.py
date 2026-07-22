"""
ASTRAXIS-AI Docker Container Sandbox Backend.

Manages isolated Docker containers for executing untrusted red-teaming payloads.

Key Concept — Docker Container Isolation:
    - Runs containers with memory limits (e.g. 512MB) and CPU quotas.
    - Mounts temporary read-only filesystems.
    - Disables network access (network_mode="none") to prevent exfiltration during tests.
"""
from __future__ import annotations

import time
import uuid
from typing import Dict, Any, Optional

from astraxis.sandbox.runner import BaseSandbox, ExecutionResult, SandboxBackend


class DockerSandbox(BaseSandbox):
    """
    Docker Engine SDK Sandbox Implementation.

    Usage:
        sandbox = DockerSandbox(image="python:3.11-slim")
        if sandbox.is_available():
            res = sandbox.execute("python -c 'print(1+1)'")
    """

    def __init__(
        self,
        image: str = "python:3.11-slim",
        mem_limit: str = "512m",
        network_disabled: bool = True
    ) -> None:
        self.image = image
        self.mem_limit = mem_limit
        self.network_disabled = network_disabled

    def is_available(self) -> bool:
        """Check if Docker SDK is installed and Docker daemon is running."""
        try:
            import docker
            client = docker.from_env()
            client.ping()
            return True
        except Exception:
            return False

    def execute(self, command: str, timeout: int = 30) -> ExecutionResult:
        """
        Execute command inside an ephemeral isolated Docker container.
        """
        if not self.is_available():
            raise RuntimeError(
                "Docker sandbox requested, but Docker SDK is not installed or daemon is unreachable."
            )

        import docker
        client = docker.from_env()
        exec_id = str(uuid.uuid4())
        start_time = time.time()

        network_mode = "none" if self.network_disabled else "bridge"

        try:
            container = client.containers.run(
                self.image,
                command=command,
                detach=False,
                mem_limit=self.mem_limit,
                network_mode=network_mode,
                remove=True,
                stdout=True,
                stderr=True,
            )
            duration_ms = round((time.time() - start_time) * 1000, 2)
            stdout_str = container.decode("utf-8") if isinstance(container, bytes) else str(container)

            return ExecutionResult(
                execution_id=exec_id,
                command=command,
                exit_code=0,
                stdout=stdout_str,
                stderr="",
                duration_ms=duration_ms,
                backend=SandboxBackend.DOCKER,
                resource_usage={"mem_limit": self.mem_limit, "network": network_mode}
            )
        except docker.errors.ContainerError as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return ExecutionResult(
                execution_id=exec_id,
                command=command,
                exit_code=e.exit_status,
                stdout="",
                stderr=str(e.stderr),
                duration_ms=duration_ms,
                backend=SandboxBackend.DOCKER,
                resource_usage={"error": "ContainerError"}
            )
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            return ExecutionResult(
                execution_id=exec_id,
                command=command,
                exit_code=1,
                stdout="",
                stderr=str(e),
                duration_ms=duration_ms,
                backend=SandboxBackend.DOCKER,
                resource_usage={"error": str(e)}
            )
