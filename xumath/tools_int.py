def gcd(*args):
    """
    GCD of a list of numbers
    """
    n = len(args)
    assert(n > 1)
    ret = args[0]
    for i in range(1, n):
        ret = __gcdBinary(ret, args[i])
    return ret


def __gcdBinary(a, b):
    """
    GCD of a and b
    """
    if a > b:
        return gcd(b, a)
    if b % a == 0:
        return a
    return gcd(a, b % a)


def lcm(*args):
    """
    LCM of a list of numbers
    """
    n = len(args)
    assert(n > 1)
    ret = args[0]
    for i in range(1, n):
        ret = __lcmBinary(ret, args[i])
    return ret


def __lcmBinary(a, b):
    """
    LCM of a and b
    """
    return a * b // __gcdBinary(a, b)
