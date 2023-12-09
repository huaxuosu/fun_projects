# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:53:07 2023

@author: huaxu
"""
import numpy as np
import operator
import matplotlib.pyplot as plt

class BlobBitmap:
    __m, __n = None, None
    @classmethod
    def setMatSize(cls, nrows, ncols):
        cls.__m = nrows
        cls.__n = ncols
    
    def __init__(self, cell=None):
        self.map = 1 << (BlobBitmap.__m * BlobBitmap.__n + 1)
        if cell is not None:
            self.addCell(cell)
    
    def addCell(self, cell):
        i = self.__getCellInd(cell)
        self.map |= 1 << i
    
    def hasCell(self, cell):
        i = self.__getCellInd(cell)
        return (self.map >> i) & 1 == 1
    
    def hasAnyCellIn(self, cells):
        for cell in cells:
            if self.hasCell(cell):
                return True
        return False
    
    def __add__(self, cell):
        b = BlobBitmap()
        b.map = self.map
        b.addCell(cell)
        return b
    
    def cells(self):
        ix = BlobBitmap.__m * BlobBitmap.__n
        for i in range(ix):
            if (self.map >> i) & 1 == 1:
                yield i//BlobBitmap.__n, i%BlobBitmap.__n
    
    def __eq__(self, b):
        return self.map == b.map
    
    def __hash__(self):
        return hash(self.map)
    
    def __repr__(self):
        return repr([e for e in self.cells()])
    
    def __getCellInd(self, cell):
        r, c = cell
        assert(-1 < r < BlobBitmap.__m and -1 < c < BlobBitmap.__n)
        return r*BlobBitmap.__n + c

# get all blobs with size >= 2 and cum prod = target
class Blobs:
    # equivalent to a dict
    # key: cell (r, c)
    # val: a list of blobs that contain the cell and have size > 2 and cum prod = target
    def __init__(self, nrows, ncols):
        self.d = {(r, c):[] for r in range(nrows) for c in range(ncols)}
    
    def add(self, blob):
        for cell in blob.cells():
            self.d[cell].append(blob)
    
    def rm(self, blob):
        for cell in blob.cells():
            self.d.pop(cell)
    
    def clean0(self):
        bset = set(b for e in self.d for b in self.d[e])
        toDel = set()
        for b in bset:
            cells = list(b.cells())
            valid = True
            for k in self.d:
                v = [e for e in self.d[k] if e == b or not e.hasAnyCellIn(cells)]
                if len(v) == 0:
                    # invalid blob
                    valid = False
                    break
            if not valid:
                toDel.add(b)
        
        cells = self.d.keys()
        for cell in cells:
            self.d[cell] = [e for e in self.d[cell] if e not in toDel]
    
    def clean(self, usedCells):
        cells = self.d.keys()
        for cell in cells:
            self.d[cell] = [e for e in self.d[cell] if not e.hasAnyCellIn(usedCells)]
    
    def __contains__(self, cell):
        return cell in self.d
    
    def __iter__(self):
        return self.d.__iter__()
    
    def __getitem__(self, cell):
        return self.d[cell]
    
    def __repr__(self):
        return repr(self.d)

def getAllValidBlobs(mat, target):
    nrows, ncols = mat.shape
    BlobBitmap.setMatSize(nrows, ncols)
    
    blobs = Blobs(nrows, ncols)
    seen = {BlobBitmap((r, c)): mat[r, c] for r in range(nrows) for c in range(ncols)}
    prev = seen.copy()
    while prev:
        cur = {}
        for b, p in prev.items():
            # b: blob; p: cumprod
            for r, c in b.cells():
                # add one neighboring cell to the current blob to create a new one
                for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nr, nc = r+dr, c+dc
                    if -1 < nr < nrows and -1 < nc < ncols:
                        np = p*mat[nr, nc]
                        nb = b + (nr, nc)
                        # if the new blob has cumprod <= target and not seen
                        if np <= target and nb not in seen and nb not in cur:
                            cur[nb] = np
                            if np == target:
                                blobs.add(nb)
        seen.update(cur)
        prev = cur
    return blobs

def plotTbl(tblData, groupIds):
    clrCodes = ["%X" % d for d in range(85, 256, 125)]
    colors = np.array([
        "#" + "".join(["FF"]*i + [c] + ["FF"]*(3-i-1))
        for c in clrCodes
        for i in range(3)
    ] + [
        "#" + "".join([c]*i + ["FF"] + [c]*(3-i-1))
        for c in clrCodes
        for i in range(3)
    ])
    nClr = len(colors)
    
    
    # plot table
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=tblData,cellColours=colors[groupIds%nClr],loc='center')
    plt.show()

mat = np.array([[5, 15, 1], [3, 3, 15], [5, 1, 1]])
target = 15

mat = np.array([
    [4, 3, 3, 6],
    [2, 2, 4, 2],
    [2, 3, 3, 4],
    [6, 2, 3, 2],
])
target = 12

mat = np.array([
    [9, 3, 12, 4, 9],
    [4, 3, 3, 2, 6],
    [2, 2, 2, 3, 6],
    [9, 6, 2, 3, 18],
    [3, 12, 3, 4, 2],
])
target = 36

mat = np.array([
    [10, 8, 2, 2, 2],
    [20, 5, 16, 2, 5],
    [4, 2, 2, 40, 10],
    [20, 2, 4, 5, 2],
    [5, 16, 4, 2, 2],
])
target = 80

mat = np.array([
    [2, 12, 6, 2, 2],
    [3, 3, 4, 2, 2],
    [8, 3, 4, 8, 2],
    [2, 4, 6, 3, 3],
    [2, 3, 2, 2, 2],
])
target = 24

mat = np.array([
    [7, 7, 3, 3, 2],
    [6, 2, 14, 6, 7],
    [7, 3, 7, 7, 7],
    [3, 2, 2, 3, 2],
    [21, 2, 21, 2, 3],
])
target = 42

# no solution
mat = np.array([
    [7, 14, 3, 3, 2],
    [6, 2, 14, 6, 7],
    [7, 3, 7, 7, 7],
    [3, 2, 2, 3, 2],
    [21, 2, 21, 2, 3],
])
target = 42

blobs = getAllValidBlobs(mat, target)
blobIds = np.zeros(mat.shape).astype(int) - 1
# num of valid blobs found
nblobs = 0

for _ in range(operator.mul(*mat.shape)):
    blobs.clean0()
    cells = sorted(blobs, key=lambda x: len(blobs[x]))
    if not cells or len(blobs[cells[0]]) < 1:
        break
    usedCells = set()
    for cell in cells:
        if cell in blobs and (len(blobs[cell]) == 1 or not usedCells):
            # use this blob
            for e in blobs[cell][0].cells():
                blobIds[e] = nblobs
                usedCells.add(e)
            blobs.rm(blobs[cell][0])
            nblobs += 1
    
    # clean blobs
    blobs.clean(usedCells)

if -1 not in blobIds:
    print("Solution found!!!")
    plotTbl(mat, blobIds)
else:
    print("Failed to find a solution!!!")
