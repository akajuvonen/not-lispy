from not_lispy import read, evaluate


def repl():
    while (expression := input('not-lispy>')) != '(exit)':
        print(evaluate(read(expression)))
