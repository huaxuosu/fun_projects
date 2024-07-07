import re


def isANumber(aStr):
    return re.search(r"(?i)^\s*[+-]?(?:inf(inity)?|nan|(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)\s*$", aStr)
