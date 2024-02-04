# internal modules
from algo.math.expressions import Expression
from algo.math.int_gen import genRandIntByRandOfNDigs
from algo.math.int_misc import isInt
from ex_base import ExerciseBase


class ExSimpleOpBase(ExerciseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4
        # Expression
        self.exp = None

    def generateExercise(self):
        return str(self.exp)

    def genExpForOneOp(self, op, n1NDigRanges=None, n2NDigRanges=None):
        n1NDigRanges = n1NDigRanges or [[1], [2], [2], [3, 6]]
        n2NDigRanges = n2NDigRanges or [[1], [1], [2], [3, 6]]
        n1 = genRandIntByRandOfNDigs(*n1NDigRanges[self.level])
        n2 = genRandIntByRandOfNDigs(*n2NDigRanges[self.level])
        self.exp = Expression([n1, n2], op)

    def validateAnswer(self, q, a):
        if isInt(a):
            return 0 if int(a) == round(self.exp.eval()) else 1
            # the following is for debug only
            # return 0 if round(eval(q)) == round(self.exp.eval()) else 1
        return -1


class Addition(ExSimpleOpBase):
    def generateExercise(self):
        ExSimpleOpBase.genExpForOneOp(self, "+")
        return ExSimpleOpBase.generateExercise(self)


class Subtraction(ExSimpleOpBase):
    def generateExercise(self):
        ExSimpleOpBase.genExpForOneOp(self, "-")
        return ExSimpleOpBase.generateExercise(self)


class Multiplication(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1NDigRanges = [[1], [2], [3], [3], [4, 6]]
        n2NDigRanges = [[1], [1], [2], [3], [3]]
        ExSimpleOpBase.genExpForOneOp(self, "*", n1NDigRanges, n2NDigRanges)
        return ExSimpleOpBase.generateExercise(self)


class Division(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1NDigRanges = [[1], [2], [3], [3], [4, 6]]
        n2NDigRanges = [[1], [1], [1], [2], [2, 3]]
        ExSimpleOpBase.genExpForOneOp(self, "//", n1NDigRanges, n2NDigRanges)
        return ExSimpleOpBase.generateExercise(self)
