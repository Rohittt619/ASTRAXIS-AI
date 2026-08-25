"""
Unit tests for ASTRAXIS-AI CLI module.
"""
import pytest
from typer.testing import CliRunner
from astraxis.cli.main import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ASTRAXIS-AI" in result.output

def test_cli_payloads():
    result = runner.invoke(app, ["payloads"])
    assert result.exit_code == 0
    assert "Adversarial Payload Library" in result.output

def test_cli_graph():
    result = runner.invoke(app, ["graph"])
    assert result.exit_code == 0
    assert "Attack Graph Nodes" in result.output

def test_cli_scan():
    result = runner.invoke(app, ["scan", "--backend", "synthetic"])
    assert result.exit_code == 0
    assert "Audit Scan Summary Report" in result.output
