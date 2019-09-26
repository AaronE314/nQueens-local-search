
import random
import sys

def nQueens(n):
    show(min_conflicts(list(range(n)), n), n)

def show(soln, n):
    for i in range(n):
        row = ['~'] * n
        for col in range(n):
            if soln[col] == n - 1 - i:
                row[col] = 'Q'
        print(''.join(row))

def min_conflicts(soln, n, iters=1000):
    
    def random_pos(li, filt):
        return random.choice([i for i in range(n) if filt(li[i])])

    for k in range(iters):
        confs = find_conflicts(soln, n)
        
        if sum(confs) == 0:
            return soln
        
        col = random_pos(confs, lambda elt: elt > 0)
        vconfs = [hits(soln, n, col, row) for row in range(n)]
        soln[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))
    raise Exception("Incomplete solution: try more iterations")

def find_conflicts(soln, n):
    return [hits(soln, n, col, soln[col]) for col in range(n)]

def hits(soln, n, col, row):
    
    total = 0
    for i in range(n):
        if i == col:
            continue
        if soln[i] == row or abs(i - col) == abs(soln[i] - row):
            total += 1
    return total

if __name__ == '__main__':
    size = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    nQueens(size)
