import pytest
from not_lispy.lisp import tokenize, parse, evaluate


def test_tokenize():
    assert tokenize('(+ 1 (- 2 3))') == ['(', '+', '1', '(', '-', '2' ,'3', ')', ')']
