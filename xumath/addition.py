# internal modules
from exercise import ExerciseBase


class Addition(ExerciseBase):
    def generateExercise(self):
        return "{} + {}".format(*self.generateTwoOperands())
