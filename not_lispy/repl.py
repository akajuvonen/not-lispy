from not_lispy import evaluate, read


def repl():
    while (expression := input('not-lispy>')) != '(exit)':
        print(evaluate(read(expression)))
