from random import randint

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
        if (i %100 == 0  ): 
            #print(puzzle.conflictQueens)
            print("BenchMark")

        if (lastCount == thisCount ):
            print("CONFLICT")
            for queen in puzzle.conflictQueens: 
                if (queen.col, queen.row) not in savedInstances: 
                    savedInstances.append((queen.col,queen.row))
            # print(savedInstances)
        else : 
            savedInstances = []

        m = len(puzzle.conflictQueens)    

        index = randint(0,m-1 )
        currentQueen = puzzle.conflictQueens[index]
        # print(currentQueen)
        # while(currentQueen in blacklistedQueens): 
        #     index = np.random.randint(0,m )
        #     currentQueen = puzzle.conflictQueens[index]
        #     if len(puzzle.conflictQueens) == len(blacklistedQueens):
        #         print("LOCAL MINIMA FOUND")
        #         return puzzle , i ,False


        pairMin, minRow = findMinimum( puzzle,n,savedInstances, currentQueen) 
        if (minRow != currentQueen.row): 
            puzzle.queens[currentQueen.col].row = minRow
            puzzle.queens[currentQueen.col].pairsCount = pairMin
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))
        else :
            if (currentQueen.col, currentQueen.row) not in savedInstances: 
                    savedInstances.append((currentQueen.col,currentQueen.row))


        puzzle.pairsCount = countPairs(puzzle,n )
        lastCount = thisCount 
        thisCount = puzzle.pairsCount
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
def findMinimum( puzzle, n,savedInstances ,currentQueen ):
    row= currentQueen.row
    col=currentQueen.col
    queens = puzzle.queens
    pairMin= n + 1 
    MinRow = row
    MinRowArray = [] 
    minQueenPairsArray = []
    for i in range(n): #put queen in n rows
        pairCount = 0 
        tempArr = []
        for j in range(n): #check other columns for value in same row
            if (j != col and queens[j].row == i ) or (j != col and abs(queens[j].row - i ) == abs(j - col )): 
                pairCount +=1 
                tempArr.append(queens[j])


        if (pairMin > pairCount):
            pairMin = pairCount
            MinRow = i
            MinRowArray= []
            minQueenPairsArray = []
            MinRowArray.append(i)
            minQueenPairsArray.append(tempArr)

        elif(pairMin == pairCount and i != row):
            MinRow = i  
            MinRowArray.append(i)
            minQueenPairsArray.append(tempArr)

        if (pairMin == 0 ): 
            minQueenPairsArray= []

            #updatePairs(0 , minQueenPairsArray, currentQueen, puzzle,pairMin)
            return pairMin, MinRow

    i = 0 
    for index in MinRowArray: 
        temp = (col , index)
        if temp not in savedInstances:
            #updatePairs(i , minQueenPairsArray, currentQueen, puzzle,pairMin)
            return pairMin, index 
        i +=1 

    #updatePairs(-1 , minQueenPairsArray, currentQueen, puzzle,pairMin)
    return pairMin, MinRow

def updatePairs(index , minQueenPairsArray, currentQueen, puzzle,pairMin):
    print(currentQueen)
    print(currentQueen.pairs)
    for queen in currentQueen.pairs: 
        print(queen)
        print(queen.pairs)
        queen.pairs.remove(currentQueen)
        queen.pairsCount -=1 
        if queen.pairsCount == 0: 
            puzzle.conflictQueens.remove(queen)



    if len(minQueenPairsArray) > 0 : 
        for queen in minQueenPairsArray[index]:
            queen.pairs.append(currentQueen)
            queen.pairsCount +=1 
            if queen.pairsCount == 1 : 
                puzzle.conflictQueens.append(queen)

    puzzle.pairsCount = puzzle.pairsCount - currentQueen.pairsCount + pairMin
         

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
    n = 10
    array = [8,4,7,0,2,9,6,9,3,2]
    newPuzzle = puzzle(n  )
    #print(newPuzzle)
    printBoard(newPuzzle)
    solution, i,solved  = localSearch(newPuzzle,4500,n)
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