import random
# internal modules
from .common import zipTwoLists


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
