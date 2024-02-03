import random


def genRandIntByNDigs(minNDigs, maxNDigs=None):
    """
    generate a random integer in range of
    [10^(minNDigs-1), 10^maxNDigs - 1]
    Prob(x) is uniform
    """
    maxNDigs = maxNDigs or minNDigs
    return random.randint(10**(minNDigs-1), 10**maxNDigs-1)


def genRandIntLsByNDigs(n, minNDigs, maxNDigs=None):
    """
    generate a list of random integers in range of
    [10^(minNDigs-1), 10^maxNDigs - 1]
    Prob(x) is uniform
    """
    return [genRandIntByNDigs(minNDigs, maxNDigs) for _ in range(n)]


def genRandIntByRandOfNDigs(minNDigs, maxNDigs=None):
    """
    generate a random integer with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    """
    maxNDigs = maxNDigs or minNDigs
    return genRandIntByNDigs(random.randint(minNDigs, maxNDigs))


def genRandIntLsByRandOfNDigs(n, minNDigs, maxNDigs=None):
    """
    generate a list of random integers with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    """
    return [genRandIntByRandOfNDigs(minNDigs, maxNDigs) for _ in range(n)]
