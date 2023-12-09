# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 12:11:56 2023

@author: huaxu
"""

import numpy as np
import random

###
# Helper functions
###
def caclResp(pk, cb):
    """
    Return # of right guesses, # of right colors
    """
    nR = (pk == cb).sum()
    n1 = np.bincount(pk)
    n2 = np.bincount(cb)
    m = min(n1.size, n2.size)
    nC = np.minimum(n1[:m], n2[:m]).sum()
    return (nR, nC - nR)

def createInitPool(codeLen, nCodeColors):
    """
    pool: all possibe combos
    """
    pool = []
    aux = [0]*codeLen
    def _initPool(i=0):
        if i == codeLen:
            pool.append(aux[:])
            return
        for aux[i] in range(nCodeColors):
            _initPool(i+1)
    _initPool()
    pool = np.array(pool)
    return pool

def getResp(codeLen):
    while True:
        resp = input("Please enter # red pids, # white pins:\n")
        try:
            resp = tuple(map(int, map(str.strip, resp.replace(",", " ").split())))
            if len(resp) == 2 and 0 <= resp[0] <= codeLen and 0 <= resp[1] <= codeLen-resp[0]:
                return resp
        except:
            pass
        print("Invalid input, try again!")

def getYesOrNo(mssg):
    while True:
        yesOrNo = input(mssg)
        if yesOrNo.lower() in ("y", "yes", "yeah", "yep"):
            return True
        if yesOrNo.lower() in ("n", "no", "nope"):
            return False
        print("Invalid input, try again!")

###
# Solver
###
class Solver:
    def __init__(self, codeColors, codeLen):
        self.__codeColors = np.array(codeColors)
        self.__codeLen = codeLen
    
    def solve(self):
        # initialize picks to any values
        picks = np.zeros(self.__codeLen, dtype=int)
        pool = createInitPool(self.__codeLen, self.__codeColors.size)
        nTries = 0
        while True:
            nTries += 1
            curPool = pool.copy()
            for i in range(self.__codeLen):
                picks[i] = np.bincount(curPool[:,i]).argmax()
                curPool = curPool[curPool[:,i] ==  picks[i], :]
            print("Here is the guess:", self.__codeColors[picks])
            resp = getResp(self.__codeLen)
            if resp[0] == 4:
                print("Code cracked after %d guesses!  Oh yeah!!!" % nTries)
                print("Here is the code:", self.__codeColors[picks])
                return
            pool = pool[np.apply_along_axis(lambda x: caclResp(picks, x) == resp, 1, pool)]
            if pool.size < 1:
                print("Impossible!  No more guesses!\nYou must have entered wrong respones for the guesses!")
                return

if __name__ == "__main__":
    ###
    # Crack codes with 6 colors and a length of 4
    ###
    codeColors = ["red", "blue", "green", "yellow", "white", "black"]
    solver = Solver(codeColors, codeLen=4)
    while True:
        solver.solve()
        if not getYesOrNo("Do you want to try again [Yes/No]:\n"):
            break
