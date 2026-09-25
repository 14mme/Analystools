from pathlib import Path

from analystools.application.project_context import (
    discover_project,
)


def test_discover_project_from_root(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "ecommerce"
    project_root.mkdir()

    config = project_root / "analystools.toml"

    config.write_text(
        """
[project]
name = "ecommerce"
version = "0.1.0"

[storage]
warehouse = ".analystools/warehouse.duckdb"
metadata = ".analystools/metadata.db"

[output]
directory = "outputs"
""".strip(),
        encoding="utf-8",
    )

    context = discover_project(project_root)

    assert context.root == project_root
    assert context.config.name == "ecommerce"


def test_discover_project_from_child(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "ecommerce"
    child = project_root / "analyses" / "monthly"

    child.mkdir(parents=True)

    config = project_root / "analystools.toml"

    config.write_text(
        """
[project]
name = "ecommerce"

[storage]
warehouse = ".analystools/warehouse.duckdb"
metadata = ".analystools/metadata.db"

[output]
directory = "outputs"
""".strip(),
        encoding="utf-8",
    )

    context = discover_project(child)

    assert context.root == project_root

def test_discover_project_fails_without_config(
    tmp_path: Path,
) -> None:
    try:
        discover_project(tmp_path)
    except RuntimeError as error:
        assert "Could not find an Analystools project" in str(error)
    else:
        raise AssertionError(
            "Expected project discovery to fail"
        )