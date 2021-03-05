from __future__ import annotations
from collections.abc import Callable
from typing import TypeVar, Generic, Optional, Union

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')

Rules = dict['NonTerminal', 'Expr']

class Expr(Generic[T]):
    def __add__(self, other):
        return Follow(self, other)

    def __or__(self, other):
        return Or(self, other)

    def then(self, transform: Callable[[T], T2]) -> Expr[T2]:
        return Transform(self, transform)

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, T]]:
        pass

class NonTerminal(Expr[T]):
    def __init__(self, name: str):
        self.name = name

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, T]]:
        return rules[self].check(text, pos, rules)

    def __repr__(self):
        return f"NonTerminal({self.name})"


class Terminal(Expr[str]):
    def __init__(self, text: str):
        self.text = text

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, str]]:
        if len(text) > pos and text[pos:pos+len(self.text)] == self.text:
            return (pos + len(self.text), self.text)
        else:
            return None

class TerminalR(Expr[str]):
    def __init__(self, regex: str):
        self.regex = re.compile(regex)

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, str]]:
        m = self.regex.match(text, pos)
        if m:
            return (m.span()[1], m.group())
        else:
            return None

class Follow(Expr[tuple[T1, T2]]):
    def __init__(self, left: Expr[T1], right: Expr[T2]):
        self.left = left
        self.right = right

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, tuple[T1, T2]]]:
        if l_res := self.left.check(text, pos, rules):
            l_pos, l_val = l_res
            if l_res and (r_res := self.right.check(text, l_pos, rules)):
                r_pos, r_val = r_res
                return (r_pos, (l_val, r_val))
            else:
                return None
        else:
            return None


class Many(Expr[list[T]]):
    def __init__(self, expr: Expr[T]):
        self.expr = expr

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, list[T]]]:
        vals: list[T] = []
        while (res := self.expr.check(text, pos, rules)) and pos < len(text):
            pos, val = res
            vals.append(val)

        return pos, vals

class ManyOne(Many[T]):
    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, list[T]]]:
        return (self.expr + Many(self.expr)).check(text, pos, rules)

class Or(Expr[Union[T1, T2]]):
    def __init__(self, left: Expr[T1], right: Expr[T2]):
        self.left = left
        self.right = right

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, Union[T1, T2]]]:
        l_res = self.left.check(text, pos, rules)
        return l_res or self.right.check(text, pos, rules)


class Opt(Expr[Optional[T]]):
    def __init__(self, expr: Expr[T]):
        self.expr = expr

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, Optional[T]]]:
        res = self.expr.check(text, pos, rules)
        return res or (pos, None)

class Transform(Expr[T2]):
    def __init__(self, expr: Expr[T1], transform: Callable[[T1], T2]):
        self.expr = expr
        self.transform = transform

    def check(self, text: str, pos: int,
              rules: Rules) -> Optional[tuple[int, T2]]:
        res = self.expr.check(text, pos, rules)
        if res:
            pos, val = res
            return (pos, self.transform(val))
        else:
            return None


class Parser(Generic[T]):
    def __init__(self, init: NonTerminal[T], rules: Rules):
        self.init = init
        self.rules = rules

    def parse(self, text: str) -> Optional[T]:
        res = self.init.check(text, 0, self.rules)
        if res and res[0] == len(text):
            return res[1]
        else:
            return None