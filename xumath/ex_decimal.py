import random

from ex_complex_op import FourOperations
from algo.math.float_misc import isANumber
from algo.math.fractions_v2 import FractionV2


class Decimals(FourOperations):
    """
    Levels (w/ negative numbers)
    1. only + & -, 3 - 6 digits, 2 - 4 numbers
    2. only * & /, 2 - 3 digits, divisor 1 - 2 digits, 2 - 4 groups
    3. all 4 ops, product up to 6 digits, divisor up to 3 digits, 2 groups
    4. all 4 ops, product up to 6 digits, divisor up to 3 digits, 4 groups
    5. all 4 ops with brackets, product up to 6 digits, divisor up to 3 digits, 4 groups
    """

    ANSWER_FORMAT = "decimal or fraction"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 0: fraction, 1-3: decimals
        self.nDecPlaces = 0

    def generateExercise(self):
        super().generateExercise()
        self.exp = self.exp.convertToDecimalsByRandomFactors(0, 3)
        self.nDecPlaces = [random.randint(1, 3), 0][random.randint(0, 1)]
        if self.nDecPlaces > 0:
            ansFmt = "round to %d decimal places" % self.nDecPlaces
        else:
            ansFmt = "round to 2 decimal places and convert to a fraction"
        return "%s\n%s" % (str(self.exp), ansFmt)

    def validateAnswer(self, q, a):
        expected = self.exp.eval()
        a = a.strip()
        if self.nDecPlaces > 0:
            if isANumber(a):
                return 0 if float(a) == round(expected, self.nDecPlaces) else 1
                # the following is for debug only
                # return 0 if round(eval(q)) == round(self.exp.eval()) else 1
            return -1
        # fraction
        expected = FractionV2(int(round(expected, 2) * 100), 100).simplify()
        ans = FractionV2.fromStr(a)
        if ans is not None:
            return 0 if ans.isIdenticalTo(expected) else 1
        return -1
