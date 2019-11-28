from random import randint
import time

class Queen : 
    def __init__(self, col ,row,pairs=0 ): 
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
    def __init__(self, n  ,array= None): 
    
        #random initial state, could be greedy
        self.queens = []
        if array is not None : 
            for i in range(n): 
                self.queens.append(Queen(i, array[i]))
        else : 
            for i in range(n): 
                self.queens.append(Queen(i,randint(0,n - 1)))
        self.conflictQueens = []
        self.pairsCount = countPairs(self,n)
        
    def __str__(self):
        return '\n Pairs = {}\n conflicted Queens = {}'.format( self.pairsCount,self.conflictQueens)

    def __repr__(self):
        return '\n Pairs = {} conflicted Queens = {}'.format( self.pairsCount,self.conflictQueens)

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
    savedInstances = [] 
    blacklistedQueens = []
    lastCount = 0 
    thisCount = 1
    for i in range(maxSteps):
        # if (i %100 == 0  ): 
            # print(puzzle.conflictQueens)
            # print("BenchMark")

        if (lastCount == thisCount ):
            # print("CONFLICT")
            for queen in puzzle.conflictQueens: 
                if (queen.col, queen.row) not in savedInstances: 
                    savedInstances.append((queen.col,queen.row))
            # print(savedInstances)
        else : 
            savedInstances = []

        m = len(puzzle.conflictQueens)    

        index = randint(0,m - 1 )
        currentQueen = puzzle.conflictQueens[index]
        # print(currentQueen)
        # while(currentQueen in blacklistedQueens): 
        #     index = np.random.randint(0,m )
        #     currentQueen = puzzle.conflictQueens[index]
        #     if len(puzzle.conflictQueens) == len(blacklistedQueens):
        #         print("LOCAL MINIMA FOUND")
        #         return puzzle , i ,False


        pairMin, minRow = findMinimum(currentQueen.row,currentQueen.col, puzzle,n,savedInstances) 
        if (minRow != currentQueen.row): 
            puzzle.queens[currentQueen.col].row = minRow
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))
        else :
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))


        puzzle.pairsCount = countPairs(puzzle,n )
        lastCount = thisCount 
        thisCount = puzzle.pairsCount
        # print("----------------------------------")
        # printBoard(puzzle)
        # print()
        # print(puzzle)
        # print("----------------------------------")
        if (puzzle.pairsCount == 0 ): 
            return puzzle, i, True
    return puzzle , i ,False

#TODO
#this is the function that will be called by localSearch() to decide which step to take next
#any ties broken by breakTies()
def findMinimum(row, col, puzzle, n,savedInstances  ):
    queens = puzzle.queens
    pairMin= n + 1 
    MinRow = row
    MinRowArray = [] 
    for i in range(n): #put queen in n rows
        pairCount = 0 
        for j in range(n): #check other columns for value in same row
            if (j != col and queens[j].row == i ) or (j != col and abs(queens[j].row - i ) == abs(j - col )): 
                pairCount +=1 

        if (pairMin > pairCount):
            pairMin = pairCount
            MinRow = i
            MinRowArray= []
            MinRowArray.append(i)

        elif(pairMin == pairCount and i != row):
            MinRow = i  
            MinRowArray.append(i)

        if (pairMin == 0 ): 
            return pairMin, MinRow


    for index in MinRowArray: 
        temp = (col , index)
        if temp not in savedInstances: 
            return pairMin, index 
    else : 
        return pairMin, MinRow

#TODO 
# This is the name of the search algo that stops the 'plateau' effect. when all moves on the board have the same minimum but none are solutions 
def tabuSearch(puzzle, maxSearch):
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
    n = 100
    array = [8,4,7,0,2,9,6,9,3,2]
    newPuzzle = puzzle(n  )
    #print(newPuzzle)
    #printBoard(newPuzzle)
    t = time.time()
    solution, i,solved  = localSearch(newPuzzle,4500,n)
    print("Time: ", time.time() - t)
    if solved: 
        print("=====================SOLUTION FOUND IN {} STEPS=====================".format(i))
        if n < 17:
            printBoard(solution)
        else : 
            print(solution)
    else: 
        print("=====================NO SOLUTION FOUND AFTER {} STEPS=====================".format(i))
        if n < 17:
            printBoard(solution)
        else : 
            print(solution)