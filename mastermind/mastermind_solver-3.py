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
def calcFeedback(guess, code):
    """
    Return # of red pegs (right guesses), # of white pegs (right colors, but wrong positions)
    """
    nRedPegs = (guess == code).sum()
    n1 = np.bincount(guess)
    n2 = np.bincount(code)
    m = min(n1.size, n2.size)
    nWhitePegs = np.minimum(n1[:m], n2[:m]).sum()
    return (nRedPegs, nWhitePegs - nRedPegs)

def createInitCandidates(codeLen, nCodeElems):
    """
    candidates: all possibe guesses
    """
    candidates = []
    aux = [0]*codeLen
    def _initCandidates(i=0):
        if i == codeLen:
            candidates.append(aux[:])
            return
        for aux[i] in range(nCodeElems):
            _initCandidates(i+1)
    _initCandidates()
    candidates = np.array(candidates)
    return candidates

def getFeedback(codeLen):
    while True:
        feedback = input("Please enter # red pegs, # white pegs:\n")
        try:
            feedback = tuple(map(int, map(str.strip, feedback.replace(",", " ").split())))
            if len(feedback) == 2 and 0 <= feedback[0] <= codeLen and 0 <= feedback[1] <= codeLen-feedback[0]:
                return feedback
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
    def __init__(self, codeElems, codeLen):
        self.__codeElems = np.array(codeElems)
        self.__codeLen = codeLen
    
    def __algo1(self, candidates):
        # initialize guess to any values
        guess = np.zeros(self.__codeLen, dtype=int)
        curCandidates = candidates.copy()
        for i in range(self.__codeLen):
            guess[i] = np.bincount(curCandidates[:,i]).argmax()
            curCandidates = curCandidates[curCandidates[:,i] ==  guess[i], :]
        return guess
    
    def __algo2(self, candidates):
        # randomly pick from candidates
        return candidates[random.randint(0, candidates.shape[0]-1), :]
    
    def __updateCandidates(self, candidates, guess, feedback):
        return candidates[np.apply_along_axis(lambda x: calcFeedback(guess, x) == feedback, 1, candidates)]
    
    def stats(self, algo, n=1000):
        if algo == 1:
            codeGen = self.__algo1
        elif algo == 2:
            codeGen = self.__algo2
        else:
            raise Exception("Invalid algorithm provided!")
        stats = []
        for _ in range(n):
            code = np.array([random.randint(0, self.__codeElems.size-1) for _ in range(self.__codeLen)])
            candidates = createInitCandidates(self.__codeLen, self.__codeElems.size)
            nTries = 0
            while True:
                nTries += 1
                guess = codeGen(candidates)
                feedback = calcFeedback(guess, code)
                if feedback[0] == 4:
                    break
                candidates = self.__updateCandidates(candidates, guess, feedback)
            stats.append(nTries)
        return np.bincount(stats)
    
    def solve(self, algo=1):
        if algo == 1:
            codeGen = self.__algo1
        elif algo == 2:
            codeGen = self.__algo2
        else:
            raise Exception("Invalid algorithm provided!")
        candidates = createInitCandidates(self.__codeLen, self.__codeElems.size)
        nTries = 0
        while True:
            nTries += 1
            guess = codeGen(candidates)
            print("Here is the guess:", self.__codeElems[guess])
            feedback = getFeedback(self.__codeLen)
            if feedback[0] == 4:
                print("Code cracked after %d guesses!  Oh yeah!!!" % nTries)
                print("Here is the code:", self.__codeElems[guess])
                return
            candidates = self.__updateCandidates(candidates, guess, feedback)
            if candidates.size < 1:
                print("Impossible!  No more guesses!\nYou must have entered incorrect feedbacks for the guesses!")
                return

if __name__ == "__main__":
    ###
    # Crack codes with 6 elementy colors and a length of 4
    ###
    codeElems = ["red", "blue", "green", "yellow", "white", "black"]
    solver = Solver(codeElems, codeLen=4)
    while True:
        solver.solve(algo=2)
        if not getYesOrNo("Do you want to try again [Yes/No]:\n"):
            break
