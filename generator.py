from itertools import permutations
from itertools import combinations
import random
import numpy as np
ar = [i for i in range(100)]
number_file = open('data/generated/numbers.txt', 'w')
random.shuffle(ar)
random.shuffle(ar)
for n in ar:
    number_file.write(str(n)+",")
number_file.close()

random.shuffle(ar)
perms = permutations(ar, 25)


board_file = open('data/generated/boards.txt', 'w')
for p, i in enumerate(perms):
    # print(p)
    i = np.array(i)
    i = i.reshape((5, 5))
    for row in range(5):
        for col in range(5):
            board_file.write(str(i[row, col])+" ")
        board_file.write("\n ")

    board_file.write("\n")
    # print(i)
    if p == 1000000:
        break
board_file.close()
