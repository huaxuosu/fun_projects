import random
import functools
import operator
# internal modules
from .math.int_gen import genRandIntByRandOfNDigs
from .math.int_mul_fac import gcd
from .ex_gen_base import genExFromOps


class ExGrpForMulDivGen:
    """
    Generates exercise questions with mul and div operations
    """
    def __init__(self, n1NDigRange, n2NDigRange):
        """
        n1NDigRange: # of digits range for the first operand
        n2NDigRange: # of digits range for all other operands
        """
        self.n1NDigRange = n1NDigRange
        self.n2NDigRange = n2NDigRange

    def genEx(self, nOperands=2):
        """
        generate exercise with nOperands number of operands
        """
        operators = [random.choice(["*", "/"]) for _ in range(nOperands - 1)]
        operands = [genRandIntByRandOfNDigs(*self.n1NDigRange)]
        dividends = [operands[0]]
        divisors = []
        for e in operators:
            v = genRandIntByRandOfNDigs(*self.n2NDigRange)
            if e == "/":
                divisors.append(v)
            else:
                dividends.append(v)
            operands.append(v)
        if divisors:
            prodOfDividends = functools.reduce(operator.mul, dividends)
            prodOfDivisors = functools.reduce(operator.mul, divisors)
            operands[0] *= prodOfDivisors // gcd(prodOfDividends, prodOfDivisors)
        return genExFromOps(operands, operators, applyNegation=True)
