from __future__ import annotations

from pathlib import Path

from valuation_parser.pipeline import run_pipeline


EXPECTED_DIR = Path("data_samples/expected")


def test_strict_default_run_matches_acceptance_baseline(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"

    outputs = run_pipeline(Path("data_samples/raw"), Path("产品与托管机构映射表.csv"), output_dir)

    assert _normalized_text(outputs["valuation_subjects"], encoding="utf-8-sig") == _normalized_text(
        EXPECTED_DIR / "valuation_subjects.csv",
        encoding="utf-8-sig",
    )
    assert _normalized_text(outputs["valuation_positions"], encoding="utf-8-sig") == _normalized_text(
        EXPECTED_DIR / "valuation_positions.csv",
        encoding="utf-8-sig",
    )
    assert _normalized_text(outputs["review_items"], encoding="utf-8-sig") == _normalized_text(
        EXPECTED_DIR / "review_items.csv",
        encoding="utf-8-sig",
    )
    assert _normalized_text(outputs["parse_summary"], encoding="utf-8") == _normalized_text(
        EXPECTED_DIR / "parse_summary.md",
        encoding="utf-8",
    )


def _normalized_text(path: Path, *, encoding: str) -> str:
    return path.read_text(encoding=encoding).replace("\r\n", "\n")