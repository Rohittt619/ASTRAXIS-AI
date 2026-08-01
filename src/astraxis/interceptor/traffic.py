"""
ASTRAXIS-AI gRPC & HTTP Traffic Interceptor Module.

Captures, inspects, and logs gRPC/HTTP agent payload transmissions, tool calls,
and API requests in real time to intercept unauthorized data exfiltration.

Key Concept — Network Traffic Interceptors:
    In microservice architectures, gRPC and HTTP interceptors act as middleware filters.
    Every request passing between agents or between agents and external tools passes
    through `TrafficInterceptor`, allowing ASTRAXIS-AI to inspect raw payload bodies
    before they are processed.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional


class ProtocolType(str, Enum):
    """Supported network protocol types."""
    GRPC = "grpc"
    HTTP = "http"
    WEBSOCKET = "websocket"


@dataclass
class TrafficEvent:
    """
    Represents an intercepted network event or tool RPC call.

    Attributes:
        event_id:      Unique UUID for tracking this intercepted payload.
        protocol:      ProtocolType (gRPC or HTTP).
        sender_agent:  ID of the agent initiating the request (e.g. "agent_fetcher").
        target_endpoint: Target service or tool URL (e.g. "grpc://sql-service:50051").
        method_name:   gRPC method or HTTP endpoint path (e.g. "/QueryDatabase").
        headers:       Request headers or gRPC metadata key-values.
        body_payload:  Raw text content of the request body.
        timestamp:     ISO timestamp of interception.
        is_blocked:    True if security filter blocked the request.
    """
    event_id: str
    protocol: ProtocolType
    sender_agent: str
    target_endpoint: str
    method_name: str
    headers: Dict[str, str]
    body_payload: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    is_blocked: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize event to dictionary for JSON audit logs."""
        return {
            "event_id": self.event_id,
            "protocol": self.protocol.value if isinstance(self.protocol, Enum) else self.protocol,
            "sender_agent": self.sender_agent,
            "target_endpoint": self.target_endpoint,
            "method_name": self.method_name,
            "headers": self.headers,
            "body_payload": self.body_payload,
            "timestamp": self.timestamp,
            "is_blocked": self.is_blocked,
        }


class TrafficInterceptor:
    """
    Middleware traffic interceptor for capturing and inspecting agent messages.

    Usage:
        interceptor = TrafficInterceptor()
        event = interceptor.intercept_request(
            protocol=ProtocolType.GRPC,
            sender="DataAgent",
            endpoint="grpc://sql-tool:50051",
            method="/ExecuteSQL",
            payload="SELECT * FROM users;"
        )
        print(event.event_id, event.is_blocked)
    """

    def __init__(self) -> None:
        self._captured_events: List[TrafficEvent] = []
        self._blocked_keywords = ["drop table", "rm -rf", "curl http://", "/etc/passwd"]

    @property
    def captured_events(self) -> List[TrafficEvent]:
        """Return list of all captured traffic events."""
        return self._captured_events

    def intercept_request(
        self,
        protocol: ProtocolType,
        sender: str,
        endpoint: str,
        method: str,
        payload: str,
        headers: Optional[Dict[str, str]] = None
    ) -> TrafficEvent:
        """
        Intercept an incoming or outgoing agent traffic request.

        Args:
            protocol: ProtocolType enum (gRPC/HTTP).
            sender: Name of sender agent.
            endpoint: Destination endpoint address.
            method: API endpoint path or gRPC method.
            payload: Request body payload text.
            headers: Optional dictionary of headers.

        Returns:
            TrafficEvent object.
        """
        payload_lower = payload.lower()
        should_block = any(kw in payload_lower for kw in self._blocked_keywords)

        event = TrafficEvent(
            event_id=str(uuid.uuid4()),
            protocol=protocol,
            sender_agent=sender,
            target_endpoint=endpoint,
            method_name=method,
            headers=headers or {},
            body_payload=payload,
            is_blocked=should_block,
        )

        self._captured_events.append(event)
        return event

    def get_blocked_events(self) -> List[TrafficEvent]:
        """Return all events that were blocked by security rules."""
        return [e for e in self._captured_events if e.is_blocked]

    def clear(self) -> None:
        """Clear captured events cache."""
        self._captured_events.clear()
