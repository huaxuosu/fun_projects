# internal modules
from ex_base import ExerciseBase


class Factors(ExerciseBase):
    """
    Levels
    1. prime factorization (simple)
    2. factors in a range (simple)
    3. GCD 1
    4. GCD 2
    5. common factors in a range
    6. mixed
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 6

    def generateExercise(self):
        pass

    def validateAnswer(self, q, a):
        pass


class Multiples(ExerciseBase):
    """
    Levels
    1. multiples in a range (simple)
    2. LCM 1
    3. LCM 2
    4. common multiples in a range
    5. mixed
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        pass

    def validateAnswer(self, q, a):
        pass
