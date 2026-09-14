from pathlib import Path

import typer

from analystools.application.project_service import create_project
from analystools.cli.output import print_success


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