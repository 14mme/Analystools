import typer

from analystools.cli.commands import (
    dataset, 
    metric,
    profile, 
    project,
    query, 
    validate
)

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

metric_app = typer.Typer(
    help="Metric management commands."
)

project_app.command("init")(project.init)

dataset_app.command("add")(dataset.add)
dataset_app.command("list")(dataset.list_command)

metric_app.command("list")(metric.list_metrics)
metric_app.command("show")(metric.show)
metric_app.command("calculate")(metric.calculate)

app.command("profile")(profile.profile)
app.command("validate")(validate.validate)
app.command("query")(query.query)

app.add_typer(
    project_app,
    name="project",
)

app.add_typer(
    dataset_app,
    name="data",
)

app.add_typer(
    metric_app,
    name="metric",
)