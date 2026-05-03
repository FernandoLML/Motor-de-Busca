from typing import List
from .base import SearchStrategy


class RabinKarpSearch(SearchStrategy):
    """
    Rabin-Karp — O(N+M) esperado, usando hash rolante.
    Usa polinômio de base 31 com módulo primo grande para minimizar colisões.
    """

    BASE = 31
    MOD = (1 << 61) - 1  # Mersenne prime

    @property
    def name(self) -> str:
        return "rabin_karp"

    def _hash(self, s: str) -> int:
        h = 0
        for ch in s:
            h = (h * self.BASE + ord(ch)) % self.MOD
        return h

    def search(self, text: str, pattern: str) -> List[int]:
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        # Precompute BASE^(m-1) % MOD
        base_m = pow(self.BASE, m - 1, self.MOD)

        pattern_hash = self._hash(pattern)
        window_hash = self._hash(text[:m])

        for i in range(n - m + 1):
            if window_hash == pattern_hash:
                # Verify character by character to avoid false positives
                match = True
                for j in range(m):
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                if match:
                    positions.append(i)

            # Roll the hash
            if i < n - m:
                window_hash = (
                    (window_hash - ord(text[i]) * base_m) * self.BASE
                    + ord(text[i + m])
                ) % self.MOD

        return positions
