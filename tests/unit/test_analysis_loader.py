from pathlib import Path

from analystools.application.analysis_loader import (
    load_analysis
)


def test_load_analysis(tmp_path: Path) -> None:
    path = tmp_path / "revenue.yaml"

    path.write_text(
        """
analysis:
    name: revenue_by_category
    dataset: sales

    dimensions:
    - category

    metrics:
    - revenue
    - profit

    order_by:
    - field: revenue
      direction: DESC
""".strip(),
        encoding=("utf-8"),
    )

    analysis = load_analysis(path)

    assert analysis.name == "revenue_by_category"
    assert analysis.dataset == "sales"
    assert analysis.dimensions == ["category"]
    assert analysis.metrics == ["revenue", "profit"]