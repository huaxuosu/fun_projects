import random
import functools
import operator
# internal modules
from .math.int_mul_fac import gcd
from .rand.gen_ints import genRandIntByRandOfNDigs
from .ex_gen_base import genExFromOps


def genExForOneBinaryOp(op, n1NDigRange, n2NDigRange):
    """
    n1NDigRange and n2NDigRange specify the # of digits of the operands in format [min # digits, max # of digits]
    """
    n1 = genRandIntByRandOfNDigs(*n1NDigRange)
    n2 = genRandIntByRandOfNDigs(*n2NDigRange)
    return genExFromOps([n1, n2], [op], applyNegation=False)


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
