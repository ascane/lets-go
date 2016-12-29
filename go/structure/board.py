import numpy as np
from scipy.spatial.distance import pdist, cdist, squareform
import matplotlib.pyplot as plt

BLACK = 1
WHITE = 2

class Board(object):
    """Definition of boundary choice and immediate reward, used to prune the Monte Carlo Tree Search.
    """
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
    
    def listcoo2listidx(self, list_coord):
        result = []
        while not(list_coord.empty()):
            coo = list_coord.pop()
            result.append(self.coo2idx(coo[0], coo[1]))
        return result
    
    def get_immediate_reward(self, player_just_moved, W_white, W_black, parent_W_white=[], parent_W_black=[]):
        assert player_just_moved == BLACK or player_just_moved == WHITE
        R = 0
        IW, IB = self.get_influence(W_white, W_black)
        parent_IW, parent_IB = self.get_influence(parent_W_white, parent_W_black)
        if player_just_moved == BLACK:
            R += len(parent_W_white) - len(W_white) # captures
            for idx in range(self.size * self.size):
                R += IB[idx] - parent_IB[idx]
                if  parent_IB[idx] < 0 and IB[idx] >= 0:
                    R += 1
        else:
            R += len(parent_W_black) - len(W_black) # captures
            for idx in range(self.size * self.size):
                R += IW[idx] - parent_IW[idx]
                if  parent_IW[idx] < 0 and IW[idx] >= 0:
                    R += 1
        return R
    
    def get_immediate_reward(self, player_just_moved, list_coo_white, list_coo_black, list_coo_parent_white=[], list_coo_parent_black=[]):
        W_white = self.listcoo2listidx(list_coo_white)
        W_black = self.listcoo2listidx(list_coo_black)
        parent_W_white = self.listcoo2listidx(list_coo_parent_white)
        parent_W_black = self.listcoo2listidx(list_coo_parent_black)
        return self.get_immediate_reward(player_just_moved, W_white, W_black, parent_W_white, parent_W_black)
    