import random
# internal modules
from algo.math.expressions import Expression
from algo.math.int_gen import (
    genRandIntByRandOfNDigs,
    genRandIntLsByRandOfNDigs,
    genMulDivOps,
)
from algo.math.int_misc import isInt
from ex_base import ExerciseBase


class FourOperations(ExerciseBase):
    """
    Levels (w/ negative numbers)
    1. only + & -, 3 - 6 digits, 2 - 4 numbers
    2. only * & /, 2 - 3 digits, divisor 1 - 2 digits, 2 - 4 groups
    3. all 4 ops, product up to 6 digits, divisor up to 3 digits, 2 groups
    4. all 4 ops, product up to 6 digits, divisor up to 3 digits, 4 groups
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4
        self.exp = None

    def generateExercise(self):
        if self.level == 0:
            # level 1
            operands = genRandIntLsByRandOfNDigs(
                n=random.randint(2, 4),
                minNDigs=3,
                maxNDigs=6,
            )
            self.exp = Expression(
                operands,
                operators=["+", "-"],
                applyRandomNegation=True,
                shuffleOperatorsWReplacement=True,
            )
        elif self.level == 1:
            # level 2
            self.exp = self.__createMulDivExp()
        else:
            # level 3 or up
            nGrps = 2 if self.level == 2 else 4
            isMulDivGrp = [1] * 2 + [random.choice([0, 1]), 0][:nGrps - 2]
            random.shuffle(isMulDivGrp)
            grps = [
                self.__createMulDivExp()
                if isMulDivGrp[i] == 1
                else genRandIntByRandOfNDigs(3, 6)
                for i in range(nGrps)
            ]
            self.exp = Expression(
                grps,
                operators=["+", "-"],
                applyRandomNegation=True,
                shuffleOperatorsWReplacement=True,
            )
        return str(self.exp)

    @staticmethod
    def __createMulDivExp():
        """
        generate expression for mul and div
        first operand has [2, 3] number of digits
        all other operands have [1, 2] number of digits
        """
        nOperands = random.randint(2, 4)
        operands, operators = genMulDivOps(nOperands, [2, 3], [1, 2])
        return Expression(
            operands,
            operators,
            applyRandomNegation=True
        )

    def validateAnswer(self, q, a):
        if isInt(a):
            return 0 if int(a) == round(self.exp.eval()) else 1
            # the following is for debug only
            # return 0 if round(eval(q)) == round(self.exp.eval()) else 1
        return -1
