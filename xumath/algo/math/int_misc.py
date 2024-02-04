import re
import collections


def isInt(s: str):
    return bool(re.search(r"^[+-]?\d+$", s))


def extractAllIntsFrom(s: str):
    return list(map(int, re.findall(r"[+-]?\d+", s)))


def parseCommaSepInts(s: str):
    aInLs = s.replace(",", " ").split()
    return list(map(int, aInLs)) if aInLs and all(map(str.isdigit, aInLs)) else None


def areSameIntLs(l1: list, l2: list):
    """
    Check to see if l1 and l2 are the same lists of integers (order doesn't matter)
    """
    return collections.Counter(l1) == collections.Counter(l2)
