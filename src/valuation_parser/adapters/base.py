from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from valuation_parser.models import ParseArtifacts, RouteDecision


class BaseValuationAdapter(ABC):
    key = "base"

    @abstractmethod
    def parse(self, source_file: Path, route: RouteDecision) -> ParseArtifacts:
        raise NotImplementedError
