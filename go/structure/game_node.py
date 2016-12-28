from math import sqrt, log


class GameNode(object):
    """docstring for structure"""
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parent_node = parent # "None" for the root node
        self.child_nodes = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.py_pachi_board.get_legal_coords(3 - state.player_just_moved, filter_suicides=True) # future child nodes
        self.player_just_moved = state.player_just_moved # the only part of the state that the GameNode needs later
        
    def UCT_select_child(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.child_nodes, key = lambda c: c.wins / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s
    
    def add_child(self, m, s):
        """ Remove m from untried_moves and add a new child node for this move.
            Return the added child node
        """
        n = GameNode(move = m, parent = self, state = s)
        self.untried_moves.remove(m)
        self.child_nodes.append(n)
        return n
    
    def update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result
    
    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits)
        
    def tree_to_string(self, indent):
        s = self.indent_string(indent) + str(self)
        for c in self.child_nodes:
             s += c.tree_to_string(indent+1)
        return s

    def indent_string(self, indent):
        s = "\n"
        for i in range (1, indent + 1):
            s += "| "
        return s

    def children_to_string(self):
        s = ""
        for c in self.child_nodes:
             s += str(c) + "\n"
        return s
