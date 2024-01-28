import random
# internal modules
from ex_base import ExerciseBase


class ExSimpleOpBase(ExerciseBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4

    def generateExercise(self):
        raise NotImplementedError

    def validateAnswer(self, q, a):
        if a.isdigit() or (a.startswith("-") and a[1:].isdigit()):
            return 0 if int(a) == eval(q) else 1
        return -1

    def generateTwoOperands(self, n1Ranges=None, n2Ranges=None):
        n1Ranges = n1Ranges or [
            [1, 1, 10, 100],
            [9, 9, 99, 999_999],
        ]
        n2Ranges = n2Ranges or [
            [1, 10, 10, 100],
            [9, 99, 99, 999_999],
        ]
        assert(len(n1Ranges) == len(n2Ranges) == 2)
        assert(len(n1Ranges[0]) == len(n1Ranges[1]) == self.nLevels)
        assert(len(n2Ranges[0]) == len(n2Ranges[1]) == self.nLevels)
        n1 = random.randint(n1Ranges[0][self.level], n1Ranges[1][self.level])
        n2 = random.randint(n2Ranges[0][self.level], n2Ranges[1][self.level])
        return n1, n2


class Addition(ExSimpleOpBase):
    def generateExercise(self):
        return "{} + {}".format(*self.generateTwoOperands())


class Subtraction(ExSimpleOpBase):
    def generateExercise(self):
        return "{1:} - {0:}".format(*self.generateTwoOperands())


class Multiplication(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1Ranges = [
            [1, 1, 11, 111, 111],
            [9, 9, 99, 999, 999],
        ]
        n2Ranges = [
            [1, 11, 111, 111, 1111],
            [9, 99, 999, 999, 999_999],
        ]
        return "{1:} * {0:}".format(*self.generateTwoOperands(n1Ranges, n2Ranges))


class Division(ExSimpleOpBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        n1Ranges = [
            [1, 1, 1, 11, 11],
            [9, 9, 9, 99, 99],
        ]
        n2Ranges = [
            [1, 11, 111, 111, 1111],
            [9, 99, 999, 999, 999_999],
        ]
        return "{1:} // {0:}".format(*self.generateTwoOperands(n1Ranges, n2Ranges))
