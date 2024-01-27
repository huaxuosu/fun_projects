from ex_base import ExerciseBase


class Addition(ExerciseBase):
    def generateExercise(self):
        return "{} + {}".format(*self.generateTwoOperands())


class Subtraction(ExerciseBase):
    def generateExercise(self):
        return "{1:} - {0:}".format(*self.generateTwoOperands())


class Multiplication(ExerciseBase):
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


class Division(ExerciseBase):
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
