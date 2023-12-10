import random
# internal modules
from exercise import ExerciseBase


class Multiplication(ExerciseBase):
    def __init__(self):
        super().__init__()
        self.nLevels = 5

    def generateTwoOperands(self):
        n1Ranges = [
            [1, 1, 11, 111, 111],
            [9, 9, 99, 999, 999],
        ]
        n2Ranges = [
            [1, 11, 111, 111, 1111],
            [9, 99, 999, 999, 999_999],
        ]
        n1 = random.randint(n1Ranges[0][self.level], n1Ranges[1][self.level])
        n2 = random.randint(n2Ranges[0][self.level], n2Ranges[1][self.level])
        return n1, n2

    def generateExercise(self):
        return "{1:} * {0:}".format(*self.generateTwoOperands())
