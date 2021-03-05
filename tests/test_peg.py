"""Tests for PEG parsing"""

import pytest
from wordsindecks.parser.parser import *

def test_accept_terminal():
    expr = NonTerminal('expr')
    rules = { expr: Terminal('aaa') }
    parser = Parser(expr, rules)
    assert parser.parse('aaa')
    assert parser.parse('aaaa') is False
    assert parser.parse('aaab') is False
    assert parser.parse('aa') is False

def test_accept_terminal_regex():
    expr = NonTerminal('expr')
    rules = { expr: TerminalR(r'[a-z]+') }
    parser = Parser(expr, rules)
    assert parser.parse('abcd')
    assert parser.parse('') is False
    assert parser.parse('abcd--') is False

def test_accept_follow():
    expr = NonTerminal('expr')
    rules = { expr: Terminal('a') + Terminal('b') }
    parser = Parser(expr, rules)
    assert parser.parse('ab')
    assert parser.parse('a') is False
    assert parser.parse('b') is False
    assert parser.parse('aab') is False
    assert parser.parse('') is False

def test_accept_or():
    expr = NonTerminal('expr')
    rules = { expr: Terminal('a') | Terminal('b') }
    parser = Parser(expr, rules)
    assert parser.parse('ab') is False
    assert parser.parse('a')
    assert parser.parse('b')
    assert parser.parse('') is False

def test_accept_many():
    expr = NonTerminal('expr')
    rules = { expr: Many(Terminal('a') | Terminal('b')) }
    parser = Parser(expr, rules)
    assert parser.parse('ab')
    assert parser.parse('a')
    assert parser.parse('b')
    assert parser.parse('') == []

def test_accept_manyone():
    expr = NonTerminal('expr')
    rules = { expr: ManyOne(Terminal('a') | Terminal('b')) }
    parser = Parser(expr, rules)
    assert parser.parse('ab')
    assert parser.parse('a')
    assert parser.parse('b')
    assert parser.parse('') is False

def test_accept_opt():
    expr = NonTerminal('expr')
    rules = { expr: Opt(Terminal('a')) }
    parser = Parser(expr, rules)
    assert parser.parse('ab') is False
    assert parser.parse('a')
    assert parser.parse('b') is False
    assert parser.parse('') is None

def test_accept_arithmetic_grammar():
    expr = NonTerminal('expr')
    sum_ = NonTerminal('sum')
    product = NonTerminal('product')
    power = NonTerminal('power')
    value = NonTerminal('value')

    rules = {
        expr: sum_,
        sum_: product + Many((Terminal('+') | Terminal('-')) + product),
        product: power + Many((Terminal('*') | Terminal('/')) + power),
        power: value + Opt(Terminal('^') + value),
        value: TerminalR(r'[a-z0-9]+') |
        (Terminal('(') + expr + Terminal(')'))      
    }

    parser = Parser(expr, rules)

    assert parser.parse('a+a')
    assert parser.parse('(a+aaa)^(c*d/a)')
    assert parser.parse('(a-a-a-(a*b+(1-1)))+1')
    assert parser.parse('((()))') is False
    assert parser.parse('((((a))') is False
    assert parser.parse('(a^a^a)') is False