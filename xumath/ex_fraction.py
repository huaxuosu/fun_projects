import random
# internal modules
from algo.math.fractions_v2 import (
    FractionV2,
    FractionExpressionV2,
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
            self.exp = self.__genFr()
            return "Simplify the following fraction:\n%s" % str(self.exp)
        elif self.level == 1:
            operands = [self.__genFr() for _ in range(random.choice([2, 3]))]
            self.exp = FractionExpressionV2.make(
                operands,
                ["+", "-"],
                applyRandomNegation=True,
                shuffleOperatorsWReplacement=True,
            )
            return str(self.exp)

    def __genFr(self):
        operands = genRandIntLsByNDigs(
            n=2,
            minNDigs=1,
            maxNDigs=2,
            nonPrime=True,
            baseFac=self.intWSmallPrimeFacsGen.genInt(1) if random.random() < 2.0 / 3 else 1,
        )
        return FractionV2(*operands)

    def validateAnswer(self, q, a):
        ans = FractionV2.fromStr(a)
        if ans is not None:
            expected = self.exp.eval() if self.level > 0 else self.exp.simplify()
            print(ans, expected)
            return 0 if ans.isIdenticalTo(expected) else 1
        return -1
