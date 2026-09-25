from pathlib import Path

import typer

from analystools.application.project_service import create_project
from analystools.cli.output import print_success
from analystools.application.project_context import (
    discover_project,
)


def init(
    name: str = typer.Argument(..., help="Project name."),
    path: Path = typer.Option(
        Path("."),
        "--path",
        "-p",
        help="Project location.",
    ),
) -> None:
    project_root = path.resolve() / name

    if project_root.exists() and any(project_root.iterdir()):
        raise typer.BadParameter(
            f"Directory already exists and is not empty: {project_root}"
        )

    project = create_project(
        root=project_root,
        name=name,
    )

    print_success(
        f"Project '{project.name}' created at {project.root}"
    )

def info() -> None:
    context = discover_project()

    print()
    print("Analystools Project")
    print("=" * 60)

    print(f"Name : {context.config.name}")
    print(f"Version : {context.config.version}")
    print(f"Root : {context.root}")
    print(f"Config : {context.config_file}")
    print(f"Warehouse : {context.warehouse_path}")
    print(f"Metadata : {context.metadata_path}")
    print(f"Metrics : {context.metrics_directory}")
    print(f"Analyses : {context.analyses_directory}")
    print(f"Reports : {context.reports_directory}")