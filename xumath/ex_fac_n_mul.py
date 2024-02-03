import random
# internal modules
from ex_base import ExerciseBase
from algo.math.primes import (
    primeFactorization,
    IntWSmallPrimeFactors,
)
from algo.ex_validate_int import (
    extractAllIntsFrom,
    parseCommaSepInts,
    areSameIntLs,
)
from algo.math.ints import findAllFactors


class Factors(ExerciseBase):
    """
    Levels
    1. prime factorization (simple, up to 4 primes < 20, up to 1000)
    2. factors in a range (simple)
    3. GCD 1
    4. GCD 2
    5. common factors in a range
    6. mixed
    """
    ANSWER_FORMAT = "integer numbers separated by ,"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 6
        # generate int with small primes < 20
        self.intWSmallPrimeFacsGen = IntWSmallPrimeFactors(20)

    def generateExercise(self):
        if self.level < 2:
            # generate int with up to 4 prime factors < 20 and up to 1,000
            n = self.intWSmallPrimeFacsGen.genInt(4, 1000)
            if self.level == 0:
                # level 1
                return "Prime factorization of %d" % n
            # level 2
            facs = findAllFactors(n)
            nFacs = len(facs)
            k = min(nFacs-2, random.randint(1, 3))
            i = random.randint(1, nFacs-k-1)
            lb = max((facs[i-1] + facs[i]) // 2, 2)
            ub = min((facs[i+k-1] + facs[i+k]) // 2, n-1)
            return "Find all factors of %d between %d and %d" % (n, lb, ub)
        elif self.level == 2:
            # level 3
            pass
        else:
            pass

    def validateAnswer(self, q, a):
        if self.level < 2:
            aInInts = parseCommaSepInts(a)
            if aInInts is None:
                return -1
            qNums = extractAllIntsFrom(q)
            if self.level == 0:
                return 0 if areSameIntLs(aInInts, primeFactorization(qNums[0])) else 1
            else:
                return 0 if areSameIntLs(aInInts, findAllFactors(*qNums)) else 1
        else:
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
