from __future__ import annotations

import operator
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Optional, Union

import attr
import click


class Atom:
    pass


class Integer(Atom, int):
    pass


class Symbol(Atom, str):
    pass


@attr.s(auto_attribs=True)
class Operation():
    function: Callable

    def __call__(self, arguments:List[Integer]):
        pass


@attr.s()
class VariadricOperation(Operation):
    def __call__(self, arguments: List[Integer]) -> Integer:
        """Apply a given function to all arguments one by one."""
        result = arguments[0]
        for argument in arguments[1:]:
            result = self.function(result, argument)
        return Integer(result)


@attr.s()
class BinaryOperation(Operation):
    def __call__(self, arguments: List[Integer]):
        if len(arguments) != 2:
            raise TypeError(f'Expected 2 arguments, got {len(arguments)}')
        return self.function(*arguments)


ENV = {Symbol('+'): VariadricOperation(operator.add),
       Symbol('-'): VariadricOperation(operator.sub),
       Symbol('*'): VariadricOperation(operator.mul),
       Symbol('/'): VariadricOperation(operator.floordiv),
       Symbol('>'): BinaryOperation(operator.gt),
       Symbol('<'): BinaryOperation(operator.lt),
       Symbol('>='): BinaryOperation(operator.ge),
       Symbol('<='): BinaryOperation(operator.le),
       Symbol('='): BinaryOperation(operator.eq)}


@attr.s(auto_attribs=True)
class Environment:
    environment: Dict[Symbol, Any] = attr.ib(factory=dict)
    parent: Optional[Environment] = None

    def add(self, name, value):
        self.environment[name] = value

    def get(self, name):
        try:
            return self.environment[name]
        except KeyError:
            self.parent.get(name)


@attr.s(auto_attribs=True)
class Procedure:
    """User-defined procedure."""
    parameters: List[Symbol]
    body: List[Atom]
    environment: Environment

    def __call__(self, arguments: List[Integer]) -> Optional[Union[Integer, Callable]]:
        for parameter, value in zip(self.parameters, arguments):
            self.environment.add(parameter, value)
        return evaluate(self.body, self.environment)


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


def evaluate(expression, environment: Environment = None) -> Optional[Union[Integer, Callable]]:
    if environment is None:
        environment = Environment(environment=ENV)
    if isinstance(expression, Integer):  # number
        return expression
    elif isinstance(expression, Symbol):  # symbol lookup
        return environment.get(expression)
    elif expression[0] == 'if':
        _, test_expression, then_expression, else_expression = expression
        if evaluate(test_expression):
            return evaluate(then_expression)
        else:
            return evaluate(else_expression)
    elif expression[0] == 'define':
        environment.add(expression[1], evaluate(expression[2]))
        return None  # want to be explicit about returning None here
    elif expression[0] == 'lambda':  # user-defined procedure
        parameters = expression[1]
        body = expression[2]
        return Procedure(parameters, body, Environment(parent=environment))
    else:  # procedure call
        procedure = evaluate(expression[0])
        arguments = [evaluate(a, environment) for a in expression[1:]]
        if not callable(procedure):
            raise SyntaxError(f"{procedure} not a valid procedure")  # this should not happen but needed for typing
        return procedure(arguments)


@click.command()
@click.argument('filename')
def execute(filename):
    print(f'TODO: load and execute program {filename}')
