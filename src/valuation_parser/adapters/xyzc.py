from __future__ import annotations

from pathlib import Path

from valuation_parser.adapters.tabular import ConfigurableTabularAdapter


class XyzcValuationAdapter(ConfigurableTabularAdapter):
    key = "xyzc"

    def __init__(self, config_path: Path | None = None) -> None:
        super().__init__(config_name=self.key, config_path=config_path)
