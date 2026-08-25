"""
ASTRAXIS-AI CLI Command Engine.

Built with Typer and Rich to provide colorized, formatted terminal commands.

Key Concept — Rich Terminal CLI:
    A professional CLI tool uses Typer for command argument parsing and Rich for tables,
    spinners, and progress bars.
    Entry Points:
      $ astraxis scan      -> Run automated multi-agent red-team scan
      $ astraxis payloads  -> List adversarial payload library
      $ astraxis graph     -> Display attack graph summary & exploit paths
"""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from astraxis.core.logger import console
from astraxis.orchestrator import OrchestratorEngine
from astraxis.redteam import PayloadGenerator
from astraxis.graph import AttackGraphBuilder, AttackGraphAnalyzer
from astraxis.sandbox import SandboxBackend

app = typer.Typer(
    name="astraxis",
    help="ASTRAXIS-AI: Autonomous Multi-Agent AI Red-Teaming & Sandbox Infrastructure CLI",
    add_completion=False,
)


@app.command()
def scan(
    backend: str = typer.Option(
        "synthetic", "--backend", "-b", help="Sandbox backend: 'synthetic' or 'docker'"
    )
) -> None:
    """Execute a full automated red-team audit scan across multi-agent architecture."""
    console.print(
        Panel(
            "[bold cyan]ASTRAXIS-AI Autonomous Red-Team Audit Scan Engine[/bold cyan]\n"
            "[dim]Executing multi-agent exploit simulations, sandbox runs & traffic interception...[/dim]",
            expand=False,
        )
    )

    sb_backend = (
        SandboxBackend.DOCKER if backend.lower() == "docker" else SandboxBackend.SYNTHETIC
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Running multi-step red-team audit pipeline...", total=None)
        orchestrator = OrchestratorEngine(force_sandbox_backend=sb_backend)
        result = orchestrator.run_full_audit()

    # Render Summary Table
    table = Table(title="ASTRAXIS-AI Audit Scan Summary Report", header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold green")

    table.add_row("Scan ID", result.scan_id[:13] + "...")
    table.add_row("Overall Risk Score", f"{result.risk_score} / 1.00")
    table.add_row("Adversarial Payloads Tested", str(result.total_payloads))
    table.add_row("Successful Tool Hijacks", str(result.hijack_count))
    table.add_row("Exploit Paths Found", str(result.exploit_paths))
    table.add_row("Policy Violations Intercepted", str(result.violations))
    table.add_row("Execution Time", f"{result.scan_duration_ms} ms")
    table.add_row("SHA-256 Fingerprint", result.sha256_hash[:20] + "...")

    console.print(table)
    console.print("[bold green]Audit completed successfully![/bold green]\n")


@app.command()
def payloads() -> None:
    """List all adversarial injection payloads in the library."""
    gen = PayloadGenerator()
    items = gen.generate_all()

    table = Table(title="Adversarial Payload Library", header_style="bold cyan")
    table.add_column("Payload ID", style="dim")
    table.add_column("Category", style="yellow")
    table.add_column("Severity", style="red")
    table.add_column("Description", style="white")

    for p in items:
        table.add_row(
            p.payload_id[:8],
            p.category.value,
            p.severity.upper(),
            p.description[:60] + "..."
        )

    console.print(table)


@app.command()
def graph() -> None:
    """Analyze NetworkX attack graph and trace multi-hop exploit paths."""
    builder = AttackGraphBuilder()
    builder.build_default_architecture()
    analyzer = AttackGraphAnalyzer(builder)

    paths = analyzer.find_exploit_paths()
    summary = analyzer.summary()

    console.print(f"[bold cyan]Attack Graph Nodes:[/bold cyan] {summary['total_nodes']}")
    console.print(f"[bold cyan]Directed Edges:[/bold cyan] {summary['total_edges']}")
    console.print(f"[bold cyan]Aggregate Risk Score:[/bold cyan] [bold red]{summary['overall_risk_score']}[/bold red]\n")

    table = Table(title="Top Discovered Multi-Hop Exploit Paths", header_style="bold yellow")
    table.add_column("Path Score", style="bold red")
    table.add_column("Hops", style="cyan")
    table.add_column("Exploit Path Flow", style="white")

    for p in paths:
        table.add_row(
            str(p.path_score),
            str(p.hops),
            " -> ".join(p.nodes)
        )

    console.print(table)


def main() -> None:
    """CLI Main Function Entry Point."""
    app()


if __name__ == "__main__":
    main()
