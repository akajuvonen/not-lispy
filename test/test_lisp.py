import pytest
from not_lispy import read, evaluate


@pytest.mark.parametrize('program, expected', [('(+ 1 2)', 3),
                                               ('(- (/ 10 2) 3)', 2),
                                               ('(* 2 2 3)', 12),
                                               ('((lambda (x y) (+ x y)) 1 2)', 3),
                                               ('(define x 1)', None),
                                               ('(if (> 3 2) 1 0)', 1),
                                               ('(min 3 2 1)', 1),
                                               ('(max 3 4 5)', 5),
                                               ('(modulo 10 8)', 2),
                                               ('(gcd 12 4 8)', 4),
                                               ('(fact 3)', 6),
                                               ('(lcm 3 4)', 12)])
def test_read_eval(program, expected):
    evaluate(read('(load standard_library/stl.lisp)'))
    assert evaluate(read(program)) == expected
