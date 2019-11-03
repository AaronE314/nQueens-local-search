from queue import Queue

class Node:
    def __init__(self,row,col,value=None, domain=range(1, 10)):
        self.row = row
        self.col = col
        self.value = value
        self.domain = list(domain)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.row, self.col, self.value, self.domain)

def addNeighbours(queue,node, puzzle):
    currentRow = node.row
    currentCollumn = node.col
    #grab neighbhors in nodes row
    i = currentRow
    for j in range(9): 
        if not (currentRow == i and currentCollumn == j):
            queue.put(puzzle[i][j])

    #grab neighbhors in nodes column
    j = currentCollumn
    for i in range(9): 
        if not (currentRow == i and currentCollumn == j):
            queue.put(puzzle[i][j])

    #grab neighbhors in box
    row = (currentRow // 3) * 3
    col = (currentCollumn // 3) * 3

    for i in range(3) :
        for j in range(3) :
            if not (currentRow == row +i and currentCollumn == col+ j):
                queue.put(puzzle[row +i][col+ j])
   
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