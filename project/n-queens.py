import numpy as np 

class Queen : 
    def __init__(self, col ,row,pairs=0 ): 
        self.col = col 
        self.row = row 
        self.pairsCount = pairs 
        self.pairs = []

    def __str__(self):
        return '\ncol={} , Y={} , Pairs={} '.format(self.col, self.row, self.pairsCount)

    def __repr__(self):
        return '\nCol={} , Y={} , Pairs={} '.format(self.col, self.row, self.pairsCount)

    def __eq__(self,other): 
        return self.col == other.col

    def __ne__(self,other):
        return not self.__eq__(other)

class puzzle: 
    def __init__(self, n  ): 
    
        #random initial state, could be greedy
        self.queens = []
        for i in range(n): 
            self.queens.append(Queen(i, np.random.randint(0,n)))

        self.conflictQueens = []
        self.pairsCount = countPairs(self,n)
        
    def __str__(self):
        return 'Queens Rows = {}\n Pairs = {}\n conflicted Queens = {}'.format(self.queens, self.pairsCount,self.conflictQueens)

    def __repr__(self):
        return 'Queens Rows = {}\n Pairs = {} conflicted Queens = {}'.format(self.queens, self.pairsCount,self.conflictQueens)

#TODO
#this function recalculates the number of pairs in the puzzle 
def countPairs(puzzle,n ):
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

#TODO
#this is the main driver for finding the solution
def localSearch(puzzle , maxSteps, n ):
    blacklistedQueens = []
    for i in range(maxSteps):
        #if (i %100 == 0  ): 
        #    print("BenchMark")

        m = len(puzzle.conflictQueens)    

        index = np.random.randint(0,m )
        currentQueen = puzzle.conflictQueens[index]
        while(currentQueen in blacklistedQueens): 
            index = np.random.randint(0,m )
            currentQueen = puzzle.conflictQueens[index]


        pairMin, minRow = findMinimum(currentQueen.row,currentQueen.col, puzzle,n) 
        if (minRow != currentQueen.row): 
            puzzle.queens[currentQueen.col].row = minRow
            blacklistedQueens = []
            blacklistedQueens.append(currentQueen)
        else :
             blacklistedQueens.append(currentQueen)
        puzzle.pairsCount = countPairs(puzzle,n )
        print("----------------------------------")
        printBoard(puzzle)
        print()
        print(puzzle)
        print("----------------------------------")
        if (puzzle.pairsCount == 0 ): 
            return puzzle, i, True
    return puzzle , i ,False

#TODO
#this is the function that will be called by localSearch() to decide which step to take next
#any ties broken by breakTies()
def findMinimum(row, col, puzzle, n  ):
    queens = puzzle.queens
    pairMin= n + 1 
    MinRow = row
    for i in range(n): #put queen in n rows
        pairCount = 0 
        for j in range(n): #check other columns for value in same row
            if (j != col and queens[j].row == i ) or (j != col and abs(queens[j].row - i ) == abs(j - col )): 
                pairCount +=1 

        if (pairMin > pairCount):
            pairMin = pairCount
            MinRow = i

        elif(pairMin == pairCount and i != row):
            MinRow = i  

        if (pairMin == 0 ): 
            return pairMin, MinRow


    return pairMin, MinRow

#TODO 
# This is the name of the search algo that stops the 'plateau' effect. when all moves on the board have the same minimum but none are solutions 
def tabuSearch():
    print()

#TODO
#heuristically break ties found by findMinimum()
def breakTies():
    print()

def printBoard(puzzle):
    arr = puzzle.queens
    for i in range(n-1 , -1 ,-1 ):#rows 
        for j in range(n):#column
            if (arr[j].row == i ): 
                print("Q|",end = "")
            else : 
                print(".|",end="")
        print()
        #print("-"*n*2)
    print("Pairs = {}".format(puzzle.pairsCount))

if __name__ == "__main__": 
    n = 4
    newPuzzle = puzzle(n )
    print(newPuzzle)
    printBoard(newPuzzle)
    solution, i,solved  = localSearch(newPuzzle,10,n)
    if solved: 
        print("=====================SOLUTION FOUND IN {} STEPS=====================".format(i))
        printBoard(solution)
    else: 
        print("=====================NO SOLUTION FOUND AFTER {} STEPS=====================".format(i))
        printBoard(newPuzzle)