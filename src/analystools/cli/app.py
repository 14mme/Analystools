import typer

from analystools.cli.commands import dataset, project

app = typer.Typer(
    name="analystools",
    help="Local analytical workbench.",
    no_args_is_help=True,
)

project_app = typer.Typer(
    help="Project management commands."
)

dataset_app = typer.Typer(
    help="Dataset management commands."
)

project_app.command("init")(project.init)

dataset_app.command("add")(dataset.add)
dataset_app.command("list")(dataset.list_command)

app.add_typer(
    project_app,
    name="project",
)

app.add_typer(
    dataset_app,
    name="data",
)