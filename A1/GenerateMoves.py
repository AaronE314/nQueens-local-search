from itertools import combinations
from copy import deepcopy
from queue import Queue

solutions = []
hashTable= {}
class Tree:

    def __init__(self, state, parent = None, action = None, pathCost = 0):
        self.children = []
        self.state = state
        self.parent = parent
        self.action = action
        self.pathCost = pathCost
        self.SOLUTION = [[0, 0], [3, 3], 'R']

        if state == self.SOLUTION:
            solutions.append(self)
            return

        self.addAllChildren()
    
    # TODO: Needs to be optimized
    # ! Aaron to do this
    def addAllChildren(self):
        
        if self.check():
            options = ''
            count = 0

            if self.state[2] == 'L':
                options += min(self.state[0][0], 2) * 'M'
                options += min(self.state[0][1], 2) * 'C'

                count = min(self.state[0][0] + self.state[0][1], 2)
            else:
                options += min(self.state[1][0], 2) * 'M'
                options += min(self.state[1][1], 2) * 'C'
                count = min(self.state[1][0] + self.state[1][1], 2)

            comb = set(combinations(options, 1))
            if count > 1:
                comb = comb.union(set(combinations(options, 2)))

            for com in comb:

                m = com.count('M')
                c = com.count('C')

                if self.action is None or not (m == self.action[0] and c == self.action[1]):
                    self.children.append(Tree(self.move((m, c)), self, (m, c), self.pathCost + 1))

    def move(self, moves):

        newState = deepcopy(self.state)

        if newState[2] == 'L':
            newState[1][0] += moves[0]
            newState[1][1] += moves[1]
            newState[0][0] -= moves[0]
            newState[0][1] -= moves[1]
        else:
            newState[0][0] += moves[0]
            newState[0][1] += moves[1]
            newState[1][0] -= moves[0]
            newState[1][1] -= moves[1]

        newState[2] = 'L' if newState[2] == 'R' else 'R'

        return newState

    def check(self):

        return not (((self.state[0][0] < self.state[0][1]) and self.state[0][0] != 0) or ((self.state[1][0] < self.state[1][1]) and self.state[1][0] != 0) or self.isInTree())

    # TODO: Needs to be optimized
    # ! Austin to do this
    def isInTree(self):
        
        key = "{}{}{}{}{}".format(self.state[0][0],self.state[0][1],self.state[1][0],self.state[1][1],self.state[2])
        table = hashTable
        value = table.get(key)
        print("--------------")
        print("new Key = ",key)
        print(table)

        if value == None: #value doesnt exist in the table
            print("False")
            table[key] = True
            print("--------------")
            return False
        print("True")
        print("--------------")
        return True


    def __str__(self, level=0):
        ret = "\t" * level + repr(self.state) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

def print_solution(end):
    s = []
    
    node = end

    while node is not None:
        s.append(node)
        node = node.parent

    print("=" * 20)
    while len(s) != 0:
        n = s.pop()

        p = "({:3} {:3} | {:3} {:3})[{:1}]".format(n.state[0][0] * 'M', n.state[0][1] * 'C', 
                                                   n.state[1][0] * 'M', n.state[1][1] * 'C', n.state[2])
        print(p)

    print("=" * 20)
    print()


def main():
            # Left side, Right side
            #[[M, C], [M, C], 'Side boat is on']
            # Cost of each action is 1
    root = Tree([[3, 3], [0, 0], 'L'])

    print(root)
    
    for solution in solutions:
        print_solution(solution)
    

if __name__ == "__main__":
    main()