import numpy as np
from scipy.spatial.distance import pdist, cdist, squareform

class Board(object):
    """docstring for structure"""
    def __init__(self, size):
        self.size = size
        coordinates = np.zeros((size * size, 2))
        coordinates[:, 0] = np.repeat(np.arange(size), size)
        coordinates[:, 1] = np.tile(np.arange(size), size)
        self.coordinates = coordinates
        self.distance = squareform(pdist(coordinates, 'minkowski', 1))

    def set_boundary(self, boundary):
        self.boundary = boundary
        self.initialize(boundary)

    def initialize(self, boundary):
        if boundary == 'empty':
            self.empty()
        elif boundary == 'dynamic':
            self.dynamic()
        elif boundary == 'adversarial':
            self.adversarial()
        else:
            print 'not implemented!'
            
    def coo2idx(self, i, j):
        return i * self.size + j

    def idx2coo(self, idx):
        return idx // self.size, idx % self.size
    
    def shift(self, idx, di, dj):
        i, j = self.idx2coo(idx)
        if i + di >= self.size or i + di < 0:
            return -1
        if j + dj >= self.size or j + dj < 0:
            return -1
        return self.coo2idx(i + di, j + dj)

    def empty(self):
        corner_idx = np.array([0, self.size - 1, self.size * (self.size - 1), self.size * self.size - 1])
        bd_idx = np.zeros((self.size - 2) * 4, dtype = int)
        bd_idx[0 : self.size - 2] = np.arange(1, self.size - 1)
        bd_idx[self.size - 2 : 2 * (self.size - 2)] = np.arange(self.size, self.size * (self.size - 1), self.size)
        bd_idx[2 * (self.size - 2) : 3 * (self.size - 2)] = np.arange(2 * self.size - 1, self.size * self.size - 1, self.size)
        bd_idx[3 * (self.size - 2) : 4 * (self.size - 2)] = np.arange(self.size * (self.size - 1) + 1, self.size * self.size - 1)
        self.I = np.maximum(4 - self.distance, 0)
        self.I[:, corner_idx] = np.maximum(self.I[:, corner_idx] - 2, 0)
        self.I[:, bd_idx] = np.maximum(self.I[:, bd_idx] - 1, 0)
        self.I_boundary = 0

    def dynamic(self):
        return 

    def adversarial(self):
        ext_bound = np.zeros((4 * (self.size + 1), 2))
        ext_bound[0 : self.size + 1, 0] = -1
        ext_bound[0 : self.size + 1, 1] = np.arange(-1, self.size)
        ext_bound[self.size + 1 : 2 * (self.size + 1), 0] = np.arange(self.size + 1)
        ext_bound[self.size + 1 : 2 * (self.size + 1), 1] = -1
        ext_bound[2 * (self.size + 1) : 3 * (self.size + 1), 0] = np.arange(-1, self.size)
        ext_bound[2 * (self.size + 1) : 3 * (self.size + 1), 1] = self.size
        ext_bound[3 * (self.size + 1) : 4 * (self.size + 1), 0] = self.size
        ext_bound[3 * (self.size + 1) : 4 * (self.size + 1), 1] = np.arange(self.size + 1)
        self.I = np.maximum(4 - self.distance, 0)
        bd_dist = cdist(self.coordinates, ext_bound, 'minkowski', 1)
        self.I_boundary = np.sum(np.maximum(4 - bd_dist, 0), 1)

    def get_influence(self, W_white, W_black):
        influence_white = np.sum(self.I[:, W_white], 1) - np.sum(self.I[:, W_black], 1) - self.I_boundary
        influence_black = np.sum(self.I[:, W_white], 1) - np.sum(self.I[:, W_black], 1) + self.I_boundary
        return (influence_white, influence_black)



# def empty(d):
#     coordinates = np.zeros((d*d, 2))
#     coordinates[:, 0] = np.repeat(np.arange(d), d)
#     coordinates[:, 1] = np.tile(np.arange(d), d)
#     distance = squareform(pdist(coordinates, 'minkowski', 1))


# def adversarial(d):
#     coordinates = np.zeros((d*d, 2))
#     coordinates[:, 0] = np.repeat(np.arange(d), d)
#     coordinates[:, 1] = np.tile(np.arange(d), d)
#     ext_bound = np.zeros((4*(d+1), 2))
#     ext_bound[0:d+1, 0] = -1
#     ext_bound[0:d+1, 1] = np.arange(-1, d)
#     ext_bound[d+1:2*(d+1), 0] = np.arange(d+1)
#     ext_bound[d+1:2*(d+1), 1] = -1
#     ext_bound[2*(d+1):3*(d+1), 0] = np.arange(-1, d)
#     ext_bound[2*(d+1):3*(d+1), 1] = d 
#     ext_bound[3*(d+1):4*(d+1), 0] = d
#     ext_bound[3*(d+1):4*(d+1), 1] = np.arange(d+1)
#     distance = squareform(pdist(coordinates, 'minkowski', 1))
#     I = np.maximum(4 - distance, 0)
#     bd_dist = cdist(coordinates, ext_bound, 'minkowski', 1)
#     I_boundary = np.sum(np.maximum(4 - bd_dist, 0), 1)
#     return I, I_boundary


def influence(I, I_boundary, W_white, W_black):
    influence_white = np.sum(I[:, W_white], 1) - np.sum(I[:, W_black], 1) - I_boundary
    influence_black = np.sum(I[:, W_white], 1) - np.sum(I[:, W_black], 1) + I_boundary
    return (influence_white, influence_black)
