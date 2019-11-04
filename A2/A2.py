from queue import Queue

class Node:
    def __init__(self,row,col,value=None, domain=range(1, 10)):
        self.row = row
        self.col = col
        if value is not None: 
            self.value = int(value)
        else : 
            self.value =value
        self.domain = list(domain)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)


def addNeighbours(queue,node, puzzle):
    currentRow = node.row
    currentColumn = node.col
    #grab neighbhors in nodes row
    i = currentRow
    for j in range(9): 
        if not (currentRow == i and currentColumn == j):
            queue.put(puzzle[i][j])

    #grab neighbhors in nodes column
    j = currentColumn
    for i in range(9): 
        if not (currentRow == i and currentColumn == j):
            queue.put(puzzle[i][j])

    #grab neighbhors in box
    row = (currentRow // 3) * 3
    col = (currentColumn // 3) * 3

    for i in range(3) :
        for j in range(3) :
            if not (currentRow == row +i and currentColumn == col+ j):
                queue.put(puzzle[row +i][col+ j])

def AC3(puzzle): 
    queue = Queue()
    
    #fill queue with initial constraints
    for row in puzzle:
        for node in row: 
            queue.put(node)

    noSolution = False
    while (queue.qsize() >  0  and not noSolution): 
        #Get first Node
        node = queue.get_nowait()
        if node.value is None: 
            #get needed attributes

            currentRow = node.row
            currentColumn = node.col
            domainCount = len(node.domain)
            #grab neighbhors in nodes row
            i = currentRow
            for j in range(9): 
                #checking Arc (Xi,Xj) where Xi != Xj. if Xj has value , remove it from Xi's domain
                Xj = puzzle[i][j]
                if (Xj.value != None and Xj.value in node.domain):
                    node.domain.remove((Xj.value))
                
                    

            #grab neighbhors in nodes column
            j = currentColumn
            for i in range(9): 
                #checking Arc (Xi,Xj) where Xi != Xj. if Xj has value , remove it from Xi's domain
                Xj = puzzle[i][j]
                if (Xj.value != None and Xj.value in node.domain):
                    node.domain.remove((Xj.value))
                
            #grab neighbhors in box
            row = (currentRow // 3) * 3
            col = (currentColumn // 3) * 3

            for i in range(3) :
                for j in range(3) :
                #checking Arc (Xi,Xj) where Xi != Xj. if Xj has value , remove it from Xi's domain
                    Xj = puzzle[row + i][col + j]
                    if (Xj.value != None and Xj.value in node.domain):
                        node.domain.remove((Xj.value))


            newDomainCount = len(node.domain)
            if newDomainCount == 1 :
                node.value = node.domain[0]
            elif newDomainCount == 0 : 
                noSolution = True
            
            if newDomainCount < domainCount:
                addNeighbours(queue,node,puzzle)

    i=0 
    j= 0 
    #checking if puzzle is solved
    noneValueFound= False
    while (i < 9 and not noneValueFound):
        while(j < 9 and not noneValueFound):
            if puzzle[i][j].value is None: 
                noneValueFound = True
            j+=1
        i +=1 
    return puzzle, not noneValueFound




def loadPuzzle(file='./puzzles/easy.csv', num=1, header=True):

    with open(file, 'r') as f:
        
        if num > 1:
            puzzles = []
            solutions = []

        for i, line in enumerate(f):
            if header and i == 0:
                continue
        
            if i > num:
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

def print_board(puzzle):

    print('- ' * 13)
    for row in puzzle:
        print('|', end=' ')
        for col in row:
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
    finishedPuzzle, completed = AC3(p)
    if (completed):
        print("Sudoku solved")
    print_board(finishedPuzzle)