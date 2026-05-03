from typing import List
from .base import SearchStrategy


class KMPSearch(SearchStrategy):
    """
    KMP (Knuth-Morris-Pratt) — O(N+M) garantido.
    Pré-processa o padrão para construir a tabela de falhas (failure function)
    e evita retroceder o ponteiro do texto.
    """

    @property
    def name(self) -> str:
        return "kmp"

    def _build_failure_table(self, pattern: str) -> List[int]:
        """
        Tabela de falhas (prefix function / failure function).
        failure[i] = comprimento do maior prefixo próprio de pattern[0..i]
        que também é sufixo.
        """
        m = len(pattern)
        failure = [0] * m
        k = 0  # length of previous longest prefix suffix

        for i in range(1, m):
            while k > 0 and pattern[k] != pattern[i]:
                k = failure[k - 1]
            if pattern[k] == pattern[i]:
                k += 1
            failure[i] = k

        return failure

    def search(self, text: str, pattern: str) -> List[int]:
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        failure = self._build_failure_table(pattern)
        q = 0  # number of characters matched

        for i in range(n):
            while q > 0 and pattern[q] != text[i]:
                q = failure[q - 1]

            if pattern[q] == text[i]:
                q += 1

            if q == m:
                positions.append(i - m + 1)
                q = failure[q - 1]

        return positions
