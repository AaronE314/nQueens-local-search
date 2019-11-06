from queue import Queue
from copy import deepcopy

class Node:
    def __init__(self,row,col,value=None, domain=range(1, 10)):
        self.row = row
        self.col = col
        if value is not None: 
            self.value = int(value)
            self.domain = [int(value)]
        else : 
            self.value = value
            self.domain = list(domain)
        

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)

class Arc: 
    def __init__(self,Xi,Xj):
        self.Xi = Xi
        self.Xj = Xj 

    def evaluate(self):
        '''
        Evaluates arc
        ---------------------------
        returns:
            noSolution: whether or not the state of the puzzle is not solvable
            Checks : Xi != Xj and Xi domain not {}
        '''
        notSolvable = False 
        #enforcing arc consistency Xi != Xj 
        if(self.Xi.value is not None and self.Xi.value == self.Xj.value):
            notSolvable = True 
        elif (self.Xj.value != None and self.Xj.value in self.Xi.domain):
            self.Xi.domain.remove((self.Xj.value))
            if (len(self.Xi.domain)< 0 ): 
                notSolvable = True
        return notSolvable
                
            

        
def addNeighbours(queue,node, puzzle):
    currentRow = node.row
    currentColumn = node.col
    #grab neighbhors in nodes row
    i = currentRow
    for j in range(9): 
        if not (currentRow == i and currentColumn == j):
            queue.put(Arc(puzzle[i][j], node ))

    #grab neighbhors in nodes column
    j = currentColumn
    for i in range(9): 
        if not (currentRow == i and currentColumn == j):
            queue.put(Arc(puzzle[i][j], node ))

    #grab neighbhors in box
    row = (currentRow // 3) * 3
    col = (currentColumn // 3) * 3

    for i in range(3) :
        for j in range(3) :
            if not (currentRow == row +i and currentColumn == col+ j):
                queue.put(Arc(puzzle[row + i][col + j], node ))

def AC3(puzzle): 
    queue = Queue()
    
    #fill queue with initial constraints
    for row in puzzle:
        for node in row: 
            currentRow = node.row
            currentColumn = node.col
            #grab neighbhors in nodes row
            i = currentRow
            for j in range(9): 
                if not (currentRow == i and currentColumn == j):
                    queue.put(Arc(node,puzzle[i][j] ))

            #grab neighbhors in nodes column
            j = currentColumn
            for i in range(9): 
                if not (currentRow == i and currentColumn == j):
                    queue.put(Arc( node,puzzle[i][j] ))

            #grab neighbhors in box
            num_row = (currentRow // 3) * 3
            col = (currentColumn // 3) * 3

            for i in range(3) :
                for j in range(3) :
                    if not (currentRow == num_row +i and currentColumn == col+ j):
                        queue.put(Arc(node,puzzle[num_row+ i][col+j] ))
                        
    noSolution = False
    while (queue.qsize() >  0  and not noSolution): 
        #Get first Node
        arc = queue.get_nowait()
        node = arc.Xi
        
        #get needed attributes
        domainCount = len(node.domain)
        noSolution= arc.evaluate()
        newDomainCount = len(node.domain)
        if newDomainCount == 1 :
            node.value = node.domain[0]
        if newDomainCount < domainCount:
            addNeighbours(queue,node,puzzle)

    i=0 
    j= 0 
    #checking if puzzle is solved
    noneValueFound= False
    while (i < 9 and not noneValueFound):
        j = 0
        while(j < 9 and not noneValueFound):
            if puzzle[i][j].value is None: 
                noneValueFound = True
            j+=1
        i +=1 
    return puzzle, not noneValueFound, noSolution




def loadPuzzle(file='./puzzles/easy.csv', num=1, header=True, start=0):
    '''
    Loads a puzzle from a file
    ---------------------------
    Params (optional):
        file: the file to load, defaults to puzzle/easy.csv
        num: the number of puzzles to load, defaults to 1
        header: if the file has a header or not, defaults to True
        start: what line to start reading the puzzle from
    returns:
        puzzle: a 2d array of Nodes representing the puzzle
        solution: a 2d array of Nodes representing the solution of the puzzle
        Note: if num > 1 will return an array of puzzles and and array of solutions
    '''
    with open(file, 'r') as f:
        
        if num > 1:
            puzzles = []
            solutions = []

        for i, line in enumerate(f):
            if header and i == 0:
                start += 1
                continue

            if i < start:
                continue
        
            if i > start + num:
                break

            puzzleAndSol = line.split(',')

            puzzle = []
            for j in range(9):
                row = []
                for k in range(9):
                    row.append(Node(j, k, None if puzzleAndSol[0][j*(9) + k] == '.' else puzzleAndSol[0][j*(9) + k]))
                puzzle.append(row)

            solution = []
            for j in range(9):
                row = []
                for k in range(9):
                    row.append(Node(j, k, None if puzzleAndSol[1][j*(9) + k] == '.' else puzzleAndSol[1][j*(9) + k]))
                solution.append(row)

            if num > 1:
                puzzles.append(puzzle)
                solutions.append(solution)
    if num > 1:
        return puzzles, solutions
    else:
        return puzzle, solution

def backtrackSearch(puzzle):
    '''
    Performs a backtracking search on a csp sudoku
    ---------------------------
    Param:
        puzzle: A 2d array of Node objects
    returns:
        A solved sudoku puzzle
        A boolean of if the puzzle is solved or not
    '''

    # Find the starting node based on the degree heuristic
    # ie selecting the node with largest amount of constraints
    firstNode = None
    for row in puzzle:
        for node in row:
            if node.value is None and (firstNode is None or len(firstNode.domain) < len(node.domain)):
                firstNode = node

    # Starts the backtracking
    return backtrack(puzzle, firstNode.row, firstNode.col)

def backtrack(puzzle, row, col):
    '''
    Auxiliary Performs a backtracking search on a csp sudoku
    ---------------------------
    Params:
        puzzle: A 2d array of Node objects
        row: The row of the current node
        col: The col of the current node
    returns:
        A solved sudoku puzzle
        A boolean for if the puzzle is solved or not
    '''
    
    # Check if the puzzle is finished, if it is we are done
    # and collapse the call stack
    if complete(puzzle):
        return puzzle, True

    # Get the order of the domain using the
    # least consraining value heuristic
    domainOrder = order(row, col, puzzle)

    for value in domainOrder:

        # Check if the current value in the domain is consistant
        # with the constraints of the sudoku
        # Should always be consisitant
        if valid(puzzle, row, col, value):
            
            # Store a copy of the current state for
            # the backtracking
            state = deepcopy(puzzle)

            # Update the value of the current node
            puzzle[row][col].value = value

            # Make the updated puzzle arc consistant
            puzzle, completed, noSolution = AC3(puzzle)

            # If the puzzle still has a solution
            # We can continue, Otherwise we move on 
            if not noSolution:
                if not completed:
                    # Figure out which node we should check next using
                    # MRV
                    nextNode = getNextNode(puzzle)

                    # Call the next node
                    puzzle, completed = backtrack(puzzle, nextNode.row, nextNode.col)

                    # We returned from the backtracking
                    # if completed then we are done
                    # collapse the call stack
                    if completed:
                        return puzzle, completed

                else:
                    return puzzle, completed
        # we returned from the backtracking
        # or the value is invalid
        # so restore the starting state
        # remove the value from the domain
        # and continue to the next value in the domain
        puzzle = state
        puzzle[row][col].domain.remove(value)
    puzzle[row][col].value = None

    # This value had no values in its domain that worked
    # Backtrack to previous node
    return puzzle, False

def valid(puzzle, row, col, value):
    '''
    Checks if a value is valid with the contraint
    ---------------------------
    Params:
        puzzle: A 2d array of Node objects
        row: The row of the current node
        col: The col of the current node
        value: The value you are checking that works
    returns:
        True if the value is valid, false otherwise
    '''
    node = puzzle[row][col]

    # Row
    col = node.col
    for row in range(9):
        if puzzle[row][col].value == value:
            return False
    
    # Column
    row = node.row
    for col in range(9):
        if puzzle[row][col].value == value:
            return False
    # Box
    row = (node.row // 3) * 3
    col = (node.col // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[row + i][col + j].value == value:
                return False
    return True

def order(row, col, puzzle):
    '''
    returns the order of the domain to check using the least
    contraining value heuristic
    ---------------------------
    Params:
        row: The row of the current node
        col: The col of the current node
        puzzle: A 2d array of Node objects
    returns:
        The domain as a new array in the order to use
    '''
    # TODO: Change this to use the least constraining value heuristic
    return deepcopy(puzzle[row][col].domain)

    # order = []
    # for value in node.domain:
    #     minDomain = 9
    #     count = 0
    #     # Row
    #     col = node.col
    #     for row in range(9):
    #         if value in puzzle[row][col].domain:
    #             minDomain = min(minDomain, len(puzzle[row][col].domain) - 1)
    #         else:
    #             minDomain = min(minDomain, len(puzzle[row][col].domain))
        
    #     # Column
    #     row = node.row
    #     for col in range(9):
    #         if puzzle[row][col] == value:
    #             return False
    #     # Box
    #     row = (node.row // 3) * 3
    #     col = (node.col // 3) * 3
    #     for i in range(3):
    #         for j in range(3):
    #             if puzzle[row + i][col + j] == value:
    #                 return False
    # return sorted(order, key=lambda x: x[1])


def complete(puzzle):
    '''
    Checks if the puzzle is solved
    ---------------------------
    Params:
        puzzle: A 2d array of Node objects
    returns:
        True if every node has a value, false otherwise
    '''
    for i in range(9):
        for j in range(9):
            if puzzle[i][j].value == None:
                return False

    return True


def getNextNode(puzzle):
    '''
    returns the next node to check using MRV
    ---------------------------
    Params:
        puzzle: A 2d array of Node objects
    returns:
        The next node to search
    '''
    nextNode = None
    for row in puzzle:
        for node in row:
            if node.value is None and (nextNode is None or len(nextNode.domain) > len(node.domain)):
                nextNode = node
    return nextNode

def print_board(puzzle, detailed=False):

    print('- ' * 13)
    for row in puzzle:
        print('|', end=' ')
        for col in row:
            if detailed:
                domain = ''.join(str(x) for x in col.domain)
                print("[{} ({:9s})]".format(col.value if col.value else '.', domain), end=' ')
            else:
                print(col.value if col.value else '.', end=' ')
            if col.col % 3 == 2:
                print('|', end=' ')
        print()
        if col.row % 3 == 2:
            print('- ' * 13)

if __name__ == "__main__":
    q = Queue()
    p, s = loadPuzzle()
    # addNeighbours(q, p[0][0], p)
    # print(q.qsize())
    # while not q.empty():
    #     print(q.get_nowait())
    print_board(p)

    print()
    print("=========Solved===========")
    print()
    finishedPuzzle, completed, noSolution = AC3(p)
    if completed:
        print("Sudoku solved")
        print_board(finishedPuzzle)
    elif noSolution:
        print('No Solution!')
    else:
        print('Board after AC3')
        print_board(finishedPuzzle)
        print('Starting Backtracking')

        finishedPuzzle, finished = backtrackSearch(finishedPuzzle)
        print('Board after Backtracking')
        print('Solved =', finished)
        print_board(finishedPuzzle)

    print('Actual Solution')
    print_board(s)
    