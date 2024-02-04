import numbers
import operator
import random
import typing
import copy


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
    DEBUG = True

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
        self.__exps = expsOrVals
        self.__ops = operators
        self.__sign = sign

        # validate inputs
        self.__validate(shuffleOperatorsWReplacement)

        # apply random negation if requested
        if applyRandomNegation:
            self.applyRandomNegation(applyRandomNegationToExps)

    def __validate(self, shuffleOperatorsWReplacement):
        # exps or vals
        if self.__exps is None:
            self.__exps = []
        elif isinstance(self.__exps, numbers.Number):
            self.__exps = [self.__exps]
        else:
            # exps should be iterable
            assert isinstance(self.__exps, typing.Iterable)
            # exps should be of Number or Expression type
            assert all(isinstance(e, numbers.Number) or isinstance(e, Expression) for e in self.__exps)
            self.__exps = list(self.__exps)
        nExps = len(self.__exps)
        for i in range(nExps):
            if isinstance(self.__exps[i], Expression):
                self.__exps[i] = self.__exps[i].simplify()

        # negation
        assert self.__sign in (-1, 1)
        if self.__sign == -1 and nExps <= 1:
            self.__sign = 1
            if nExps == 1:
                self.__exps[0] = -self.__exps[0]

        # operators
        if self.__ops is None:
            self.__ops = []
        elif isinstance(self.__ops, str):
            self.__ops = [self.__ops]
        else:
            # ops should be a list, tuple, etc
            assert isinstance(self.__ops, typing.Iterable)
            # all ops should be supported
            assert all(isinstance(e, str) and e in Expression.SUPPORTED_OPERATORS for e in self.__ops)
            self.__ops = list(self.__ops)
        # all ops should have the same precedence
        assert not self.__ops or len(set(map(Expression.OPERATORS_PRECEDENCES.get, self.__ops))) == 1
        if shuffleOperatorsWReplacement:
            self.__ops = [random.choice(self.__ops) for _ in range(nExps - 1)]
        assert len(self.__ops) == max(nExps - 1, 0)

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
        if not self.__ops:
            return 0
        if self.__sign == -1:
            return 2
        return max(map(Expression.OPERATORS_PRECEDENCES.get, self.__ops))

    def simplify(self):
        """
        If an expression has some layers without any operation, we can unwrap it
        It could return a number if all layers are empty
        """
        if not self.__exps:
            self.__sign = 1
        elif not self.__ops:
            if self.__sign == -1:
                self.__exps[0] = -self.__exps[0]
                self.__sign = 1
            if isinstance(self.__exps[0], Expression):
                # simplify recursively
                return self.__exps[0].simplify()
            return self.__exps[0]
        return self

    def __str__(self):
        def getPrecedence(x):
            return x.precedence if isinstance(x, Expression) else 0
        if not self.__exps:
            return ""
        s = str(self.__exps[0])
        curPrecedence = getPrecedence(self.__exps[0])
        for i, op in enumerate(self.__ops):
            opPrecedence = Expression.OPERATORS_PRECEDENCES[op]
            if curPrecedence > opPrecedence:
                s = "(%s)" % s
            fmt = " %s (%s)" if getPrecedence(self.__exps[i+1]) >= opPrecedence else " %s %s"
            s += fmt % (op, str(self.__exps[i+1]))
            curPrecedence = opPrecedence
        if self.__sign == -1:
            s = "-(%s)" % s
        # for debug only
        if Expression.DEBUG:
            assert abs(eval(s) - self.eval()) < 1e-16
        return s

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return bool(self.__exps)

    def __neg__(self):
        assert(bool(self.__exps))
        return Expression(self.__exps, self.__ops, -self.__sign)

    def eval(self):
        def __eval(x):
            return x.eval() if isinstance(x, Expression) else x
        assert(bool(self.__exps))
        ret = __eval(self.__exps[0])
        for i, op in enumerate(self.__ops):
            ret = Expression.OPERATORS_OPERATORS[op](ret, __eval(self.__exps[i+1]))
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
        assert(bool(self.__exps))
        assert(isinstance(op, str) and op in Expression.SUPPORTED_OPERATORS)
        if isinstance(other, numbers.Number):
            other = Expression(other)
        if self.precedence in (0, Expression.OPERATORS_PRECEDENCES[op]):
            exps = copy.copy(self.__exps) + [other.simplify()]
            ops = copy.copy(self.__ops) + [op]
            return Expression(exps, ops)
        return Expression([self.simplify(), other.simplify()], op)

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
