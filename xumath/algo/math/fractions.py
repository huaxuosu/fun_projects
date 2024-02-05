import random
import re
# internal modules
from .expressions import Expression
from .int_misc import extractAllIntsFrom
from .int_mul_fac import (
    gcd,
    lcm,
)


class Fraction:
    """
    Fraction:
    A fraction is represented as __n / __d, i.e. numerator / denominator
    if __d is None, it is a integer equal to __n
    A fraction can negative, if so, __n < 0
    __d always > 0
    if __d = 1, it is an integer
    """

    @staticmethod
    def chkDenom(denom):
        return isinstance(denom, int) and denom > 0

    @classmethod
    def fromStr(cls, s):
        m = re.search(r"^\s*([+-]?)\s*(\d+)\s*/\s*(\d+)$", s)
        if m:
            sign, num, denom = m.groups()
            i = 0
        else:
            m = re.search(r"^\s*([+-]?)\s*(\d+)\s+(\d+)\s*/\s*(\d+)$", s)
            if not m:
                return None
            sign, i, num, denom = m.groups()
        i, num, denom = map(int, (i, num, denom))
        num += i * denom
        if sign == "-":
            num = -num
        return Fraction(num, denom)

    def __init__(self, num=0, denom=1):
        assert isinstance(num, int) and Fraction.chkDenom(denom)
        # default is an integer of 0
        self.__n = num
        self.__d = denom

    @property
    def num(self):
        return self.__n

    @property
    def denom(self):
        return self.__d

    def copy(self):
        return Fraction(self.__n, self.__d)

    def toFloat(self):
        return float(self.__n) / self.__d

    def simplify(self, fac=None):
        """
        simplify to the most simple form
        """
        if fac is None:
            fac = gcd(abs(self.__n), self.__d) if self.__n != 0 else self.__d
        else:
            assert Fraction.chkDenom(fac) and self.__n % fac == self.__d % fac == 0
        return Fraction(self.__n//fac, self.__d//fac)

    def complicate(self, fac):
        """
        inverse of simplify
        """
        assert Fraction.chkDenom(fac)
        return Fraction(self.__n*fac, self.__d*fac)

    def changeDenom(self, denom):
        """
        set denom to a new value
        """
        assert Fraction.chkDenom(denom)
        if denom > self.__d:
            assert denom % self.__d == 0
            return self.complicate(denom // self.__d)
        assert self.__d % denom == 0
        return self.simplify(self.__d // denom)

    def isIdenticalTo(self, other):
        assert isinstance(other, Fraction)
        return self.__n == other.__n and self.__d == other.__d

    ###
    # Operators overloading
    ###
    def __neg__(self):
        return Fraction(-self.__n, self.__d)

    def __add__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        # least common denom
        lcd = lcm(self.__d, other.__d)
        return Fraction(
            self.__n * (lcd // self.__d) + other.__n * (lcd // other.__d),
            lcd,
        ).simplify()

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        # least common denom
        lcd = lcm(self.__d, other.__d)
        return Fraction(
            self.__n * (lcd // self.__d) - other.__n * (lcd // other.__d),
            lcd,
        ).simplify()

    def __mul__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction(
            self.__n * other.__n,
            self.__d * other.__d,
        ).simplify()

    def __truediv__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction(
            self.__n * other.__d,
            self.__d * other.__n,
        ).simplify()

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __mod__(self, other):
        raise NotImplementedError

    def __pow__(self, p):
        return Fraction(
            self.__n ** p,
            self.__d ** p,
        ).simplify()

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d == self.__d * other.__n
        # other could be just a number
        return abs(self.__n/self.__d - other) < 1e-16

    def __ne__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d != self.__d * other.__n
        # other could be just a number
        return abs(self.__n / self.__d - other) >= 1e-16

    def __lt__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d < self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d < other

    def __gt__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d > self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d > other

    def __le__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d <= self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d <= other

    def __ge__(self, other):
        if isinstance(other, Fraction):
            return self.__n * other.__d >= self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d >= other


class FractionExpression(Expression):
    """
    Math expression for fractions
    """
    SUPPORTED_VAL_CLASSES = {Fraction}
    SUPPORTED_OPERATORS = ["**", "*", "/", "//", "+", "-"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return str(FractionExpressionRepr(self))


class FractionExpressionRepr:
    """
    A representation in strings for FractionExpression
    """
    def __init__(self, expOrFrac):
        """
        Fraction strings are represented in three rows
         -num
        -------
         denom
        """
        assert isinstance(expOrFrac, FractionExpression) or isinstance(expOrFrac, Fraction)
        self.__up = ""
        self.__mid = ""
        self.__low = ""
        if FractionExpression.isSupportedValType(expOrFrac):
            self.fromFraction(expOrFrac)
        else:
            self.fromExpression(expOrFrac)

    def reset(self):
        self.__up = self.__mid = self.__low = ""

    def fromFraction(self, frac: Fraction):
        num, denom = frac.num, frac.denom
        i = abs(num) // denom if random.random() < 0.5 else 0
        if i > 0:
            num = abs(num) - i * denom
            if num < 0:
                i = -i
        num, denom, i = str(num), str(denom), str(i) if i != 0 else ""
        # len
        k = max(len(num), len(denom))
        self.__up = " "*(len(i)+1) + " "*((k-len(num))//2) + num + " "*((k-len(num)+1)//2 + 1)
        self.__mid = i + "-"*(len(self.__up) - len(i))
        self.__low = " "*(len(i)+1) + " "*((k-len(denom))//2) + denom + " "*((k-len(denom)+1)//2 + 1)
        if i and i[0] == "-":
            self.addOuterBracket()

    def fromExpression(self, exp: FractionExpression):

        def __precedence(x):
            return x.precedence if isinstance(x, Expression) else 0

        if not exp.exps:
            self.reset()
            return
        s = FractionExpressionRepr(exp.exps[0])
        curPrecedence = __precedence(exp.exps[0])
        for i, op in enumerate(exp.ops):
            opPrecedence = exp.__class__.getOpPrecedences(op)
            if curPrecedence > opPrecedence:
                s.addOuterBracket()
            s.addOpStr(op)
            nxtExpOrVal = FractionExpressionRepr(exp.exps[i + 1])
            if __precedence(exp.exps[i + 1]) >= opPrecedence:
                nxtExpOrVal.addOuterBracket()
            s.add(nxtExpOrVal)
            curPrecedence = opPrecedence
        if exp.sign == -1:
            s.addNegation()
        return str(s)

    def addOuterBracket(self):
        self.__up = " " + self.__up + " "
        self.__mid = "(" + self.__mid + ")"
        self.__low = " " + self.__low + " "

    def addOpStr(self, op, sep=" "):
        self.__up += sep + " "*len(op)
        self.__mid += sep + op
        self.__low += sep + " "*len(op)

    def add(self, other, sep=" "):
        self.__up += sep + other.__up
        self.__mid += sep + other.__mid
        self.__low += sep + other.__low

    def addNegation(self):
        assert bool(self.__mid)
        if self.__mid[0] == "(":
            self.__up = " " + self.__up
            self.__mid = "-" + self.__mid
            self.__low = " " + self.__low
            return

        upNums = extractAllIntsFrom(self.__up)
        midNums = extractAllIntsFrom(self.__mid)
        lowNums = extractAllIntsFrom(self.__low)
        if re.search(r"^[-\s\d]+$", self.__mid) and len(upNums) == 1 and len(lowNums) == 1:
            assert len(midNums) <= 1
            frac = Fraction.fromStr("%d %d/%d" % (midNums[0] if midNums else 0, upNums[0], lowNums[0]))
            self.reset()
            self.add(FractionExpressionRepr(frac), sep="")
        else:
            # we need to add brackets first
            self.addOuterBracket()
            self.addNegation()

    def __str__(self):
        return "\n".join((self.__up, self.__mid, self.__low))
