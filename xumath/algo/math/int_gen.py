import random
import math
# internal modules
from .int_primes import isPrime, IntWSmallPrimeFactors
from .int_mul_fac import gcd


def genRandIntByNDigs(minNDigs, maxNDigs=None, nonPrime=False, baseFac=1):
    """
    generate a random integer in range of
    [10^(minNDigs-1), 10^maxNDigs - 1]
    Prob(x) is uniform
    nonPrime: return a non-prime number if true
    baseFac: return a number that is a multiple of baseFac
    """
    maxNDigs = maxNDigs or minNDigs
    ret = None
    while ret is None or (nonPrime and isPrime(ret)):
        ret = random.randint(10**(minNDigs-1), 10**maxNDigs-1)
    if baseFac > 1:
        ret = (ret + baseFac - 1) // baseFac * baseFac
    return ret


def genRandIntLsByNDigs(n, minNDigs, maxNDigs=None, nonPrime=False, baseFac=1):
    """
    generate a list of random integers in range of
    [10^(minNDigs-1), 10^maxNDigs - 1]
    Prob(x) is uniform
    nonPrime: return a non-prime number if true
    baseFac: return a number that is a multiple of baseFac
    """
    return [genRandIntByNDigs(minNDigs, maxNDigs, nonPrime, baseFac) for _ in range(n)]


def genRandIntByRandOfNDigs(minNDigs, maxNDigs=None, nonPrime=False, baseFac=1):
    """
    generate a random integer with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    nonPrime: return a non-prime number if true
    baseFac: return a number that is a multiple of baseFac
    """
    maxNDigs = maxNDigs or minNDigs
    return genRandIntByNDigs(random.randint(minNDigs, maxNDigs), nonPrime=nonPrime, baseFac=baseFac)


def genRandIntLsByRandOfNDigs(n, minNDigs, maxNDigs=None, nonPrime=False, baseFac=1):
    """
    generate a list of random integers with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    nonPrime: return a non-prime number if true
    baseFac: return a number that is a multiple of baseFac
    """
    return [genRandIntByRandOfNDigs(minNDigs, maxNDigs, nonPrime, baseFac) for _ in range(n)]


def genRandIntLsWithRandomGcd(
        n,
        intWSmallPrimeFacsGen: IntWSmallPrimeFactors,
        maxNumPrimeFactorsOfGac,
        maxGcd=math.inf):
    """
    returns the values and their GCD
    """
    fac = intWSmallPrimeFacsGen.genInt(maxNumPrimeFactorsOfGac, maxGcd)
    return [e*fac for e in intWSmallPrimeFacsGen.genPrimes(n)], fac


def genMulDivOps(nOperands, n1NDigRange, n2NDigRange):
    """
    generate a series of operations of mul or div
        it is guaranteed that the division is a clean one
    n1NDigRange: # of digits range for the first operand
    n2NDigRange: # of digits range for all other operands
    """
    operators = [random.choice(["*", "/"]) for _ in range(nOperands - 1)]
    operands = [genRandIntByRandOfNDigs(*n1NDigRange)]
    prodOfDividends = operands[0]
    prodOfDivisors = 1
    for e in operators:
        v = genRandIntByRandOfNDigs(*n2NDigRange)
        if e == "/":
            prodOfDivisors *= abs(v)
        else:
            prodOfDividends *= abs(v)
        operands.append(v)
    operands[0] *= prodOfDivisors // gcd(prodOfDividends, prodOfDivisors)
    return operands, operators
