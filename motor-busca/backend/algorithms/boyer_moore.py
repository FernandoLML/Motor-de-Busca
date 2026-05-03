from typing import List, Dict
from .base import SearchStrategy


class BoyerMooreSearch(SearchStrategy):
    """
    Boyer-Moore — O(N/M) melhor caso (sublinear), muito eficiente para texto natural.
    Implementa as duas heurísticas:
    - Bad Character Rule
    - Good Suffix Rule
    Compara o padrão da direita para a esquerda.
    """

    @property
    def name(self) -> str:
        return "boyer_moore"

    def _bad_character_table(self, pattern: str) -> Dict[str, int]:
        """
        Para cada caractere, armazena o índice da sua última ocorrência no padrão.
        Se não ocorre, considera -1.
        """
        table: Dict[str, int] = {}
        for i, ch in enumerate(pattern):
            table[ch] = i
        return table

    def _good_suffix_table(self, pattern: str) -> List[int]:
        """
        Tabela de bom sufixo (good suffix shift).
        shift[i] = quanto o padrão pode ser deslocado quando uma incompatibilidade
        ocorre na posição i do padrão.
        """
        m = len(pattern)
        shift = [m] * (m + 1)
        border = [0] * (m + 1)

        # Phase 1: Compute border positions
        i = m
        j = m + 1
        border[i] = j

        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if shift[j] == m:
                    shift[j] = j - i
                j = border[j]
            i -= 1
            j -= 1
            border[i] = j

        # Phase 2: Fill remaining shifts
        j = border[0]
        for i in range(m + 1):
            if shift[i] == m:
                shift[i] = j
            if i == j:
                j = border[j]

        return shift

    def search(self, text: str, pattern: str) -> List[int]:
        n = len(text)
        m = len(pattern)
        positions = []

        if m == 0 or m > n:
            return positions

        bad_char = self._bad_character_table(pattern)
        good_suffix = self._good_suffix_table(pattern)

        s = 0  # shift of the pattern with respect to text
        while s <= n - m:
            j = m - 1

            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1

            if j < 0:
                positions.append(s)
                s += good_suffix[0]
            else:
                bc_shift = j - bad_char.get(text[s + j], -1)
                gs_shift = good_suffix[j + 1]
                s += max(bc_shift, gs_shift)

        return positions
