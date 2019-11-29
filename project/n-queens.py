from random import randint
from operator import add
import time
import sys

import numpy as np

class Queen: 
    def __init__(self, col ,row, pairs=0): 
        self.col = col 
        self.row = row 
        self.pairsCount = pairs 
        self.pairs = []

    def __str__(self):
        return '\nCol={} , Row={} , Pairs={} '.format(self.col, self.row, self.pairsCount)

    def __repr__(self):
        return '\nCol={} , Row={} , Pairs={} '.format(self.col, self.row, self.pairsCount)

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
            self.queens = createBoard3(n)
        self.conflictQueens = []
        self.pairsCount = countPairs2(self,n)
        
    def __str__(self):
        return '\n Pairs = {}\n conflicted Queens = {}'.format( self.pairsCount,self.conflictQueens)

    def __repr__(self):
        return '\n Pairs = {} conflicted Queens = {}'.format( self.pairsCount,self.conflictQueens)

def createBoard(n):
    '''
    Creates the inital state of the board by adding the next queen to the spot with the least conflicts
    ---------------------------
    Params:
        n: the size of the board
    returns:
        puzzle: a 1-d list of size n containing a queen at each column
    '''

    queens = [Queen(0, randint(0, n - 1))]

    for cCol in range(1, n):
        f_row = [0] * n
        f_mdiag = [0] * n
        f_sdiag = [0] * n

        for i in range(len(queens)):

            row = queens[i].row
            if i != cCol:
                f_row[row] += 1

            if cCol <= row + i <= cCol + (n - 1):
                f_mdiag[row + i - cCol] += 1
            if cCol + 1 <= n - row + i <= n + cCol:
                f_sdiag[abs((n - row + i) - (n + cCol))] += 1

        total = list(map(add, list(map(add, f_row, f_mdiag)), f_sdiag))

        m = min(total)
        mins = [(x, i) for i, x in enumerate(total) if x == m]

        i = randint(0, len(mins) - 1)
        r = mins[i][1]

        queens.append(Queen(cCol, r))

    return queens

def createBoard2(n):
    '''
    Creates the inital state of the board by adding the next queen to the spot with the least conflicts
    ---------------------------
    Params:
        n: the size of the board
    returns:
        puzzle: a 1-d list of size n containing a queen at each column
    '''
    row = [0] * n
    ld = [0] * n
    rd = [0] * n

    i = randint(0, n - 1)

    row[i] += 1
    ld[i] += 1
    rd[i] += 1

    queens = [Queen(0, i)]

    for col in range(1, n):
        # t = time.time()
        q = queens[col - 1]
        ld = [0] + ld[:-1]
        rd = rd[1:] + [0]
        # print("Time 1:", time.time() - t) 

        # t = time.time()
        total = list(map(add, list(map(add, row, ld)), rd))
        # print("Time 2:", time.time() - t) 
        # t = time.time()
        m = min(total)
        mins = [(x, i) for i, x in enumerate(total) if x == m]
        # print("Time 3:", time.time() - t) 

        i = randint(0, len(mins) - 1)
        r = mins[i][1]

        row[r] += 1
        ld[r] += 1
        rd[r] += 1

        queens.append(Queen(col, r))
    return queens

def createBoard3(N):
    '''
    Creates the inital state of the board by adding the next queen to the spot with the least conflicts
    ---------------------------
    Params:
        n: the size of the board
    returns:
        puzzle: a 1-d list of size n containing a queen at each column
    '''
    row = np.zeros(N)
    ld = np.zeros(N)
    rd = np.zeros(N)

    total = row + ld + rd

    r = np.random.randint(0, N)

    row[r] = 1
    ld[r] = 1
    rd[r] = 1

    queens = [Queen(0, r)]

    for col in range(1, N):

        if N >= 100000:
            if col % 1000 == 0:
                print("Progress: {}/{}".format(col, N), end='\r') 
        
        q = queens[col - 1]
        ld = np.roll(ld, 1)
        ld[0] = 0
        rd = np.roll(rd, -1)
        rd[-1] = 0

        total = row + ld + rd

        minT = np.where(total == total.min())[0]
        # r = total[r]

        r = np.random.randint(0, minT.shape[0])
        r = minT[r]

        row[r] += 1
        ld[r] += 1
        rd[r] += 1

        queens.append(Queen(col, r))
    print()
    return queens

def countPairs(puzzle, n):
    '''
    Counts the total number of pairs in the board
    ---------------------------
    Params:
        puzzle: A puzzle for the current state
        n: the size of the board
    returns:
        counts: the count of the pairs
    '''
    totalPairs = 0 
    for i in range(n): 
        pairs =0 
        currentQueen = puzzle.queens[i]
        pairedArray = []
        j= 0 
        for j in range(n): #check other columns for value in same row
            if ((j != currentQueen.col and puzzle.queens[j].row == currentQueen.row) or (j != currentQueen.col and abs(puzzle.queens[j].col- currentQueen.col ) == abs(puzzle.queens[j].row - currentQueen.row ))  ): 
                pairs +=1
                pairedArray.append(puzzle.queens[j]) 


        if (pairs > 0  ): 
            currentQueen.pairs = pairedArray
            if (currentQueen not in puzzle.conflictQueens):
                puzzle.conflictQueens.append(currentQueen)
        else : 
            currentQueen.pairs = []
            if (currentQueen in puzzle.conflictQueens):
                puzzle.conflictQueens.remove(currentQueen)
        totalPairs += pairs
        currentQueen.pairsCount = pairs
    return totalPairs//2

