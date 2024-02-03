import random
# internal modules
from algo.math.int_gen import (
    genRandIntByRandOfNDigs,
    genRandIntLsByRandOfNDigs,
)
from algo.ex_gen_base import (
    applyNegationToVal,
    genExFromOps,
)
from algo.ex_gen_int import ExGrpForMulDivGen
from algo.ex_validate_int import evalSimpleEq
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
        # exercise generator for mul and div
        # first operand has [2, 3] number of digits
        # all other operands have [1, 2] number of digits
        self.mulDivGrpGen = ExGrpForMulDivGen([2, 3], [1, 2])

    def generateExercise(self):
        if self.level == 0:
            # level 1
            operands = genRandIntLsByRandOfNDigs(
                n=random.randint(2, 4),
                minNDigs=3,
                maxNDigs=6,
            )
            return genExFromOps(
                operands,
                operators=["+", "-"],
                applyNegation=True,
                shuffleOperatorsWReplacement=True,
            )
        elif self.level == 1:
            # level 2
            return self.mulDivGrpGen.genEx(nOperands=random.randint(2, 4))
        else:
            # level 3 or up
            nGrps = 2 if self.level == 2 else 4
            isMulDivGrp = [1] * 2 + [random.choice([0, 1]), 0][:nGrps - 2]
            random.shuffle(isMulDivGrp)
            grps = [
                self.mulDivGrpGen.genEx(nOperands=random.randint(2, 4))
                if isMulDivGrp[i] == 1
                else applyNegationToVal(genRandIntByRandOfNDigs(3, 6))
                for i in range(nGrps)
            ]
            return genExFromOps(
                grps,
                operators=["+", "-"],
                applyNegation=False,
                shuffleOperatorsWReplacement=True,
            )

    def validateAnswer(self, q, a):
        return evalSimpleEq(q, a)
