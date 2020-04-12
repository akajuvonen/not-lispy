# not-lispy

A Lisp interpreter in Python. Many people have named similar repos as "LisPy" or `lis.py` since it's pretty clever. So this is called... not that.

This repo is intended only for learning and experimentation purposes at the moment. There will be missing features, mistakes and nonoptimal design patterns.

Everything will probably be loosely based on [Make a Lisp](https://github.com/kanaka/mal) and the excellent posts [here](https://norvig.com/lispy.html) and [here](https://norvig.com/lispy2.html).

## Usage

Read and eval function are available by importing them: `from not_lispy import read, eval`. Then you can evaluate individual expressions, e.g.,  `eval(read('(+ 1 2)'))`. 

The only available number types are integers. Only basic "calculator" operations are supported for now:
- addition `+`
- subtraction `-`
- multiplication `*`
- division `/` (note: since only integers available, this is floor division)

In addition, a basic repl is available through command `notlispy-repl`. You can exit by typing `(exit)`.

For now only individual expressions can be evaluated. There is only global environment, and variables cannot be defined yet (so no `define`, `lambda` etc.). I plan to add support for local environments next along with lambda function definitions.
