from typing import Dict
from .base import SearchStrategy
from .naive import NaiveSearch
from .rabin_karp import RabinKarpSearch
from .kmp import KMPSearch
from .boyer_moore import BoyerMooreSearch


# Registry maps algorithm identifier -> strategy instance
ALGORITHMS: Dict[str, SearchStrategy] = {
    "naive": NaiveSearch(),
    "rabin_karp": RabinKarpSearch(),
    "kmp": KMPSearch(),
    "boyer_moore": BoyerMooreSearch(),
}

ALGORITHM_LABELS = {
    "naive": "Força Bruta (Naive)",
    "rabin_karp": "Rabin-Karp",
    "kmp": "KMP (Knuth-Morris-Pratt)",
    "boyer_moore": "Boyer-Moore",
}


def get_strategy(algorithm: str) -> SearchStrategy:
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Algoritmo '{algorithm}' não encontrado. Disponíveis: {list(ALGORITHMS.keys())}")
    return ALGORITHMS[algorithm]


def list_algorithms():
    return [
        {"id": key, "label": ALGORITHM_LABELS[key]}
        for key in ALGORITHMS
    ]
