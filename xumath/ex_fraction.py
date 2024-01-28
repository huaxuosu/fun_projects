# internal modules
from ex_base import ExerciseBase


class Fractions(ExerciseBase):
    """
    Levels
    1. fraction simplification
    2. fraction addition and subtraction
    3. fraction comparison
    4. fraction multiplication
    5. fraction division
    6. mixed
    """

    @classmethod
    def validateAnswer(cls, q, a):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 6
