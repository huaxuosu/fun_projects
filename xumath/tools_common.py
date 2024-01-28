import functools
import operator


def zipTwoLists(l1, l2):
    # l1 and l2 are of same size, or l2 is short by 1
    # return [l1[0], l2[0], l1[1], l2[1], ..., l1[-1], l2[-1]]
    assert(len(l1) - len(l2) in [0, 1])
    m = len(l2)
    return functools.reduce(operator.add, map(list, zip(l1[:m], l2))) + l1[m:]


