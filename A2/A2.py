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
                for k in range(9):
                    puzzle.append(Node(j, k, None if puzzleAndSol[0][j*(9) + k] == '.' else puzzleAndSol[0][j*(9) + k]))

            solution = []
            for j in range(9):
                for k in range(9):
                    solution.append(Node(j, k, None if puzzleAndSol[1][j*(9) + k] == '.' else puzzleAndSol[1][j*(9) + k]))

            if num > 1:
                puzzles.append(puzzle)
                solutions.append(solution)
    if num > 1:
        return puzzles, solutions
    else:
        return puzzle, solution

if __name__ == "__main__":
    # print(load_puzzle())
    pass