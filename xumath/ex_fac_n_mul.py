import random
import collections
# internal modules
from ex_base import ExerciseBase
from algo.primes import (
    isPrime,
    findPrimes,
    primeFactorization,
)
from tools.int_in_str import extractAllIntsFrom
from algo.ints import findAllFactors


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
        # primes before 30
        self.primesBf30 = findPrimes(20)

    def generateExercise(self):
        if self.level <= 1:
            n = self._genSmallNumForFactorization()
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

    def _genSmallNumForFactorization(self):
        n = 1
        for _ in range(4):
            p = random.choice(self.primesBf30)
            if n * p >= 1000 and not isPrime(n):
                break
            n *= p
        return n

    def validateAnswer(self, q, a):
        if self.level < 2:
            aInLs = a.replace(",", " ").split()
            if not all(map(str.isdigit, aInLs)):
                return -1
            aInCnts = collections.Counter(map(int, aInLs))
            qNums = extractAllIntsFrom(q)
            if self.level == 0:
                return 0 if aInCnts == collections.Counter(primeFactorization(qNums[0])) else 1
            else:
                facsInRange = findAllFactors(*qNums)
                return 0 if aInCnts == collections.Counter(facsInRange) else 1
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
