import random
# internal modules
from algo.math.expressions_v2 import ExpressionV2
from algo.math.fractions_v2 import (
    FractionV2,
    FRACTION_V2_DEBUG,
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
    2. fraction comparison
    3. fraction addition and subtraction
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
            operands = tuple(self.__genFr() for _ in range(2))
            self.exp = ExpressionV2(operands[0], "-", operands[1])
            return "Compare %s to %s (1 bigger, -1 smaller, 0 equal)" % operands
        elif self.level <= 4:
            # levels 3, 4, and 5
            self.exp = self.__genFrSimpleExp(self.level-2)
        else:
            # mixed
            grps = [self.__genFrSimpleExp(2) for _ in range(2)]
            self.exp = ExpressionV2.make(
                grps,
                ["+", "-"],
                applyRandomNegation=True,
                shuffleOperatorsWReplacement=True
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

    def __genFrSimpleExp(self, expType):
        # expType, 0: +/-, 1: *, 2: /, 3: */-
        assert 0 <= expType <= 3
        operators = [["+", "-"], ["*"], ["/"], ["*", "/"]][expType]
        operands = tuple(self.__genFr() for _ in range(random.choice([2, 3])))
        return ExpressionV2.make(
            operands,
            operators,
            applyRandomNegation=True,
            shuffleOperatorsWReplacement=True,
        )

    def validateAnswer(self, q, a):
        a = a.strip()
        ans = FractionV2.fromStr(a)
        if ans is not None:
            expected = self.exp.eval() if self.level > 0 else self.exp.simplify()
            if FRACTION_V2_DEBUG:
                print(ans, expected)
            if self.level == 1:
                expected = FractionV2(expected > 0 and 1 or (expected < 0 and -1 or 0))
            return 0 if ans.isIdenticalTo(expected) else 1
        return -1
