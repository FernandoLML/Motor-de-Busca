"""
Tests for all 4 substring search algorithms.
Validation uses Python's built-in str.find() — ONLY allowed in tests per spec.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from algorithms.naive import NaiveSearch
from algorithms.rabin_karp import RabinKarpSearch
from algorithms.kmp import KMPSearch
from algorithms.boyer_moore import BoyerMooreSearch
from algorithms.base import SearchStrategy


# ── Fixtures ────────────────────────────────────────────────────────────────
STRATEGIES = [
    NaiveSearch(),
    RabinKarpSearch(),
    KMPSearch(),
    BoyerMooreSearch(),
]

def reference_search(text: str, pattern: str):
    """Ground truth using built-in (only allowed in tests)."""
    positions = []
    start = 0
    while True:
        idx = text.find(pattern, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + 1
    return positions


def assert_all(text, pattern):
    expected = reference_search(text, pattern)
    for strategy in STRATEGIES:
        result = strategy.search(text, pattern)
        assert result == expected, (
            f"{strategy.name}: expected {expected}, got {result} "
            f"(text='{text}', pattern='{pattern}')"
        )


# ── Basic cases ──────────────────────────────────────────────────────────────
def test_single_occurrence():
    assert_all("hello world", "world")

def test_multiple_occurrences():
    assert_all("ababab", "ab")

def test_not_found():
    assert_all("hello world", "xyz")

def test_empty_pattern():
    for s in STRATEGIES:
        assert s.search("hello", "") == []

def test_pattern_longer_than_text():
    assert_all("hi", "hello world")

def test_pattern_equals_text():
    assert_all("abcde", "abcde")

def test_single_char_pattern():
    assert_all("aababaa", "a")

def test_overlapping_pattern():
    assert_all("aaaa", "aa")

def test_at_start():
    assert_all("searchme", "search")

def test_at_end():
    assert_all("findsearch", "search")

def test_special_chars():
    assert_all("olá, mundo!", "mundo")

def test_case_sensitive():
    assert_all("Hello World", "hello")
    assert_all("Hello World", "Hello")

def test_repeated_pattern():
    text = "abcabcabc"
    assert_all(text, "abc")

# ── Long text ────────────────────────────────────────────────────────────────
def test_long_text_performance():
    text = "a" * 10_000 + "b"
    pattern = "aaab"
    assert_all(text, pattern)

def test_worst_case_naive():
    text = "a" * 1000
    pattern = "a" * 100
    assert_all(text, pattern)

# ── Strategy pattern ─────────────────────────────────────────────────────────
def test_execute_returns_search_result():
    result = NaiveSearch().execute("hello world", "world")
    assert result.found is True
    assert result.occurrences == 1
    assert result.positions == [6]
    assert result.execution_time_ms >= 0
    assert result.text_length == 11
    assert result.pattern_length == 5
    assert result.algorithm == "naive"

def test_execute_not_found():
    result = KMPSearch().execute("hello", "xyz")
    assert result.found is False
    assert result.occurrences == 0

def test_all_strategies_implement_interface():
    for s in STRATEGIES:
        assert isinstance(s, SearchStrategy)
        assert hasattr(s, 'search')
        assert hasattr(s, 'execute')
        assert hasattr(s, 'name')

# ── Rabin-Karp hash collision resistance ─────────────────────────────────────
def test_rabin_karp_no_false_positives():
    # Deliberately construct a case prone to hash collisions
    text = "a" * 100 + "b" + "a" * 100
    pattern = "b"
    rk = RabinKarpSearch()
    result = rk.search(text, pattern)
    assert result == [100]

# ── Boyer-Moore specific ─────────────────────────────────────────────────────
def test_boyer_moore_sublinear_skip():
    text = "ABCDEFGHIJ" * 100
    pattern = "ABCDEFGHIJ"
    bm = BoyerMooreSearch()
    result = bm.search(text, pattern)
    assert len(result) == 100
    assert result[0] == 0
