from __future__ import annotations

from pathlib import Path

from valuation_parser.adapters.base import BaseValuationAdapter
from valuation_parser.models import ParseArtifacts, RouteDecision


class PlaceholderValuationAdapter(BaseValuationAdapter):
    def __init__(self, key: str) -> None:
        self.key = key

    def parse(self, source_file: Path, route: RouteDecision) -> ParseArtifacts:
        return ParseArtifacts(route=route, subjects=[], positions=[])
