import operator
from collections import deque
from typing import Callable, Deque, Dict, List, Union

import attr


@attr.s(auto_attribs=True)
class Operation:
    function: Callable

    def __call__(self, arguments: List[int]) -> int:
        """Apply a given function to all arguments one by one."""
        result = arguments[0]
        for argument in arguments[1:]:
            result = self.function(result, argument)
        return result


class Atom:
    pass


class Integer(Atom, int):
    pass


class Symbol(Atom, str):
    pass


ENV = {'+': Operation(operator.add), '-': Operation(operator.sub), '*': Operation(operator.mul),
       '/': Operation(operator.floordiv)}


def read(program: str) -> List[Union[List, int, str]]:
    return parse(tokenize(program))


def tokenize(program: str) -> List[str]:
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens_list: List[str]) -> List[Union[List, int, str]]:
    tokens = deque(tokens_list)  # convert to deque since we do a lot of popping from the beginning
    first_token = tokens.popleft()
    return _parse(first_token, tokens)


def _parse(current_token: str, remaining_tokens: Deque[str]):
    if current_token == '(':
        parsed_list = []
        while (current_token := remaining_tokens.popleft()) != ')':
            parsed_list.append(_parse(current_token, remaining_tokens))
        return parsed_list
    else:
        # Return int if possible, otherwise str
        try:
            return int(current_token)
        except ValueError:
            return current_token


def evaluate(expression: Union[int, str], environment: Dict[str, Callable]) -> Union[int, Callable]:
    if isinstance(expression, int):
        return expression
    else:
        procedure = environment[expression[0]]
        arguments = [evaluate(a, environment) for a in expression[1:]]
        return procedure(arguments)


def main():
    program = '(/ (+ (- 5 3 1) 12 1) 2)'
    print(f"Program '{program}' evaluates to {evaluate(read(program), ENV)}")


if __name__ == '__main__':
    main()
