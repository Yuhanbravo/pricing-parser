from __future__ import annotations

import argparse

from valuation_parser.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the valuation parser scaffold pipeline.")
    parser.add_argument("--input", required=True, help="Input file or directory containing valuation samples.")
    parser.add_argument("--mapping", required=True, help="CSV or XLSX mapping table path.")
    parser.add_argument("--output-dir", required=True, help="Directory for pipeline outputs.")
    parser.add_argument("--summary-path", help="Optional explicit path for parse_summary.md.")
    parser.add_argument("--adapter", help="Manual adapter override.")
    parser.add_argument(
        "--fail-on-routing-error",
        action="store_true",
        help="Fail the run immediately when any file cannot be routed.",
    )
    parser.add_argument(
        "--inactive-mapping-policy",
        choices=["exclude", "include"],
        default="exclude",
        help="Whether inactive mappings should remain routable.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_pipeline(
        input_path=args.input,
        mapping_path=args.mapping,
        output_dir=args.output_dir,
        summary_path=args.summary_path,
        adapter_override=args.adapter,
        fail_on_routing_error=args.fail_on_routing_error,
        include_inactive_mapping=args.inactive_mapping_policy == "include",
    )


if __name__ == "__main__":
    main()
