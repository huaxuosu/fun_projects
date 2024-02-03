import random
# internal modules
from .tools.common import zipTwoLists


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


def genExFromOps(operands, operators, applyNegation=False, shuffleOperatorsWReplacement=False):
    """
    Generate the equation from the operands and operators
    """
    if shuffleOperatorsWReplacement:
        operators = [random.choice(operators) for _ in range(len(operands) - 1)]
    assert(len(operands) - len(operands) == 1)
    if applyNegation:
        operands = applyNegationToVals(operands)
    return " ".join(map(str, zipTwoLists(operands, operators)))
