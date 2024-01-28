import random
# internal modules
from ex_base import ExerciseBase
from tools_int_gen import (
    genRandIntByRandOfNDigs,
    genRandIntLsByRandOfNDigs,
    applyNegationToVal,
    genEqFromOps,
)
from tools_int import lcm


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

    def generateExercise(self):
        if self.level == 0:
            # level 1
            nOperands = random.randint(2, 4)
            operands = genRandIntLsByRandOfNDigs(nOperands, 3, 6)
            return self._genAddSubEq(operands, applyNegation=True)
        elif self.level == 1:
            # level 2
            return self._genMulDivGrp(random.randint(2, 4))
        else:
            # level 3 or up
            nGrps = 2 if self.level == 2 else 4
            isSingleVal = [1]*2 + [random.choice([0, 1]), 0][:nGrps-2]
            random.shuffle(isSingleVal)
            grps = [
                self._genMulDivGrp(random.randint(2, 4))
                if isSingleVal[i] == 1
                else applyNegationToVal(genRandIntByRandOfNDigs(3, 6))
                for i in range(nGrps)
            ]
            return self._genAddSubEq(grps, applyNegation=False)

    @staticmethod
    def _genAddSubEq(operands, applyNegation=False):
        nOperands = len(operands)
        operators = [random.choice(["+", "-"]) for _ in range(nOperands - 1)]
        return genEqFromOps(operands, operators, applyNegation=applyNegation)

    @staticmethod
    def _genMulDivGrp(nOperands=2):
        operators = [random.choice(["*", "/"]) for _ in range(nOperands - 1)]
        operands = [genRandIntByRandOfNDigs(2, 3)]
        divisors = []
        for e in operators:
            v = genRandIntByRandOfNDigs(1, 2)
            if e == "/":
                divisors.append(v)
            operands.append(v)
        if divisors:
            operands[0] = lcm(operands[0], *divisors)
        return genEqFromOps(operands, operators, applyNegation=True)

    def validateAnswer(self, q, a):
        if a.isdigit() or (a.startswith("-") and a[1:].isdigit()):
            return 0 if int(a) == round(eval(q)) else 1
        return -1
