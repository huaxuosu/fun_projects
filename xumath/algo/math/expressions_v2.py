import numbers
import operator
import random
import typing
import copy
# internal modules
from .fractions_v2 import FractionV2

# debug mode
EXPRESSION_V2_DEBUG = True


class ExpressionV2:
    """
    Expression:
    a math expression
    it contains expressions/values and operators (list of strings)
    supported operators:
        **
        *, /, //, %
        +, -

    Implemented using binary tree
    All leaves are values or None
    All other nodes are operators
    """
    SUPPORTED_VAL_CLASSES = {numbers.Number, FractionV2}
    SUPPORTED_OPERATORS = ["**", "*", "/", "//", "%", "+", "-"]
    OPERATORS_PRECEDENCES = {
        "**": 1,
        "*": 3, "/": 3, "//": 3, "%": 3,
        "+": 4, "-": 4,
    }
    __LEAST_OP_PRECEDENCE = 1_001
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
    def isSupportedOperator(cls, op):
        return isinstance(op, str) and op in cls.SUPPORTED_OPERATORS

    @classmethod
    def isSupportedValType(cls, val):
        return any(isinstance(val, e) for e in cls.SUPPORTED_VAL_CLASSES)

    @classmethod
    def isValidOperand(cls, operand):
        return cls.isSupportedValType(operand) or isinstance(operand, cls)

    @classmethod
    def make(
            cls,
            expsOrVals,
            operatorStrs,
            shuffleOperatorsWReplacement=False,
            applyRandomNegation=False,
            applyRandomNegationToExps=False):
        """
        expsOrVals contain expressions or values
        operators contain operators that are all binary ones of the same precedence
        applyRandomNegation: apply negation to the numbers in expsOrVals by random
        applyRandomNegationToExps: apply negation to the expressions in expsOrVals by random as well
            it only works when applyRandomNegation = True
        """
        assert isinstance(expsOrVals, typing.Iterable)
        assert all(map(cls.isValidOperand, expsOrVals))
        # ops should be a list, tuple, etc, and all ops should be supported
        assert isinstance(operatorStrs, typing.Iterable)
        expsOrVals = list(expsOrVals)
        ops = list(operatorStrs)
        assert all(map(cls.isSupportedOperator, ops))
        # all ops should have the same precedence
        assert len(set(cls.getOpPrecedences(ops))) == 1
        if shuffleOperatorsWReplacement:
            ops = [random.choice(ops) for _ in range(len(expsOrVals)-1)]
        assert len(ops) > 0 and len(expsOrVals) == len(ops) + 1

        def __buildTree(_vals, _ops):
            if len(_vals) == 1:
                return _vals[0]
            nd = cls(_vals[0], _ops[0], _vals[1])
            return __buildTree([nd] + _vals[2:], _ops[1:])

        if applyRandomNegation:
            for i in range(len(expsOrVals)):
                # do negation if it is a num or exp when applyRandomNegationToExps = True
                toApply = not isinstance(expsOrVals[i], cls) or applyRandomNegationToExps
                if toApply and random.choice([0, 1]) == 1:
                    expsOrVals[i] = -expsOrVals[i]

        return __buildTree(expsOrVals, ops)

    @classmethod
    def copyValOrExp(cls, orig):
        if orig is None or not isinstance(orig, cls):
            return copy.copy(orig)
        return cls(
            cls.copyValOrExp(orig.left),
            orig.op,
            cls.copyValOrExp(orig.right),
        )

    def __init__(self, leftOperand, operatorStr, rightOperand):
        """
        An expression is
        left operand operators on right operand
        if left operand is None, it is a unary operator
        Operands can be values or another expressions
        """
        assert operatorStr in self.__class__.SUPPORTED_OPERATORS
        assert leftOperand is None or self.__class__.isValidOperand(leftOperand)
        assert self.__class__.isValidOperand(rightOperand)
        self.left = self.__class__.copyValOrExp(leftOperand)
        self.op = operatorStr
        self.right = self.__class__.copyValOrExp(rightOperand)

    def applyRandomNegationRecursively(self, applyRandomNegationToExps=False):
        """
        apply negative by random to operands recursively
        if applyRandomNegationToExps is True, also apply to expressions
        """

        def __postorder(nd):
            if not isinstance(nd, self.__class__):
                # a leaf
                return -nd \
                    if nd is not None and random.choice([0, 1]) == 1 \
                    else self.__class__.copyValOrExp(nd)
            nd.left = __postorder(nd.left)
            nd.right = __postorder(nd.right)
            if applyRandomNegationToExps and random.choice([0, 1]) == 1:
                return -nd
            return self.__class__.copyValOrExp(nd)

        return __postorder(self)

    @property
    def opPrecedence(self):
        if self.left is not None:
            # binary
            return self.__class__.getOpPrecedences(self.op)
        # unary, always bracketed
        return 0

    def __neg__(self):
        if self.left is not None:
            # binary
            return self.__class__(None, "-", self.__class__.copyValOrExp(self))
        elif self.op == "-":
            return self.__class__.copyValOrExp(self.right)
        return self.__class__(None, "-", self.__class__.copyValOrExp(self.right))

    def eval(self):

        def __postorder(nd):
            if not isinstance(nd, self.__class__):
                # a leaf
                return nd
            rv = __postorder(nd.right)
            if nd.left is not None:
                # binary
                lv = __postorder(nd.left)
                return self.__class__.getOpOps(nd.op)(lv, rv)
            return -rv if nd.op == "-" else rv

        return __postorder(self)

    def copy(self):
        self.__class__.copyValOrExp(self)

    def treeRepr(self):

        def _helper(nd):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # leaf
            if not isinstance(nd, self.__class__):
                line = '%s' % nd
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle
            # Only right child.
            if nd.left is None:
                lines, n, p, x = _helper(nd.right)
                s = '%s' % nd.op
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
            # Two children.
            left, n, p, x = _helper(nd.left)
            right, m, q, y = _helper(nd.right)
            s = '%s' % nd.op
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

        allLines, *_ = _helper(self)
        return "\n".join(allLines)

    def __str__(self):

        def __postorder(nd):
            # return str rep and op precedence
            if not isinstance(nd, self.__class__):
                # a leaf
                return str(nd), 0 if nd > 0 else self.__class__.__LEAST_OP_PRECEDENCE
            rs, rp = __postorder(nd.right)
            if nd.left is not None:
                # binary
                cp = nd.opPrecedence
                ls, lp = __postorder(nd.left)
                if lp > cp:
                    ls = "(%s)" % ls
                if rp >= cp:
                    rs = "(%s)" % rs
                return "%s %s %s" % (ls, nd.op, rs), cp
            # unary
            if nd.op == "-":
                return ("-%s" if rp == 0 else "-(%s)") % rs, self.__class__.__LEAST_OP_PRECEDENCE
            return rs, rp

        s = __postorder(self)[0]
        if EXPRESSION_V2_DEBUG:
            print(self.treeRepr())
            print(float(self.eval()), eval(s))
            assert abs(float(self.eval()) - eval(s)) < 1e-16
        return s

    def __repr__(self):
        return str(self)

    ###
    # Binary Operators overloading
    ###
    def __add__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "+", other)

    def __sub__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "-", other)

    def __mul__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "*", other)

    def __truediv__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "/", other)

    def __floordiv__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "//", other)

    def __pow__(self, other):
        assert self.__class__.isValidOperand(other)
        return self.__class__(self, "**", other)
