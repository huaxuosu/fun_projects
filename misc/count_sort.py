# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 16:32:38 2024

@author: huaxu
"""

inpStr = "\
we need to sort this string using count sort \
it only has lower case letters and spaces \
we ignore all the spaces"

def countSort(inpStr):
    counts = {}
    # for i in range(10)
    # meaning that we start i from 0, and go all the way to 9 (NOT 10)
    for i in range(len(inpStr)):
        c = inpStr[i]
        if c != " ":
            if c not in counts:
                counts[c] = 0
            counts[c] += 1
    
    outStr = ""
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c in counts:
            outStr += c * counts[c]
    
    return outStr

countSort(inpStr)

countSort("hanyong xu")
