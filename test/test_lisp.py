import pytest
from not_lispy import read, evaluate


@pytest.mark.parametrize('program, expected', [('(+ 1 2)', 3),
                                               ('(- (/ 10 2) 3)', 2),
                                               ('(* 2 2 3)', 12),
                                               ('((lambda (x y) (+ x y)) 1 2)', 3),
                                               ('(define x 1)', None),
                                               ('(if (> 3 2) 1 0)', 1)])
def test_read_eval(program, expected):
    assert evaluate(read(program)) == expected
