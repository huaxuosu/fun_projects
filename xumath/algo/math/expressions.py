import numbers
import operator
import random
import typing
import copy

# debug mode
EXPRESSION_DEBUG = True


class Expression:
    """
    Expression:
    a math expression
    it contains expressions/values and operators (list of strings)
    exp_1 operator_1 exp_2 operator_2 ...
    exp_i is a value or expression
    supported operators:
        **
        *, /, //, %
        +, -
    """
    SUPPORTED_VAL_CLASSES = {numbers.Number}
    SUPPORTED_OPERATORS = ["**", "*", "/", "//", "%", "+", "-"]
    OPERATORS_PRECEDENCES = {
        "**": 1,
        "*": 3, "/": 3, "//": 3, "%": 3,
        "+": 4, "-": 4,
    }
    OPERATORS_OPERATORS = {
        "**": operator.pow,
        "*": operator.mul,
        "/": operator.truediv,
        "//": operator.floordiv,
        "%": operator.mod,
        "+": operator.add,
        "-": operator.sub,
    }

    @classmethod
    def getOpPrecedences(cls, ops):
        if isinstance(ops, str):
            assert ops in cls.SUPPORTED_OPERATORS
            return cls.OPERATORS_PRECEDENCES[ops]
        return list(map(cls.OPERATORS_PRECEDENCES.get, ops))

    @classmethod
    def getOpOps(cls, ops):
        if isinstance(ops, str):
            assert ops in cls.SUPPORTED_OPERATORS
            return cls.OPERATORS_OPERATORS[ops]
        return list(map(cls.OPERATORS_OPERATORS.get, ops))

    @classmethod
    def isSupportedValType(cls, val):
        return any(isinstance(val, e) for e in cls.SUPPORTED_VAL_CLASSES)

    @classmethod
    def validateSingleExpOrVal(cls, expOrVal):
        return isinstance(expOrVal, Expression) or cls.isSupportedValType(expOrVal)

    @classmethod
    def validateInpExpsOrVals(cls, expsOrVals):
        if expsOrVals is None:
            expsOrVals = []
        elif cls.validateSingleExpOrVal(expsOrVals):
            expsOrVals = [expsOrVals]
        else:
            # exps should be iterable and all elements be Number or Expression type
            assert isinstance(expsOrVals, typing.Iterable) and all(map(cls.validateSingleExpOrVal, expsOrVals))
            expsOrVals = list(expsOrVals)
        return expsOrVals

    @classmethod
    def validateSingleOp(cls, op):
        if isinstance(op, str):
            assert op in cls.SUPPORTED_OPERATORS
            return True
        return False

    @classmethod
    def validateInpOps(cls, ops, shuffleToSize):
        if ops is None:
            ops = []
        elif cls.validateSingleOp(ops):
            ops = [ops]
        else:
            # ops should be a list, tuple, etc, and all ops should be supported
            assert isinstance(ops, typing.Iterable) and all(map(cls.validateSingleOp, ops))
            ops = list(ops)
            # all ops should have the same precedence
            assert len(set(cls.getOpPrecedences(ops))) <= 1
        if shuffleToSize > -1:
            ops = [random.choice(ops) for _ in range(shuffleToSize)]
        return ops

    def __init__(
            self,
            expsOrVals=None,
            operators=None,
            sign=1,
            applyRandomNegation=False,
            applyRandomNegationToExps=False,
            shuffleOperatorsWReplacement=False):
        """
        expsOrVals and self.__exps contain expressions or values
        operators and self.__ops contain operators
            all operators are binary and should have the same precedence
        if __sign is -1, negation is applied to the expression
        applyRandomNegation: apply negation to the numbers in expsOrVals by random
        applyRandomNegationToExps: apply negation to the expressions in expsOrVals by random as well
            it only works when applyRandomNegation = True
        """
        self.__exps = self.__class__.validateInpExpsOrVals(expsOrVals)
        self.__ops = self.__class__.validateInpOps(
            operators,
            max(len(self.__exps)-1, 0) if shuffleOperatorsWReplacement else -1,
        )
        self.__sign = sign

        # final validate
        assert self.__sign in (-1, 1) and len(self.__ops) == max(len(self.__exps) - 1, 0)

        # apply random negation if requested
        if applyRandomNegation:
            self.applyRandomNegation(applyRandomNegationToExps)

        # simplify if needed
        self.simplify()

    def applyRandomNegation(self, applyRandomNegationToExps=False):
        for i in range(len(self.__exps)):
            # do negation if it is a num or exp when applyRandomNegationToExps = True
            act = applyRandomNegationToExps or not isinstance(self.__exps[i], Expression)
            if act and random.choice([0, 1]) == 1:
                self.__exps[i] = -self.__exps[i]

    @property
    def precedence(self):
        """
        lowest precedence of the operations in the Expression
        if the expression only have one val/exp and no operations and sign = 1, it has precedence of 0
        if sign = -1, its 2
        if it only has **, its 1,
        if it only has *, /, //, %, its 3
        if it only has +, -, its 4
        """
        assert bool(self.__exps)
        if not self.__ops:
            return 0
        if self.__sign == -1:
            return 2
        return max(self.__class__.getOpPrecedences(self.__ops))

    def simplify(self):
        """
        If an expression has some layers without any operation, we can unwrap it
        It could return a number if all layers are empty
        """
        if not self.__exps:
            self.__sign = 1
        elif self.__ops:
            for i in range(len(self.__exps)):
                if isinstance(self.__exps[i], Expression):
                    self.__exps[i] = self.__exps[i].simplify()
        else:
            if self.__sign == -1:
                self.__exps[0] = -self.__exps[0]
                self.__sign = 1
            exp = self.__exps[0]
            if isinstance(exp, Expression):
                exp = exp.simplify()
            if isinstance(exp, Expression):
                self.__exps, self.__ops, self.__sign = exp.__exps, exp.__ops, exp.__sign
            else:
                self.__exps[0] = exp
                return exp
        return self

    def __str__(self):

        def __precedence(x):
            return x.precedence if isinstance(x, Expression) else 0

        def __str(x):
            return ("(%s)" if self.__class__.isSupportedValType(x) and x < 0 else "%s") % str(x)

        if not self.__exps:
            return ""
        s = __str(self.__exps[0])
        curPrecedence = __precedence(self.__exps[0])
        for i, op in enumerate(self.__ops):
            opPrecedence = self.__class__.getOpPrecedences(op)
            if curPrecedence > opPrecedence:
                s = "(%s)" % s
            fmt = " %s (%s)" if __precedence(self.__exps[i + 1]) >= opPrecedence else " %s %s"
            s += fmt % (op, __str(self.__exps[i+1]))
            curPrecedence = opPrecedence
        if self.__sign == -1:
            s = "-(%s)" % s
        # for debug only
        if EXPRESSION_DEBUG:
            assert abs(eval(s) - self.eval()) < 1e-16
        return s

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return bool(self.__exps)

    def __neg__(self):
        assert(bool(self.__exps))
        return self.__class__(self.__exps, self.__ops, -self.__sign)

    def eval(self):

        def __eval(x):
            return x.eval() if isinstance(x, Expression) else x

        assert(bool(self.__exps))
        ret = __eval(self.__exps[0])
        for i, op in enumerate(self.__ops):
            ret = self.__class__.getOpOps(op)(ret, __eval(self.__exps[i+1]))
        return -ret if self.__sign == -1 else ret

    ###
    # Binary Operators overloading
    ###
    def __calc(self, other, op):
        """
        expression calculation:
            create a new expression equal to
                self op other
        for example self = (3 + 5), other = (4//2), op = *
        new exps = [(3+5), (4//2)]
        new ops = ["*"]
        the resulted expression = (3 + 5) * (4 // 2)
        """
        assert bool(self.__exps)
        assert self.__class__.validateSingleOp(op)
        if self.__class__.isSupportedValType(other):
            other = self.__class__(other)
        if self.precedence in (0, self.__class__.getOpPrecedences(op)):
            exps = copy.copy(self.__exps) + [other.simplify()]
            ops = copy.copy(self.__ops) + [op]
            return self.__class__(exps, ops)
        return self.__class__([self.simplify(), other.simplify()], op)

    def __add__(self, other):
        return self.__calc(other, "+")

    def __sub__(self, other):
        return self.__calc(other, "-")

    def __mul__(self, other):
        return self.__calc(other, "*")

    def __truediv__(self, other):
        return self.__calc(other, "/")

    def __floordiv__(self, other):
        return self.__calc(other, "//")

    def __pow__(self, other):
        return self.__calc(other, "**")
