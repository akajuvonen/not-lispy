# not-lispy

A Lisp interpreter in Python. Many people have named similar repos as "LisPy" or `lis.py` since it's pretty clever. So this is called... not that.

This repo is intended only for learning and experimentation purposes at the moment. There will be missing features, mistakes and nonoptimal design patterns.

Everything will probably be loosely based on [Make a Lisp](https://github.com/kanaka/mal) and the excellent posts [here](https://norvig.com/lispy.html) and [here](https://norvig.com/lispy2.html).

## Current status

Read and eval function are available by importing them: `from not_lispy import read, eval`. Then you can evaluate individual expressions, e.g.,  `eval(read('(+ 1 2)'))`. Syntax checking is not perfect, and currently only basic calculator operations are supported (`+`, `-`, `*`, and `/`). Only integers are available at the moment, so division always just performs floor division (e.g., `(/ 3 2)` evaluates to `1`. In short, the interpreter is basically nothing but a calculator (and not a great one, either).

A simple repl is available after installation as command `notlispy-repl`, which you can exit by typing `(exit)`.

Notably `define`, `lambda` or frankly anything not mentioned above is not supported, meaning there is only default gloval environment. Therefore for now only individual expressions can be evaluated.
