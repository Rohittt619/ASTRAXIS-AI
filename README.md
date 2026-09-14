# ASTRAXIS-AI

> Autonomous Multi-Agent AI Red-Teaming, Exploit Path Simulation & Defense Sandbox Infrastructure

[![CI Pipeline](https://github.com/Rohittt619/ASTRAXIS-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/Rohittt619/ASTRAXIS-AI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Overview

ASTRAXIS-AI is an open-source cybersecurity benchmark and sandbox engine designed to evaluate the safety posture of multi-agent LLM systems. It combines NetworkX threat graph analysis, synthetic red-teaming payload simulation, isolated container execution, and real-time gRPC/HTTP traffic interception.

The system evaluates multi-agent architectures against direct prompt injection, document payload hiding, DAN-style jailbreaks, tool argument hijacking, and inter-agent trust escalation while generating tamper-proof SHA-256 audit reports.

---

## Key Features

- **Red-Teaming Payload Suite:** Multi-category synthetic test suite covering direct injection, indirect payload hiding, roleplay jailbreaks, Base64 obfuscation, and system prompt override scenarios.
- **NetworkX Attack Graph Engine:** Graph-based threat modeling mapping agent nodes, tool dependencies, database assets, and credential stores to trace multi-hop exploit paths.
- **Container Sandbox Isolation:** Dual-mode execution engine using Docker SDK (`512MB` RAM limit, CPU quotas, `network_mode="none"`) with an automatic in-memory synthetic fallback guard.
- **gRPC & HTTP Syscall Interceptor:** Middleware inspecting RPC request payloads and kernel-level syscalls (`execve`, `openat`, `connect`) to flag security policy violations.
- **Glassmorphism Web Dashboard:** Interactive Streamlit web interface for visual audit scan execution, path rendering, and report exports.
- **Rich CLI Interface:** Terminal command suite (`astraxis scan`, `astraxis payloads`, `astraxis graph`) built with Typer and Rich.
- **Cryptographic Report Integrity:** Generates SHA-256 fingerprints for all scan reports to guarantee tamper-proof audit records.

---

## Project Architecture

```
ASTRAXIS-AI Engine Structure
├── src/astraxis/
│   ├── core/          # Pydantic configuration, SHA-256 hasher, Rich logger
│   ├── redteam/       # Payload generator, tool hijacker, collusion simulator
│   ├── graph/         # NetworkX attack graph builder & exploit path analyzer
│   ├── sandbox/       # Docker SDK container manager & synthetic fallback engine
│   ├── interceptor/   # gRPC/HTTP payload interceptor & OS syscall logger
│   ├── orchestrator/  # Master audit scan orchestrator engine
│   ├── ui/            # Streamlit glassmorphism cyber dashboard
│   └── cli/           # Typer & Rich terminal interface
├── tests/
│   ├── unit/          # Unit test suites (100% pass rate across 23 tests)
│   └── integration/   # End-to-end pipeline integration test suite
├── infrastructure/    # Multi-stage Dockerfile & docker-compose configuration
└── docs/              # System architecture guide & sample forensic reports
```

---

## Installation

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Git
- *(Optional)* Docker Desktop (if using container isolation mode)

### Clone & Install

```bash
git clone https.github.com/Rohittt619/ASTRAXIS-AI.git
cd ASTRAXIS-AI
pip install -e .
```

For development & testing tools:
```bash
pip install -e ".[dev]"
```

---

## Usage

### 1. Command-Line Interface (CLI)

Run an automated audit scan:
```bash
astraxis scan --backend synthetic
```

Inspect adversarial payload library:
```bash
astraxis payloads
```

Analyze attack graph exploit paths:
```bash
astraxis graph
```

### 2. Streamlit Web Dashboard

Launch the interactive web application:
```bash
python -m streamlit run src/astraxis/ui/app.py --server.port 8501
```
Open `http://localhost:8501` in your browser.

---

## Testing & Quality Assurance

Run the complete pytest unit and integration test suite:

```bash
pytest tests/
```

All 25 tests execute in isolated synthetic mode without reading any environment secrets or making external network calls.

---

## Security Policy & Safety Disclaimers

- **Synthetic Benchmarks Only:** All adversarial payloads, tool hijack scenarios, and graph nodes in ASTRAXIS-AI are synthetic, non-destructive test cases intended solely for defensive security evaluations and research.
- **Zero Secret Access:** The engine does not read, log, or transmit any environment variables or host API keys.
- **Network Isolation:** Sandbox container executions run with disabled network interfaces (`network_mode="none"`).

---

## Author & Maintainer

**Rohit** ([@Rohittt619](https://github.com/Rohittt619))  
*Autonomous AI Security Research & Sandbox Infrastructure*

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
