import operator
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Union

import attr


class Atom:
    pass


class Integer(Atom, int):
    pass


class Symbol(Atom, str):
    pass


@attr.s(auto_attribs=True)
class Procedure:
    """User-defined procedure."""
    parameters: List[Symbol]
    body: List[Atom]
    environment: Dict[Symbol, Any]

    def __call__(self, arguments: List[Integer]) -> Union[Integer, Callable]:
        for parameter, value in zip(self.parameters, arguments):
            self.environment[parameter] = value
        return evaluate(self.body, self.environment)


@attr.s(auto_attribs=True)
class Operation():
    """A primitive operation that can be applied to arbitrary number of arguments."""
    function: Callable

    def __call__(self, arguments: List[Integer]) -> Integer:
        """Apply a given function to all arguments one by one."""
        result = arguments[0]
        for argument in arguments[1:]:
            result = self.function(result, argument)
        return Integer(result)


ENV = {Symbol('+'): Operation(operator.add),
       Symbol('-'): Operation(operator.sub),
       Symbol('*'): Operation(operator.mul),
       Symbol('/'): Operation(operator.floordiv)}


def read(program: str) -> List[Union[List, Atom]]:
    return parse(tokenize(program))


def tokenize(program: str) -> List[str]:
    return program.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(tokens_list: List[str]) -> List[Union[List, Atom]]:
    tokens = deque(tokens_list)  # convert to deque since we do a lot of popping from the beginning
    first_token = tokens.popleft()
    parsed = _parse(first_token, tokens)
    if not isinstance(parsed, List):
        raise SyntaxError('Expression must be enclosed in parentheses')
    return parsed


def _parse(current_token: str, remaining_tokens: Deque[str]) -> Union[List, Atom]:
    if current_token == '(':
        parsed_list: List[Union[List, Atom]] = []
        while (current_token := remaining_tokens.popleft()) != ')':
            parsed_list.append(_parse(current_token, remaining_tokens))
        return parsed_list
    else:
        try:
            return Integer(current_token)
        except ValueError:
            return Symbol(current_token)


def evaluate(expression, environment: Dict[Symbol, Any] = ENV) -> Union[Integer, Callable]:
    if isinstance(expression, Integer):  # number
        return expression
    elif isinstance(expression, Symbol):  # symbol lookup
        return environment[expression]
    elif expression[0] == 'define':
        environment[expression[1]] = evaluate(expression[2])
    elif expression[0] == 'lambda':  # user-defined procedure
        parameters = expression[1]
        body = expression[2]
        return Procedure(parameters, body, environment)
    else:  # procedure call
        procedure = evaluate(expression[0])
        arguments = [evaluate(a, environment) for a in expression[1:]]
        if not callable(procedure):
            raise SyntaxError(f"{procedure} not a valid procedure")  # this should not happen but needed for typing
        return procedure(arguments)


def main():
    program = '((lambda (x y) (+ x y)) 1 2)'
    ast = read(program)
    evaluated = evaluate(ast)
    print(evaluated)


if __name__ == '__main__':
    main()
