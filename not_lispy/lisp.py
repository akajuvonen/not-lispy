from __future__ import annotations

import operator
from collections import deque
from math import gcd
from typing import Any, Callable, Deque, Dict, List, Optional, Tuple, Union

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

    def __call__(self, *arguments: Tuple[Integer]) -> Integer:
        try:
            result = self.function(*arguments)
        except TypeError:  # some operations in Python only accept two arguments, in Lisp can accept many
            result = arguments[0]
            for argument in arguments[1:]:
                result = self.function(result, argument)
        return Integer(result)


ENV = {Symbol('+'): Operation(operator.add),
       Symbol('-'): Operation(operator.sub),
       Symbol('*'): Operation(operator.mul),
       Symbol('/'): Operation(operator.floordiv),
       Symbol('>'): Operation(operator.gt),
       Symbol('<'): Operation(operator.lt),
       Symbol('>='): Operation(operator.ge),
       Symbol('<='): Operation(operator.le),
       Symbol('='): Operation(operator.eq),
       Symbol('min'): Operation(min),
       Symbol('max'): Operation(max),
       Symbol('modulo'): Operation(operator.mod),
       Symbol('gcd'): Operation(gcd)}


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
            return self.parent.get(name)


GLOBAL_ENV = Environment(environment=ENV)


@attr.s(auto_attribs=True)
class Procedure:
    """User-defined procedure."""
    parameters: List[Symbol]
    body: List[Atom]
    environment: Environment

    def __call__(self, *arguments: Tuple[Integer]) -> Optional[Union[Integer, Callable]]:
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


def evaluate(expression, environment: Environment = GLOBAL_ENV) -> Optional[Union[Integer, Callable]]:
    if isinstance(expression, Integer):  # number
        return expression
    elif isinstance(expression, Symbol):  # symbol lookup
        return environment.get(expression)
    form, *arguments = expression
    if form == 'if':
        _, test_expression, then_expression, else_expression = expression
        if evaluate(test_expression, environment):
            return evaluate(then_expression, environment)
        else:
            return evaluate(else_expression, environment)
    elif form == 'define':
        parameter, value = arguments
        environment.add(parameter, evaluate(value, environment))
        return None  # want to be explicit about returning None here
    elif form == 'lambda':  # user-defined form
        parameters, body = arguments
        return Procedure(parameters, body, Environment(parent=environment))
    elif form == 'load':
        [filename] = arguments
        expressions = _read_lines_from_file(filename)
        for expression in expressions:
            result = evaluate(read(expression))
    else:  # procedure call
        procedure = evaluate(form, environment)
        arguments = (evaluate(a, environment) for a in arguments)
        if not callable(procedure):
            raise SyntaxError(f"{procedure} not a valid procedure")  # this should not happen but needed for typing
        return procedure(*arguments)


def _read_lines_from_file(filename: str) -> List[str]:
    with open(filename) as f:
        content = f.read()
    return list(filter(None, content.split('\n')))


@click.command()
@click.argument('filename')
def execute(filename):
    expressions = _read_lines_from_file(filename)
    for expression in expressions:
        result = evaluate(read(expression))
        if result is not None:
            print(result)
