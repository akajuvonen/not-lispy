import pytest
from not_lispy import read, evaluate


def test_tokenize():
    assert read('(+ 1 (- 2 3))') == ['+', 1, ['-', 2, 3]]


def test_evaluate():
    assert evaluate(['+', 1, ['*', 2, 3]]) == 7
    assert evaluate(['/', ['-', 10, 4], 2]) == 3
