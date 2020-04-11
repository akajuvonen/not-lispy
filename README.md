# not-lispy

A Lisp interpreter in Python. Many people have named similar repos as "LisPy" or `lis.py` since it's pretty clever. So this is called... not that.

This repo is intended only for learning and experimentation purposes at the moment. There will be missing features, mistakes and nonoptimal design patterns.

Everything will probably be loosely based on [Make a Lisp](https://github.com/kanaka/mal) and the excellent posts [here](https://norvig.com/lispy.html) and [here](https://norvig.com/lispy2.html).

## Current status

Only supports integers and a few basic operations (addition, subtraction, multiplication, division), and they support arbitrary number of arguments. Numbers don't have any proper class yet, they are just ints. Currently it's basically a calculator without a REPL. For example, `eval(read('(+ 1 (* 2 3))'))` evaluates to `7` as it should. Calculation support integers only for now.

Version `0.2.0` adds class `Atom` and its subclasses `Integer` and `Symbol` (`+`, `-` etc.) for better typing.
