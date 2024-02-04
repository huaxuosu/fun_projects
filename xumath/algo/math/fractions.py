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

    def __init__(self, num=0, denom=1):
        assert(isinstance(num, int) and Fraction.chkDenom(denom))
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
            assert(Fraction.chkDenom(fac) and self.__n % fac == self.__d % fac == 0)
        return Fraction(self.__n//fac, self.__d//fac)

    def complicate(self, fac):
        """
        inverse of simplify
        """
        assert(Fraction.chkDenom(fac))
        return Fraction(self.__n*fac, self.__d*fac)

    def changeDenom(self, denom):
        """
        set denom to a new value
        """
        assert(Fraction.chkDenom(denom))
        if denom > self.__d:
            assert(denom % self.__d == 0)
            return self.complicate(denom // self.__d)
        assert(self.__d % denom == 0)
        return self.simplify(self.__d // denom)

    def isIdenticalTo(self, other):
        assert(isinstance(other, Fraction))
        return self.__n == other.__n and self.__d == other.__d

    ###
    # Operators overloading
    ###
    def __neg__(self):
        return Fraction(-self.__n, self.__d)

    def __add__(self, other):
        assert (isinstance(other, Fraction))
        # least common denom
        lcd = lcm(self.__d, other.__d)
        return Fraction(
            self.__n * (lcd // self.__d) + other.__n * (lcd // other.__d),
            lcd,
        ).simplify()

    def __sub__(self, other):
        assert (isinstance(other, Fraction))
        # least common denom
        lcd = lcm(self.__d, other.__d)
        return Fraction(
            self.__n * (lcd // self.__d) - other.__n * (lcd // other.__d),
            lcd,
        ).simplify()

    def __mul__(self, other):
        assert (isinstance(other, Fraction))
        return Fraction(
            self.__n * other.__n,
            self.__d * other.__d,
        ).simplify()

    def __truediv__(self, other):
        assert (isinstance(other, Fraction))
        return Fraction(
            self.__n * other.__d,
            self.__d * other.__n,
        ).simplify()

    def __pow__(self, p):
        return Fraction(
            self.__n ** p,
            self.__d ** p,
        ).simplify()

    def __eq__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d == self.__d * other.__n

    def __ne__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d != self.__d * other.__n

    def __lt__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d < self.__d * other.__n

    def __gt__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d > self.__d * other.__n

    def __le__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d <= self.__d * other.__n

    def __ge__(self, other):
        assert(isinstance(other, Fraction))
        return self.__n * other.__d >= self.__d * other.__n


class FractionExpression:
    """
    Math expression for fractions
    it contains fractions and operators
    exp_1 operator_1 exp_2 operator_2 ...
    exp_i can be a Fraction or a FractionExpression
    """
    def __init__(self):
        self.__exps = []
        self.__ops = []

    def __repr__(self):
        pass