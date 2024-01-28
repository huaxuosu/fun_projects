# internal modules
from ex_base import ExerciseBase


class FourOperations(ExerciseBase):
    """
    Levels (w/ negative numbers)
    1. only + & -, up to 6 digits, 2 - 4 numbers
    2. only * & /, product up to 6 digits, divisor up to 3 digits, 2 groups
    3. all 4 ops, product up to 6 digits, divisor up to 3 digits, 2 groups
    4. all 4 ops, product up to 6 digits, divisor up to 3 digits, 4 groups
    """
    @classmethod
    def validateAnswer(cls, q, a):
        if a.isdigit() or (a.startswith("-") and a[1:].isdigit()):
            return 0 if int(a) == round(eval(q)) else 1
        return -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4

