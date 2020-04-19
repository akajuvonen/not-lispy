import readline

from not_lispy import evaluate, read

readline.parse_and_bind('set editing-mode vi')


def repl():
    while (expression := input('not-lispy>')) != '(exit)':
        result = evaluate(read(expression))
        if result is not None:
            print(result)
