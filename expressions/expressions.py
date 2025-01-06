"""Expressions class and its hierarchy."""
import numbers
from functools import singledispatch


class Expression:
    """Basic expression class."""

    def __init__(self, *operands):
        self.operands = operands

    def __add__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Add(self, ex)

    def __radd__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Add(ex, self)

    def __sub__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Sub(self, ex)

    def __rsub__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Sub(ex, self)

    def __mul__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Mul(self, ex)

    def __rmul__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Mul(ex, self)

    def __truediv__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Div(self, ex)

    def __rtruediv__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Div(ex, self)

    def __pow__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Pow(self, ex)

    def __rpow__(self, ex):
        if isinstance(ex, numbers.Number):
            ex = Number(ex)
        if isinstance(ex, str):
            ex = Symbol(ex)
        return Pow(ex, self)


class Operator(Expression):
    """Basic operator class inherented from expression."""

    symbol = None
    Procedence = None

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        a = self.operands[0]
        b = self.operands[1]
        if self.Procedence > a.Procedence or self.Procedence > b.Procedence:
            if (
                self.Procedence > a.Procedence
                and self.Procedence > b.Procedence
            ):
                return f"({str(a)}) {self.symbol} ({str(b)})"
            elif self.Procedence > a.Procedence:
                return f"({str(a)}) {self.symbol} {str(b)}"
            else:
                return f"{str(a)} {self.symbol} ({str(b)})"
        else:
            return f"{str(a)} {self.symbol} {str(b)}"


class Add(Operator):
    """Addition."""

    Procedence = 0
    symbol = '+'


class Sub(Operator):
    """Subtraction."""

    Procedence = 0
    symbol = '-'


class Mul(Operator):
    """Multiplication."""

    Procedence = 1
    symbol = '*'


class Div(Operator):
    """Division."""

    Procedence = 1
    symbol = '/'


class Pow(Operator):
    """Power."""

    Procedence = 2
    symbol = '^'


class Terminal(Expression):
    """Basic class for terminal."""

    Procedence = 4

    def __init__(self, value, *operands):
        super().__init__(*operands)
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Number(Terminal):
    """Number."""

    def __init__(self, value, *operands):
        super().__init__(value, *operands)
        if not isinstance(value, numbers.Number):
            raise TypeError("Need to be number")


class Symbol(Terminal):
    """Symbol."""

    def __init__(self, value, *operands):
        super().__init__(value, *operands)
        if not isinstance(value, str):
            raise TypeError("Need to be string")


def postvisitor(expr, evaluate, **kwargs):
    """Implement of DAG."""
    stack = []
    visited = {}
    stack.append(expr)
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            stack.extend(unvisited_children)
        else:
            visited[e] = evaluate(e,
                                  *(visited[o] for o in e.operands),
                                  **kwargs
                                  )

    return visited[expr]


@singledispatch
def differentiate(expr, *children, **var):
    """Differentiate."""
    raise NotImplementedError(f"Cannot differentiate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, *o, var, **kwarg):
    return Number(0)


@differentiate.register(Symbol)
def _(expr, *o, var, **kwarg):
    if expr.value == var:
        return Number(1)
    else:
        return Number(0)


@differentiate.register(Add)
def _(expr, *o, var, **kwarg):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, var, **kwarg):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, var, **kwarg):
    return expr.operands[0] * o[1] + expr.operands[1] * o[0]


@differentiate.register(Div)
def _(expr, *o, var, **kwarg):
    f = expr.operands[0]
    g = expr.operands[1]
    df = o[0]
    dg = o[1]
    return (df * g - f * dg) / (g ** 2)


@differentiate.register(Pow)
def _(expr, *o, var, **kwarg):
    base = expr.operands[0]
    power = expr.operands[1]
    return power * (base ** (power - 1))
