import sys
sys.path.append("..")

# d = 9
# coordinates = np.zeros((d*d, 2))
# coordinates[:, 0] = np.repeat(np.arange(d), d)
# coordinates[:, 1] = np.tile(np.arange(d), d)
# distance = squareform(pdist(coordinates, 'minkowski', 1))
# M = np.maximum(4 - distance, 0)
# print M[:10,:10] 


import matplotlib.pyplot as plt

from structure import board
from structure import const

CONST = const.CONST
d = CONST.d()
# I, I_boundary = adversarial(d)
# print I_boundary.reshape(d,d)
# Iw, Ib = influence(I, I_boundary, [12, 5, 8], [])

test_board = board.Board(d)

test_board.set_boundary('empty')
Iw, Ib = test_board.get_influence([12, 5], [0])
print Iw.reshape(d,d)
plt.matshow(Iw.reshape(d,d))
plt.show()
