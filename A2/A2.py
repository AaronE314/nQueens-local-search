

def load_puzzle(file='./puzzles/easy.csv', num=1, header=True):

    with open(file, 'r') as f:
        
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
    return puzzle, solution
