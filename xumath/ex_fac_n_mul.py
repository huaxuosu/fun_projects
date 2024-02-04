import random
# internal modules
from algo.math.int_gen import (
    genRandIntByNDigs,
    genRandIntLsByNDigs,
    genRandIntLsWithRandomGcd,
)
from algo.math.int_misc import (
    extractAllIntsFrom,
    parseCommaSepInts,
    areSameIntLs,
)
from algo.math.int_mul_fac import (
    gcd,
    lcm,
    findAllFactors,
    findAllCommonFactors,
    findMultiplesInRange,
    findCommonMultiplesInRange,
)
from algo.math.int_primes import (
    primeFactorization,
    IntWSmallPrimeFactors,
)
from ex_base import ExerciseBase


class ExFacMulBase(ExerciseBase):
    ANSWER_FORMAT = "integer numbers separated by ,"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # generate int with small primes < 20
        self.intWSmallPrimeFacsGen = IntWSmallPrimeFactors(20)

    def generateExercise(self):
        raise NotImplementedError

    def validateAnswer(self, q, a):
        raise NotImplementedError


class Factors(ExFacMulBase):
    """
    Levels
    1. prime factorization (simple, up to 4 primes < 20, up to 1000)
    2. factors in a range (simple)
    3. GCD 1
    4. GCD 2
    5. common factors in a range
    """
    Q_HEAD_PF = "Prime factorization"
    Q_HEAD_FAF = "Find all factors"
    Q_HEAD_GCD = "Find GCD"
    Q_HEAD_FACF = "Find all common factors"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 5

    def generateExercise(self):
        if self.level < 2:
            # generate int with up to 4 prime factors and up to 1,000
            n = self.intWSmallPrimeFacsGen.genInt(maxNumPrimeFactors=4, maxVal=1000)
            if self.level == 0:
                # level 1
                return "%s of %d" % (Factors.Q_HEAD_PF, n)
            # level 2
            return self.__genExFaf(n)
        elif self.level < 4:
            # levels 3 and 4
            return self.__genExGcd()
        else:
            # level 5
            return self.__genExFacf()

    @staticmethod
    def __calcExFafParams(n):
        facs = findAllFactors(n)
        nFacs = len(facs)
        k = min(nFacs - 2, random.randint(1, 3))
        i = random.randint(1, nFacs - k - 1)
        lb = max((facs[i - 1] + facs[i]) // 2, 2)
        ub = min((facs[i + k - 1] + facs[i + k]) // 2, n - 1)
        return lb, ub

    def __genExFaf(self, n):
        lb, ub = self.__calcExFafParams(n)
        return "%s of %d between %d and %d" % (Factors.Q_HEAD_FAF, n, lb, ub)

    def __genExGcd(self):
        nOperands = random.randint(3, 4) if self.level == 3 else 2
        operands = genRandIntLsByNDigs(
            n=nOperands,
            minNDigs=2,
            maxNDigs=4,
            nonPrime=True,
            baseFac=self.intWSmallPrimeFacsGen.genInt(1) if random.random() < 2.0/3 else 1,
        )
        return "%s of %s" % (Factors.Q_HEAD_GCD, ", ".join(map(str, operands)))

    def __genExFacf(self):
        # vals and fac is their GCD
        vals, fac = genRandIntLsWithRandomGcd(
            n=2,
            intWSmallPrimeFacsGen=self.intWSmallPrimeFacsGen,
            maxNumPrimeFactorsOfGac=3,
            maxGcd=200,
        )
        lb, ub = self.__calcExFafParams(fac)
        vals = ", ".join(map(str, vals))
        return "%s of %s between %d and %d" % (Factors.Q_HEAD_FACF, vals, lb, ub)

    def validateAnswer(self, q, a):
        aInInts = parseCommaSepInts(a)
        if aInInts is None:
            return -1
        qNums = extractAllIntsFrom(q)
        if q.startswith(Factors.Q_HEAD_PF):
            return 0 if areSameIntLs(aInInts, primeFactorization(qNums[0])) else 1
        elif q.startswith(Factors.Q_HEAD_FAF):
            return 0 if set(aInInts) == set(findAllFactors(*qNums)) else 1
        elif q.startswith(Factors.Q_HEAD_GCD):
            return 0 if aInInts[0] == gcd(*qNums) else 1
        elif q.startswith(Factors.Q_HEAD_FACF):
            return 0 if set(aInInts) == set(findAllCommonFactors(qNums[:-2], *qNums[-2:])) else 1
        else:
            raise Exception("Unknown error!")


class Multiples(ExFacMulBase):
    """
    Levels
    1. multiples in a range (simple)
    2. LCM 1
    3. LCM 2
    4. common multiples in a range
    """
    Q_HEAD_FAM = "Find all multiples"
    Q_HEAD_LCM = "Find LCM"
    Q_HEAD_FACM = "Find all common multiples"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nLevels = 4

    def generateExercise(self):
        if self.level == 0:
            # level 1
            return self.__genExFam()
        elif self.level < 3:
            # levels 2 and 3
            return self.__genExLcm()
        else:
            # level 4
            return self.__genExFacf()

    @staticmethod
    def __calcExFamParams(n):
        k = random.randint(1, 3)
        i = genRandIntByNDigs(1, 2)
        lb = n*i - n//2
        ub = n*(i+k-1) + n//2
        return lb, ub

    def __genExFam(self):
        n = self.intWSmallPrimeFacsGen.genInt(maxNumPrimeFactors=4, maxVal=200)
        lb, ub = self.__calcExFamParams(n)
        return "%s of %d between %d and %d" % (Multiples.Q_HEAD_FAM, n, lb, ub)

    def __genExLcm(self):
        nOperands = random.randint(3, 4) if self.level == 2 else 2
        # vals and fac is their GCD
        vals, _ = genRandIntLsWithRandomGcd(
            n=nOperands,
            intWSmallPrimeFacsGen=self.intWSmallPrimeFacsGen,
            maxNumPrimeFactorsOfGac=3,
            maxGcd=200,
        )
        return "%s of %s" % (Multiples.Q_HEAD_LCM, ", ".join(map(str, vals)))

    def __genExFacf(self):
        # vals and fac is their GCD
        vals, _ = genRandIntLsWithRandomGcd(
            n=2,
            intWSmallPrimeFacsGen=self.intWSmallPrimeFacsGen,
            maxNumPrimeFactorsOfGac=2,
            maxGcd=100,
        )
        lb, ub = self.__calcExFamParams(lcm(*vals))
        vals = ", ".join(map(str, vals))
        return "%s of %s between %d and %d" % (Multiples.Q_HEAD_FACM, vals, lb, ub)

    def validateAnswer(self, q, a):
        aInInts = parseCommaSepInts(a)
        if aInInts is None:
            return -1
        qNums = extractAllIntsFrom(q)
        if q.startswith(Multiples.Q_HEAD_FAM):
            return 0 if set(aInInts) == set(findMultiplesInRange(*qNums)) else 1
        elif q.startswith(Multiples.Q_HEAD_LCM):
            return 0 if aInInts[0] == lcm(*qNums) else 1
        elif q.startswith(Multiples.Q_HEAD_FACM):
            return 0 if set(aInInts) == set(findCommonMultiplesInRange(qNums[:-2], *qNums[-2:])) else 1
        else:
            raise Exception("Unknown error!")
