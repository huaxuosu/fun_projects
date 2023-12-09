# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:11:56 2023

@author: huaxu
"""

import numpy as np
import random

###
# Settings
###
codes = ["red", "blue", "green", "yellow", "white", "black"]
codeSize = 4

codes = np.array(codes)
nc = codes.size

def caclResp(pk, cb):
    nR = (pk == cb).sum()
    n1 = np.bincount(pk)
    n2 = np.bincount(cb)
    m = min(n1.size, n2.size)
    nC = np.minimum(n1[:m], n2[:m]).sum()
    return (nR, nC - nR)

stats = []
for _ in range(1000):
    combo = np.array([random.randint(0, nc-1) for _ in range(codeSize)])

    # [# of color and position are both right, # of only color is right]
    resp = (0, 0)

    # pool: all possibe combos
    pool = np.array([
            [e1, e2, e3, e4]
            for e1 in range(nc)
            for e2 in range(nc)
            for e3 in range(nc)
            for e4 in range(nc)
        ])
    
    # initialize picks to be impossible values
    picks = np.zeros(codeSize, dtype=int) + -1
    
    nTries = 0
    while True:
        nTries += 1
        curPool = pool.copy()
        for i in range(codeSize):
            picks[i] = np.bincount(curPool[:,i]).argmax()
            curPool = curPool[curPool[:,i] ==  picks[i], :]
        resp = caclResp(picks, combo)
        if resp[0] == 4:
            break
        pool = pool[np.apply_along_axis(lambda x: caclResp(picks, x) == resp, 1, pool)]
    
    stats.append(nTries)
