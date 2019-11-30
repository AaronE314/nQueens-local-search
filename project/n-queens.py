from random import randint
from operator import add
import time
import sys

import numpy as np

class Queen: 
    def __init__(self, col ,row, pairs=0): 
        self.col = col 
        self.row = row

    def __str__(self):
        return '\nCol={}, Row={}'.format(self.col, self.row)

    def __repr__(self):
        return '\nCol={}, Row={}'.format(self.col, self.row)

    def __eq__(self,other): 
        return self.col == other.col

    def __ne__(self,other):
        return not self.__eq__(other)

class puzzle: 
    def __init__(self, n, array=None): 
    
        #random initial state, could be greedy
        self.queens = []
        if array is not None : 
            for i in range(n): 
                self.queens.append(Queen(i, array[i]))
        else : 
            # for i in range(n): 
                # self.queens.append(Queen(i,randint(0,n - 1)))
            self.queens = createBoard(n)
        self.conflictQueens = []
        self.pairsCount = countPairs(self, n)
        
    def __str__(self):
        return '\n Pairs = {}\n conflicted Queens = {}'.format(self.pairsCount, self.conflictQueens)

    def __repr__(self):
        return '\n Pairs = {} conflicted Queens = {}'.format(self.pairsCount, self.conflictQueens)

def createBoard(N):
    '''
    Creates the inital state of the board by adding the next queen to the spot with the least conflicts O(2n^2)
    ---------------------------
    Params:
        n: the size of the board
    returns:
        puzzle: a 1-d list of size n containing a queen at each column
    '''
    row = np.zeros(N, dtype=int)
    ld = np.zeros(N + N, dtype=int)
    rd = np.zeros(N + N, dtype=int)

    r = np.random.randint(0, N)

    row[r] = 1
    ld[r] = 1
    rd[N - r] = 1

    queens = [Queen(0, r)]

    for col in range(1, N): # O(N)

        if N >= 100000:
            if col % 1000 == 0:
                print("Progress: {}/{}".format(col, N), end='\r') 

        p = ld[col: col + N]
        q = (rd[col + 1: col + N + 1])[::-1]
        total = row + p + q # O(N)
        minT = np.where(total == total.min())[0] # O(N)
        r = np.random.randint(0, minT.shape[0])
        r = minT[r]

        row[r] += 1
        ld[r + col] += 1
        rd[N - r + col] += 1

        queens.append(Queen(col, r))
    print()
    return queens

def countPairs(puzzle, n):
    '''
    Counts the total number of pairs in the board O(4n)
    ---------------------------
    Params:
        puzzle: A puzzle for the current state
        n: the size of the board
    returns:
        counts: the count of the pairs
    '''
    count = 0
    f_row = [0] * n
    f_mdiag = [0] * (n + n)
    f_sdiag = [0] * (n + n)
    queens = puzzle.queens
    puzzle.conflictQueens = []

    cRow = dict({})
    cmD = dict({})
    csD = dict({})

    for i in range(n): # O(n)
        row = queens[i].row
        f_row[row] += 1
        if f_row[row] > 1:
            cRow[row] = True
        f_mdiag[row + i] += 1
        if f_mdiag[row + i] > 1:
            cmD[row + i] = True
        f_sdiag[n - row + i] += 1
        if f_sdiag[n - row + i] > 1:
            csD[n - row + i] = True

    for i in range(n + n): # O(2n)
        x, y, z = 0, 0, 0

        if i < n:
            x = f_row[i]
        y = f_mdiag[i]
        z = f_sdiag[i]

        count += (x * (x - 1)) // 2
        count += (y * (y - 1)) // 2
        count += (z * (z - 1)) // 2

    for q in queens: # O(n)

        if q.row in cRow or q.row + q.col in cmD or n - q.row + q.col in csD:
            puzzle.conflictQueens.append(q)
    return count

