# internal modules
from exercise import ExerciseBase


class Multiplication(ExerciseBase):
    def generateExercise(self):
        return "{1:} * {0:}".format(*self.generateTwoOperands())
