from typing import List
from .base import SearchStrategy


class NaiveSearch(SearchStrategy):
    """
    Força Bruta (Naive) — O(N·M) pior caso.
    Desliza o padrão sobre o texto e compara caractere a caractere.
    """

    @property
    def name(self) -> str:
        return "naive"

    def search(self, text: str, pattern: str) -> List[int]:
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        for i in range(n - m + 1):
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)

        return positions
