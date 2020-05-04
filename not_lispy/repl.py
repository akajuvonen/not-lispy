import readline

from not_lispy import evaluate, read

readline.parse_and_bind('set editing-mode vi')


STL_PATH = 'standard_library/stl.lisp'


def repl():
    evaluate(read(f'(load {STL_PATH})'))
    print(f"Loaded standard library from '{STL_PATH}'")
    try:
        while (expression := input('not-lispy>')) != '(exit)':
            result = evaluate(read(expression))
            if result is not None:
                print(result)
    except EOFError:
        print()
