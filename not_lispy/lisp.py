import operator
from collections import deque
from typing import Deque, List


ENV = {'+': operator.add, '-': operator.sub}


def tokenize(program):
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens):
    tokens = deque(tokens)
    first_token = tokens.popleft()
    return _parse(first_token, tokens)


def _parse(current_token, remaining_tokens):
    if current_token == '(':
        l = []
        while (current_token := remaining_tokens.popleft()) != ')':
            l.append(_parse(current_token, remaining_tokens))
        return l
    else:
        try:
            return int(current_token)
        except ValueError:
            return current_token


def evaluate(expression, environment):
    if isinstance(expression, int):
        return expression
    else:
        procedure = environment[expression[0]]
        arguments = [evaluate(a, environment) for a in expression[1:]]
        return procedure(*arguments)


def main():
    program = '(+ 1 (- 3 2))'
    tokenized = tokenize(program)
    print(f'Tokenized: {tokenized}')
    parsed = parse(tokenized)
    print(f'Parsed: {parsed}')
    evaluated = evaluate(parsed, ENV)
    print(f'Evaluated: {evaluated}')


if __name__ == '__main__':
    main()
