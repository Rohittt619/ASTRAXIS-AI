"""
ASTRAXIS-AI Interceptor & Syscall Audit Package.

Provides gRPC/HTTP request interceptors, syscall audit loggers,
and real-time anomaly detection for monitoring agent behavior.
"""
from astraxis.interceptor.traffic import TrafficInterceptor, TrafficEvent, ProtocolType
from astraxis.interceptor.syscall import SyscallAuditLogger, SyscallEvent, SyscallType
from astraxis.interceptor.detector import AnomalyDetector, AnomalyViolation

__all__ = [
    "TrafficInterceptor",
    "TrafficEvent",
    "ProtocolType",
    "SyscallAuditLogger",
    "SyscallEvent",
    "SyscallType",
    "AnomalyDetector",
    "AnomalyViolation",
]
