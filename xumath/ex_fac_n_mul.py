import random
# internal modules
from algo.math.ints import findAllFactors, gcd
from algo.math.primes import (
    primeFactorization,
    IntWSmallPrimeFactors,
)
from algo.rand.gen_ints import genRandIntLsByNDigs
from algo.ex_validate_int import (
    extractAllIntsFrom,
    parseCommaSepInts,
    areSameIntLs,
)
from ex_base import ExerciseBase


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
    Q_HEAD_PF = "Prime factorization"
    Q_HEAD_FAF = "Find all factors"
    Q_HEAD_GCD = "Find GCD"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 6
        # generate int with small primes < 20
        self.intWSmallPrimeFacsGen = IntWSmallPrimeFactors(20)

    def generateExercise(self):
        if self.level < 2:
            # generate int with up to 4 prime factors and up to 1,000
            n = self.intWSmallPrimeFacsGen.genInt(4, 1000)
            if self.level == 0:
                # level 1
                return "%s of %d" % (Factors.Q_HEAD_PF, n)
            # level 2
            facs = findAllFactors(n)
            nFacs = len(facs)
            k = min(nFacs-2, random.randint(1, 3))
            i = random.randint(1, nFacs-k-1)
            lb = max((facs[i-1] + facs[i]) // 2, 2)
            ub = min((facs[i+k-1] + facs[i+k]) // 2, n-1)
            return "%s of %d between %d and %d" % (Factors.Q_HEAD_FAF, n, lb, ub)
        elif self.level <= 3:
            # levels 3 and 4
            operands = genRandIntLsByNDigs(
                n=random.randint(3, 4) if self.level == 3 else 2,
                minNDigs=2,
                maxNDigs=4)
            return "%s of %s" % (Factors.Q_HEAD_GCD, ", ".join(map(str, operands)))
        else:
            pass

    def validateAnswer(self, q, a):
        aInInts = parseCommaSepInts(a)
        if aInInts is None:
            return -1
        qNums = extractAllIntsFrom(q)
        if q.startswith(Factors.Q_HEAD_PF):
            return 0 if areSameIntLs(aInInts, primeFactorization(qNums[0])) else 1
        elif q.startswith(Factors.Q_HEAD_FAF):
            return 0 if areSameIntLs(aInInts, findAllFactors(*qNums)) else 1
        elif q.startswith(Factors.Q_HEAD_GCD):
            return 0 if aInInts[0] == gcd(*qNums) else 1
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
