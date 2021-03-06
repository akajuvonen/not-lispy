# not-lispy

A Lisp interpreter in Python. Many people have named similar repos as "LisPy" or `lis.py` since it's pretty clever. So this is called... not that.

This repo is intended only for learning and experimentation purposes at the moment. There will be missing features, mistakes and nonoptimal design patterns.

Everything will probably be loosely based on [Make a Lisp](https://github.com/kanaka/mal) and the excellent posts [here](https://norvig.com/lispy.html) and [here](https://norvig.com/lispy2.html).

## Usage

Start repl with `notlispy-repl` (exit using `(exit)`). Evaluate a single file using `notlispy filename`. Note that for the time being all expressions must be on a single line.

**Note:** in the following, `(+ 1 2) => 3 ` means expression `(+ 1 2)` evaluates to `3`.

Read and eval function are available by importing them: `from not_lispy import read, eval`. Then you can evaluate individual expressions, e.g.,  `eval(read('(+ 1 2)'))`. 

The only available number types are integers since I'm aiming for simplicity at firt. Built-in basic "calculator" operations are supported:
- addition `+`
- subtraction `-`
- multiplication `*`
- division `/` (note: since only integers available, this is floor division, i.e., `(/ 3 2) => 1`)

In addition, the following arithmetic operations can be used:
- modulo: `(modulo 10 8) => 2`
- min and max: `(max 1 2 3) => 3`
- greatest common divisor: `(gcd 8 4 12) => 4`

The following operations are implemented in a small standard library in `standard_library/stl.lisp`:
- factorial: `(fact 3) => 6`
- lowest common multiplier: `(lcm 3 4) => 12` (for now supports only two arguments until variadic custom procedures are implemented)

The above standard library is automatically loaded for repl. For any code loaded from a file, stl or any other file containing definitions can be loaded with `(load filename)`, e.g., `(load standard_library/stl.lisp)`. Note that due to lack of `String` type, `filename` must **not** be enclosed in double quotes.

Custom procedures are supported using `lambda`. All procedures must be defined exactly `(lambda (parameters) (body))`, parentheses should not be omitted (no implicit lists).

Variables and procedures can be defined using `define`, e.g.,
- `(define x 1)`
- `(define addone (lambda (x) (+ x 1)))`
- `(addone x) => 2`

Local variable scopes work in the above example, i.e., variable `x` inside custom procedure `addone` will not clash with the global definition. Therefore, it's possible to do something like this:
- `(define addone (lambda (x) (+ x 1)))`
- `(define addtwo (lambda (x) (+ (addone x) 1)))`
- `(addtwo 1) => 3`

Conditional statement `if` can be used using syntax `(if (test-expr) then-expr else-epr)`, e.g., `(if (> 3 2) 1 0) => 1`.
