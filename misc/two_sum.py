# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 17:34:58 2023

@author: huaxu
"""
import numpy as np
import math
import functools
import operator

def findPrimesSlow(n):
    if n < 2:
        return []
    
    isPrime = [True]*(n + 1)
    isPrime[0] = isPrime[1] = False
    ix = math.ceil(math.sqrt(n+1))
    for i in range(2, ix):
        if isPrime[i]:
            isPrime[i*i:n+1:i] = [False]*((n-i*i+i)//i)
    primes = [i for i in range(2, n+1) if isPrime[i]]
    return primes


def findPrimes(n):
    if n < 2:
        return []
    
    isPrime = np.ones(n+1, int)
    isPrime[0] = isPrime[1] = 0
    ix = math.ceil(math.sqrt(n+1))
    for i in range(2, ix):
        if isPrime[i] == 1:
            isPrime[i*i:n+1:i] = 0
    primes = np.where(isPrime == 1)[0]
    return primes


def isPrime(n):
    if n & 1 == 0 or n % 10 == 5 or sum(map(int, str(n))) % 3 == 0:
        return False
    return findPrimes(n)[-1] == n


def primeFactorizationSlow(n):
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


def primeFactorization(n):
    if n <= 3:
        return [n]
    
    ans = []
    primes = findPrimes(n)
    while n > 1:
        found = primes[np.where(n % primes == 0)[0]]
        ans.extend(found)
        n //= functools.reduce(operator.mul, found)
    return sorted(ans)
