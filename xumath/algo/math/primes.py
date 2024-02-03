import math
import random
# import functools
# import operator
# import numpy as np


def findPrimes(n):
    if n < 2:
        return []

    isPrimeLs = [True] * (n + 1)
    isPrimeLs[0] = isPrimeLs[1] = False
    ix = math.ceil(math.sqrt(n+1))
    for i in range(2, ix):
        if isPrimeLs[i]:
            isPrimeLs[i * i:n + 1:i] = [False] * ((n - i * i + i) // i)
    primes = [i for i in range(2, n+1) if isPrimeLs[i]]
    return primes


def isPrime(n):
    if n & 1 == 0 or n % 10 == 5 or sum(map(int, str(n))) % 3 == 0:
        return False
    return findPrimes(n)[-1] == n


def primeFactorization(n):
    if n <= 3:
        return [n]

    ans = []
    primes = findPrimes(n)
    for p in primes:
        while n % p == 0:
            ans.append(p)
            n //= p
        if n < p:
            if n > 1:
                ans.append(n)
            break
    return ans


class IntWSmallPrimeFactors:
    """
    This class generates an int with only small prime factors
    """
    def __init__(self, maxFac: int):
        """
        maxFac: biggest prime factor
        if maxFax is not prime, the nearest left prime will be used
        """
        # primes before maxFac
        self.primes = findPrimes(maxFac)

    def genInt(self, maxNumPrimeFactors, maxVal):
        """
        generate an int with up to maxNumPrimeFactors prime factors
        and <= maxVal
        """
        n = 1
        for _ in range(maxNumPrimeFactors):
            p = random.choice(self.primes)
            if n * p > maxVal and not isPrime(n):
                break
            n *= p
        return n


"""
def findPrimesFast(n):
    if n < 2:
        return []

    isPrimeVec = np.ones(n + 1, int)
    isPrimeVec[0] = isPrimeVec[1] = 0
    ix = math.ceil(math.sqrt(n+1))
    for i in range(2, ix):
        if isPrimeVec[i] == 1:
            isPrimeVec[i * i:n + 1:i] = 0
    primes = np.where(isPrimeVec == 1)[0]
    return primes


def isPrime(n):
    if n & 1 == 0 or n % 10 == 5 or sum(map(int, str(n))) % 3 == 0:
        return False
    return findPrimesFast(n)[-1] == n


def primeFactorizationFast(n):
    if n <= 3:
        return [n]

    ans = []
    primes = findPrimesFast(n)
    while n > 1:
        found = primes[np.where(n % primes == 0)[0]]
        ans.extend(found)
        n //= functools.reduce(operator.mul, found)
    return sorted(ans)
"""
