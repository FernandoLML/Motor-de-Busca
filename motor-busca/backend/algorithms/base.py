from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchResult:
    found: bool
    occurrences: int
    positions: List[int]
    execution_time_ms: float
    text_length: int       # N
    pattern_length: int    # M
    algorithm: str


class SearchStrategy(ABC):
    """Strategy interface — every algorithm must implement this."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def search(self, text: str, pattern: str) -> List[int]:
        """Return list of starting indices where pattern occurs in text."""
        ...

    def execute(self, text: str, pattern: str) -> SearchResult:
        import time
        start = time.perf_counter()
        positions = self.search(text, pattern)
        elapsed = (time.perf_counter() - start) * 1000

        return SearchResult(
            found=len(positions) > 0,
            occurrences=len(positions),
            positions=positions,
            execution_time_ms=round(elapsed, 4),
            text_length=len(text),
            pattern_length=len(pattern),
            algorithm=self.name,
        )
