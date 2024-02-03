# internal modules
from algo.ex_gen_int import genExForOneBinaryOp
from algo.ex_validate_int import evalSimpleEq
from ex_base import ExerciseBase


class ExSimpleOpBase(ExerciseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4

    def generateExercise(self):
        raise NotImplementedError

    def genExForOneBinaryOp(self, op, n1NDigRanges=None, n2NDigRanges=None):
        n1NDigRanges = n1NDigRanges or [[1], [2], [2], [3, 6]]
        n2NDigRanges = n2NDigRanges or [[1], [1], [2], [3, 6]]
        return genExForOneBinaryOp(
            op,
            n1NDigRanges[self.level],
            n2NDigRanges[self.level],
        )

    def validateAnswer(self, q, a):
        return evalSimpleEq(q, a)


class Addition(ExSimpleOpBase):
    def generateExercise(self):
        return ExSimpleOpBase.genExForOneBinaryOp(self, "+")


class Subtraction(ExSimpleOpBase):
    def generateExercise(self):
        return ExSimpleOpBase.genExForOneBinaryOp(self, "-")


class Multiplication(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1NDigRanges = [[1], [2], [3], [3], [4, 6]]
        n2NDigRanges = [[1], [1], [2], [3], [3]]
        return ExSimpleOpBase.genExForOneBinaryOp(self, "*", n1NDigRanges, n2NDigRanges)


class Division(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1NDigRanges = [[1], [2], [3], [3], [4, 6]]
        n2NDigRanges = [[1], [1], [1], [2], [2, 3]]
        return ExSimpleOpBase.genExForOneBinaryOp(self, "//", n1NDigRanges, n2NDigRanges)
