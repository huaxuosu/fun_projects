from .rand.gen_ints import genRandIntByRandOfNDigs
from .ex_gen_base import genExFromOps


def genExForOneBinaryOp(op, n1NDigRange, n2NDigRange):
    """
    n1NDigRange and n2NDigRange specify the # of digits of the operands in format [min # digits, max # of digits]
    """
    n1 = genRandIntByRandOfNDigs(*n1NDigRange)
    n2 = genRandIntByRandOfNDigs(*n2NDigRange)
    return genExFromOps([n1, n2], [op], applyNegation=False)


class ExerciseGenerator:
    """
    Generates exercise questions
    """
    def __init__(self):
        pass
