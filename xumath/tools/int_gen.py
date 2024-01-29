import random
# internal modules
from .common import zipTwoLists


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
    maxNDigs = maxNDigs or minNDigs
    return [random.randint(10**(minNDigs-1), 10**maxNDigs-1) for _ in range(n)]


def genRandIntByRandOfNDigs(minNDigs, maxNDigs):
    """
    generate a random integer with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    """
    return genRandIntByNDigs(random.randint(minNDigs, maxNDigs))


def genRandIntLsByRandOfNDigs(n, minNDigs, maxNDigs):
    """
    generate a list of random integers with the number of digits
    in range [minNDigs, maxNDigs]
    The main difference between genRandIntByRandOfNDigs and genRandIntByNDigs
    is that Prob(x) is not uniform, but Prob(log10(x)) is uniform
    """
    return [genRandIntByNDigs(random.randint(minNDigs, maxNDigs)) for _ in range(n)]


def applyNegationToVal(v):
    """
    apply negation by random
    """
    assert(isinstance(v, int) or v.isdigit())
    return random.choice(["(-{})", "{}"]).format(v)


def applyNegationToVals(vals):
    """
    return a list of strings with all the values applied with negation by random
    """
    return list(map(applyNegationToVal, vals))


def genEqFromOps(operands, operators, applyNegation=False):
    """
    Generate the equation from the operands and operators
    """
    if applyNegation:
        operands = applyNegationToVals(operands)
    return " ".join(map(str, zipTwoLists(operands, operators)))
