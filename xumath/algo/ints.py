import collections
# internal modules
from .primes import primeFactorization


def gcd(*args):
    """
    GCD of a list of numbers
    """

    def __gcdBinary(a, b):
        """
        GCD of a and b
        """
        if a > b:
            return gcd(b, a)
        if b % a == 0:
            return a
        return gcd(a, b % a)

    n = len(args)
    assert(n > 1)
    ret = args[0]
    for i in range(1, n):
        ret = __gcdBinary(ret, args[i])
    return ret


def lcm(*args):
    """
    LCM of a list of numbers
    """

    def __lcmBinary(a, b):
        """
        LCM of a and b
        """
        return a * b // gcd(a, b)

    n = len(args)
    assert(n > 1)
    ret = args[0]
    for i in range(1, n):
        ret = __lcmBinary(ret, args[i])
    return ret


def findAllFactors(n, lb=1, ub=None):
    """
    find all factors of n (sorted), including 1 and itself
    """
    assert(n > 1)
    ub = ub or n
    pfs = primeFactorization(n)
    cnts = collections.Counter(pfs)
    pLs = list(cnts.keys())
    k = len(pLs)
    ret = []

    def __helper(i=0, prod=1):
        if i == k:
            ret.append(prod)
            return
        p = pLs[i]
        for m in range(cnts[p]+1):
            f = p**m
            prod *= f
            __helper(i+1, prod)
            prod //= f

    __helper()
    return sorted(e for e in ret if lb <= e <= ub)
