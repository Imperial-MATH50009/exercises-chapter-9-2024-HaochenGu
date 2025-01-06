import numbers

class Expression:

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

    symbol = None
    Procedence = None
    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        a = self.operands[0]
        b = self.operands[1]
        if self.Procedence > a.Procedence or self.Procedence > b.Procedence:
            if self.Procedence > a.Procedence and self.Procedence > b.Procedence:
                return f"({str(a)}) {self.symbol} ({str(b)})"
            elif self.Procedence > a.Procedence:
                return f"({str(a)}) {self.symbol} {str(b)}"
            else:
                return f"{str(a)} {self.symbol} ({str(b)})"
        else:
            return f"{str(a)} {self.symbol} {str(b)}"

class Add(Operator):
    Procedence = 0
    symbol = '+'

class Sub(Operator):
    Procedence = 0
    symbol = '-'

class Mul(Operator):
    Procedence = 1
    symbol = '*'

class Div(Operator):
    Procedence = 1
    symbol = '/'

class Pow(Operator):
    Procedence = 2
    symbol = '^'


class Terminal(Expression):

    Procedence = 4

    def __init__(self, value, *operands):
        super().__init__(*operands)
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class Number(Terminal):

    def __init__(self, value, *operands):
        super().__init__(value, *operands)
        if not isinstance(value, numbers.Number):
            raise TypeError("Need to be number")

class Symbol(Terminal):

    def __init__(self, value, *operands):
        super().__init__(value, *operands)
        if not isinstance(value, str):
            raise TypeError("Need to be string")


def postvisitor(expr, fn, **kwargs):
    return fn(expr,
              *(postvisitor(c, fn, **kwargs) for c in expr.operands),
              **kwargs)