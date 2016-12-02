import const

CONST = const.CONST

class State(object):
    def __init__(self, size):
        self.size = size
        self.whiteSet = set()
        self.blackSet = set()
        self.nextTurn = CONST.BLACK()
        self.diffWB = 0
        
    def isValid(self):
        for s in self.whiteSet:
            if self.blackSet.__contains__(s):
                return False
            if s >= self.size * self.size or s < 0:
                return False
        for s in self.blackSet:
            if s >= self.size * self.size or s < 0:
                return False
        return True
            
    def play(self, pos):
        if pos >= self.size * self.size or pos < 0:
            raise ValueError('Position %d out of bound', pos)
        if self.whiteSet.__contains__(pos):
            raise ValueError('This position is already occupied by a white stone.')
        if self.blackSet.__contains__(pos):
            raise ValueError('This position is already occupied by a black stone.')
        if self.nextTurn == CONST.BLACK():
            self.blackSet.add(pos)
            # TODO: Remove surrounded white stones if any. DFS or BFS.
            self.nextTurn = CONST.WHITE()
        else:
            self.whiteSet.add(pos)
            # TODO: Remove surrounded black stones if any. DFS or BFS.
            self.nextTurn = CONST.BLACK()
            