from not_lispy.lisp import read, evaluate


def main():
    while (expression := input('not-lispy>')) != '(exit)':
        print(evaluate(read(expression)))


if __name__ == '__main__':
    main()