def localSearch(puzzle, maxSteps, n):
    '''
    Performs min conflics local search of the puzzle O(6n)
    ---------------------------
    Params:
        puzzle: A puzzle for the current state
        maxSteps: The maximum number of steps to try before aborting
        n: the size of the board
    returns:
        The finished puzzle
        The number of steps
        If it was solved
    '''
    savedInstances = dict({})
    blacklistedQueens = []
    lastCount = 0 
    thisCount = 1
    for i in range(maxSteps): # O(k)
        if i %100 == 0: 
            print("BenchMark:", i)

        if lastCount == thisCount:
            for queen in puzzle.conflictQueens: 
                if (queen.col, queen.row) not in savedInstances: 
                    savedInstances[(queen.col,queen.row)] = True
        else : 
            savedInstances = dict({})

        m = len(puzzle.conflictQueens)    

        index = randint(0, m - 1)
        currentQueen = puzzle.conflictQueens[index]

        pairMin, minRow = findMinimum(currentQueen.row,currentQueen.col, puzzle,n,savedInstances) # O(2n)
        if (minRow != currentQueen.row): 
            puzzle.queens[currentQueen.col].row = minRow
            puzzle.queens[currentQueen.col].pairsCount = pairMin
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                savedInstances[(currentQueen.col,currentQueen.row)] = True
        else:
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                savedInstances[(currentQueen.col,currentQueen.row)] = True

        puzzle.pairsCount = countPairs(puzzle,n) # O(4n)
        lastCount = thisCount 
        thisCount = puzzle.pairsCount

        if puzzle.pairsCount == 0: 
            return puzzle, i, True
    return puzzle, i, False

def findMinimum(cRow, cCol, puzzle, n, savedInstances):
    '''
    Finds the next move to do for a given queen that will minimize the conflicts O(2n)
    ---------------------------
    Params:
        row: The row of the current queen
        col: The column of the current queen
        puzzle: A puzzle for the current state
        n: the size of the board
        savedInstance: A small buffer of previous moves used for dealing with plateaus
    returns:
        The new count for the conflicts
        The row to move the queen too
    '''

    total = np.zeros(n)
    queens = puzzle.queens

    for i in range(n): # O(n)

        row = queens[i].row
        if i != cCol:
            total[row] += 1

        if cCol <= row + i <= cCol + (n - 1):
            total[row + i - cCol] += 1
        if cCol + 1 <= n - row + i <= n + cCol:
            total[abs((n - row + i) - (n + cCol))] += 1

    mins = np.where(total == total.min())[0] # O(n)

    i = np.random.randint(0, mins.shape[0])
    r = mins[i]

    while len(mins) > 1 and (cCol, r) in savedInstances:
        mins = np.delete(mins, i)
        i = randint(0, len(mins) - 1)
        r = mins[i]
    
    if len(mins) == 1:
        return total[mins[0]], mins[0]
    else:
        return total[mins[i]], mins[i]


def printBoard(puzzle):
    '''
    Prints the board with index 0, 0 at the botton left corner
    ---------------------------
    Params:
        puzzle: A puzzle for the current state
    prints:
        prints the board
    '''
    arr = puzzle.queens
    for i in range(n-1 , -1 ,-1 ):#rows 
        for j in range(n):#column
            if arr[j].row == i: 
                print("Q|",end = "")
            else : 
                print(".|",end="")
        print()
    print("Pairs = {}".format(puzzle.pairsCount))

if __name__ == "__main__": 
    n = 8 if len(sys.argv) < 2 else int(sys.argv[1])
    array = [8,4,7,0,2,9,6,9,3,2]
    print("Generating board")
    t = time.time()
    newPuzzle = puzzle(n)
    print("Board Generated in {:.5f}s".format(time.time() - t))

    if n < 17:
        printBoard(newPuzzle)
    else:
        print("Initial Pairs = {}".format(newPuzzle.pairsCount))

    if newPuzzle.pairsCount != 0:

        t = time.time()
        solution, i, solved = localSearch(newPuzzle, 10000, n)
        print("Time: {:.5f}s".format(time.time() - t))
        if solved: 
            print("=====================SOLUTION FOUND IN {} STEPS=====================".format(i))
            if n < 17:
                printBoard(solution)
            else:
                print("Initial Pairs = {}".format(newPuzzle.pairsCount))
            # else : 
                # print(solution)
        else: 
            print("=====================NO SOLUTION FOUND AFTER {} STEPS=====================".format(i))
            if n < 17:
                printBoard(solution)
            else:
                print("Initial Pairs = {}".format(newPuzzle.pairsCount))
            # else : 
                # print(solution)