class Node:
    def __init__(self,i,j,value=None, domain=[1,2,3,4,5,6,7,8,9]):
        self.i = i
        self.j = j
        self.value = value
        self.domain = domain

def addNeighbhors(queue,node, puzzle):
    currentRow = node.i
    currentCollumn = node.j 
    #grab neighbhors in nodes row
    i = currentRow
    for j in range(9): 
        if (currentRow != i and currentCollumn != j):
            queue.add(puzzle[i][j])

    #grab neighbhors in nodes column
    j = currentCollumn
    for i in range(9): 
        if (currentRow != i and currentCollumn != j):
            queue.add(puzzle[i][j])

    #grab neighbhors in box
    row = (currentRow / 3) * 3
    col = (currentCollumn / 3) * 3

    for i in range(3) :
        for j in range(3) :
            if (currentRow != i and currentCollumn != j):
                queue.add(puzzle[i][j])
            
     




def load_puzzle(file='./puzzles/easy.csv', num=1, header=True):

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
                val = j+(j*8)
                puzzle.append(puzzleAndSol[0][val:val+9])

            solution = []
            for j in range(9):
                val = j+(j*8)
                solution.append(puzzleAndSol[1][val:val+9])

            if num > 1:
                puzzles.append(puzzle)
                solutions.append(solution)
    if num > 1:
        return puzzles, solutions
    else:
        return puzzle, solution
