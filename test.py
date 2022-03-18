import numpy as np
import timeit

x = np.random.randint(1000000, size=1000000)
y = np.random.randint(1000000, size=1000000)
z = np.random.randint(1000000, size=1000000)
# or 
#x = np.random.standard_normal(1000)

def pure_sum():
    return x + y + z

def numpy_sum():
    return np.add(np.add(x, y), z)

def roll():
    ld = np.roll(x, 1)
    ld[0] = 0
    return ld

def sliceRoll():
    return np.concatenate(([0], x[:-1]))

n = 10000

t1 = timeit.timeit(roll, number = n)
print('Pure Python Sum:', t1)
t2 = timeit.timeit(sliceRoll, number = n)
print('Numpy Sum:', t2)