def countPairs2(puzzle, n):
    '''
    Counts the total number of pairs in the board
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

    for i in range(n):
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

    for i in range(n + n):
        x, y, z = 0, 0, 0

        if i < n:
            x = f_row[i]
        y = f_mdiag[i]
        z = f_sdiag[i]

        count += (x * (x - 1)) // 2
        count += (y * (y - 1)) // 2
        count += (z * (z - 1)) // 2

    for q in queens:

        if q.row in cRow or q.row + q.col in cmD or n - q.row + q.col in csD:
            puzzle.conflictQueens.append(q)
    return count

def localSearch(puzzle, maxSteps, n):
    '''
    Performs min conflics local search of the puzzle
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
    savedInstances = [] 
    blacklistedQueens = []
    lastCount = 0 
    thisCount = 1
    for i in range(maxSteps):
        # if i %100 == 0: 
        #     print("BenchMark:", i)

        if lastCount == thisCount:
            for queen in puzzle.conflictQueens: 
                if (queen.col, queen.row) not in savedInstances: 
                    savedInstances.append((queen.col,queen.row))
        else : 
            savedInstances = []

        m = len(puzzle.conflictQueens)    

        index = randint(0, m - 1)
        currentQueen = puzzle.conflictQueens[index]

        pairMin, minRow = findMinimum2(currentQueen.row,currentQueen.col, puzzle,n,savedInstances)
        if (minRow != currentQueen.row): 
            puzzle.queens[currentQueen.col].row = minRow
            puzzle.queens[currentQueen.col].pairsCount = pairMin
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))
        else:
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))

        puzzle.pairsCount = countPairs2(puzzle,n)
        lastCount = thisCount 
        thisCount = puzzle.pairsCount

        if puzzle.pairsCount == 0: 
            return puzzle, i, True
    return puzzle, i, False

def findMinimum(row, col, puzzle, n, savedInstances):
    '''
    Finds the next move to do for a given queen that will minimize the conflicts
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
    queens = puzzle.queens
    pairMin= n + 1 
    MinRow = row
    MinRowArray = [] 
    for i in range(n): #put queen in n rows
        pairCount = 0 
        for j in range(n): #check other columns for value in same row
            if (j != col and queens[j].row == i ) or (j != col and abs(queens[j].row - i ) == abs(j - col )): 
                pairCount += 1 
                if pairMin < pairCount:
                    break

        if pairMin > pairCount:
            pairMin = pairCount
            MinRow = i
            MinRowArray= []
            MinRowArray.append(i)

        elif pairMin == pairCount and i != row:
            MinRow = i  
            MinRowArray.append(i)

        if pairMin == 0 : 
            return pairMin, MinRow


    for index in MinRowArray: 
        temp = (col , index)
        if temp not in savedInstances: 
            return pairMin, index 
    else : 
        return pairMin, MinRow

def findMinimum2(cRow, cCol, puzzle, n, savedInstances):
    '''
    Finds the next move to do for a given queen that will minimize the conflicts
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
    f_row = [0] * n
    f_mdiag = [0] * n
    f_sdiag = [0] * n
    queens = puzzle.queens

    cmD = cRow + cCol
    csD = n - cRow + cCol

    for i in range(n):

        row = queens[i].row
        if i != cCol:
            f_row[row] += 1

        if cCol <= row + i <= cCol + (n - 1):
            f_mdiag[row + i - cCol] += 1
        if cCol + 1 <= n - row + i <= n + cCol:
            f_sdiag[abs((n - row + i) - (n + cCol))] += 1

    total = list(map(add, list(map(add, f_row, f_mdiag)), f_sdiag))

    m = min(total)
    mins = [(x, i) for i, x in enumerate(total) if x == m]

    if mins[-1][0] == 0:
        return mins[-1]
    
    for x, i in mins:
        temp = (cCol, i)
        if temp not in savedInstances:
            return x, i
    else:
        return mins[-1]


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
        solution, i, solved = localSearch(newPuzzle, 4500, n)
        print("Time: {:.5f}s".format(time.time() - t))
        if solved: 
            print("=====================SOLUTION FOUND IN {} STEPS=====================".format(i))
            if n < 17:
                printBoard(solution)
            # else : 
                # print(solution)
        else: 
            print("=====================NO SOLUTION FOUND AFTER {} STEPS=====================".format(i))
            if n < 17:
                printBoard(solution)
            # else : 
                # print(solution)