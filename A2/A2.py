class Node:
    def __init__(self,i,j,value=none, domain=[1,2,3,4,5,6,7,8,9]):
        self.i = i
        self.j = i
        self.value = value
        self.domain = domain



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
