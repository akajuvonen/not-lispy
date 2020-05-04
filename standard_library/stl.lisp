(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))
(define lcm (lambda (x y) (/ (* x y) (gcd x y))))
