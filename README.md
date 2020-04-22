# not-lispy

A Lisp interpreter in Python. Many people have named similar repos as "LisPy" or `lis.py` since it's pretty clever. So this is called... not that.

This repo is intended only for learning and experimentation purposes at the moment. There will be missing features, mistakes and nonoptimal design patterns.

Everything will probably be loosely based on [Make a Lisp](https://github.com/kanaka/mal) and the excellent posts [here](https://norvig.com/lispy.html) and [here](https://norvig.com/lispy2.html).

## Usage

**Note:** in the following, `(+ 1 2) => 3 ` means expression `(+ 1 2)` evaluates to `3`.

Read and eval function are available by importing them: `from not_lispy import read, eval`. Then you can evaluate individual expressions, e.g.,  `eval(read('(+ 1 2)'))`. 

The only available number types are integers since I'm aiming for simplicity at firt. Built-in basic "calculator" operations are supported:
- addition `+`
- subtraction `-`
- multiplication `*`
- division `/` (note: since only integers available, this is floor division, i.e., `(/ 3 2) => 1`)

Custom procedures are supported using `lambda`. All procedures must be defined exactly `(lambda (parameters) (body))`, parentheses should not be omitted (no implicit lists).

Variables and procedures can be defined using `define`, e.g.,
- `(define x 1)`
- `(define addone (lambda (x) (+ x 1)))`
- `(addone x) => 2`

Local variable scopes work in the above example, i.e., variable `x` inside custom procedure `addone` will not clash with the global definition. Therefore, it's possible to do something like this:
- `(define addone (lambda (x) (+ x 1)))`
- `(define addtwo (lambda (x) (+ (addone x) (addone x))))`
- `(addtwo 1) => 3`

In addition, a basic repl is available through command `notlispy-repl`. You can exit by typing `(exit)`.
