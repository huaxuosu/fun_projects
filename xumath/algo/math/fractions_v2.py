import re
# internal modules
from .int_mul_fac import (
    gcd,
    lcm,
)
from .constants import eps

# debug mode
FRACTION_V2_DEBUG = False


class FractionV2:
    """
    FractionV2:
    A fraction is represented as __n / __d, i.e. numerator / denominator
    if __d is 1, it is a integer equal to __n
    A fraction can be negative, if so, __n < 0
    __d always > 0
    """

    @staticmethod
    def chkDenom(denom):
        return isinstance(denom, int) and denom > 0

    @classmethod
    def fromStr(cls, s):
        if re.search(r"^\s*([+-]?)\s*(\d+)\s*$", s):
            # it is an integer
            return cls(int(s))

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
        return cls(num, denom)

    def __init__(self, num=0, denom=1):
        if denom is None:
            denom = 1
        if denom < 0:
            denom, num = -denom, -num
        assert isinstance(num, int) and self.__class__.chkDenom(denom)
        # default is an integer of 0
        self.__n = num
        self.__d = denom

    @property
    def num(self):
        return self.__n

    @property
    def denom(self):
        return self.__d

    def __copy__(self):
        return FractionV2(self.__n, self.__d)

    def __float__(self):
        return float(self.__n) / self.__d

    def simplify(self, fac=None):
        """
        simplify to the most simple form
        """
        if fac is None:
            fac = gcd(abs(self.__n), self.__d) if self.__n != 0 else self.__d
        else:
            assert self.__class__.chkDenom(fac) and self.__n % fac == self.__d % fac == 0
        return FractionV2(self.__n // fac, self.__d // fac)

    def complicate(self, fac):
        """
        inverse of simplify
        """
        assert self.__class__.chkDenom(fac)
        return FractionV2(self.__n * fac, self.__d * fac)

    def changeDenom(self, denom):
        """
        set denom to a new value
        """
        assert self.__class__.chkDenom(denom)
        if denom > self.__d:
            assert denom % self.__d == 0
            return self.complicate(denom // self.__d)
        assert self.__d % denom == 0
        return self.simplify(self.__d // denom)

    def isIdenticalTo(self, other):
        assert isinstance(other, FractionV2)
        return self.__n == other.__n and self.__d == other.__d

    def __str__(self):
        return "(%d/%d)" % (self.__n, self.__d) if self.__d > 1 else str(self.__n)

    def __repr__(self):
        return str(self)

    ###
    # Operators overloading
    ###
    def __neg__(self):
        return FractionV2(-self.__n, self.__d)

    def __add__(self, other):
        if not isinstance(other, FractionV2):
            other = FractionV2(other)
        # least common denom
        lcdenom = lcm(self.__d, other.__d)
        return FractionV2(
            self.__n * (lcdenom // self.__d) + other.__n * (lcdenom // other.__d),
            lcdenom,
        ).simplify()

    def __sub__(self, other):
        if not isinstance(other, FractionV2):
            other = FractionV2(other)
        # least common denom
        lcdenom = lcm(self.__d, other.__d)
        return FractionV2(
            self.__n * (lcdenom // self.__d) - other.__n * (lcdenom // other.__d),
            lcdenom,
        ).simplify()

    def __mul__(self, other):
        if not isinstance(other, FractionV2):
            other = FractionV2(other)
        return FractionV2(
            self.__n * other.__n,
            self.__d * other.__d,
        ).simplify()

    def __truediv__(self, other):
        if not isinstance(other, FractionV2):
            other = FractionV2(other)
        return FractionV2(
            self.__n * other.__d,
            self.__d * other.__n,
        ).simplify()

    def __floordiv__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __pow__(self, p):
        return FractionV2(
            self.__n ** p,
            self.__d ** p,
        ).simplify()

    def __eq__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d == self.__d * other.__n
        # other could be just a number
        return abs(self.__n/self.__d - other) < eps

    def __ne__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d != self.__d * other.__n
        # other could be just a number
        return abs(self.__n / self.__d - other) >= eps

    def __lt__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d < self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d < other

    def __gt__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d > self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d > other

    def __le__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d <= self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d <= other

    def __ge__(self, other):
        if isinstance(other, FractionV2):
            return self.__n * other.__d >= self.__d * other.__n
        # other could be just a number
        return self.__n / self.__d >= other
