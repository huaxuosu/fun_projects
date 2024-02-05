import random
# internal modules
from algo.math.fractions import (
    Fraction,
    FractionExpression,
)
from algo.math.int_gen import (
    genRandIntLsByNDigs,
)
from algo.math.int_primes import IntWSmallPrimeFactors
from ex_base import ExerciseBase


class ExFractions(ExerciseBase):
    """
    Levels
    1. fraction simplification
    2. fraction addition and subtraction
    3. fraction comparison
    4. fraction multiplication
    5. fraction division
    6. mixed
    """

    ANSWER_FORMAT = "integer_part dividend / divisor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 6
        self.exp = None
        # generate int with small primes < 20
        self.intWSmallPrimeFacsGen = IntWSmallPrimeFactors(20)

    def generateExercise(self):
        if self.level == 0:
            # level 1
            return self.__genFrSim()

    def __genFrSim(self):
        operands = genRandIntLsByNDigs(
            n=2,
            minNDigs=1,
            maxNDigs=2,
            nonPrime=True,
            baseFac=self.intWSmallPrimeFacsGen.genInt(1) if random.random() < 2.0 / 3 else 1,
        )
        self.exp = FractionExpression(Fraction(*operands))
        return "Simplify the following fraction:\n%s" % str(self.exp)

    def validateAnswer(self, q, a):
        ans = Fraction.fromStr(a)
        if ans is not None:
            print(ans, self.exp)
            return 0 if ans.isIdenticalTo(self.exp.eval()) else 1
        return -1
