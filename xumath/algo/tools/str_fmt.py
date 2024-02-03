def framedStr(s):
    n = len(s)
    return "\n".join(("#"*(n+4), "# %s #" % s, "#"*(n+4)))
