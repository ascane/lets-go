import game_state
import uct
import random
from abc import abstractmethod

class Strategy(object):
    
    @abstractmethod
    def get_state(self):
        pass
    
    @abstractmethod
    def next_move(self):
        pass
        
class UctStrategy(Strategy):
    def __init__(self, prune=False, zero_sum=False, epsilon=0., n_iter=1000, verbose=False):
        self.prune = prune
        self.zero_sum = zero_sum
        self.epsilon = epsilon
        self.n_iter = n_iter
        self.verbose = verbose
        self.state = None
        
    def get_state(self):
        if not(self.state):
            self.state = game_state.GameState(self.prune, self.zero_sum, self.epsilon)
        return self.state
    
    def next_move(self):
        return uct.UCT(self.state, self.n_iter,  self.verbose)
    
class RandomStrategy(Strategy):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.state = None
        
    def get_state(self):
        if not(self.state):
            self.state = game_state.GameState()
        return self.state
    
    def next_move(self):
        return random.choice(self.get_state().get_all_moves()) 
    
def play_game(strategy1, strategy2):
    assert isinstance(strategy1, Strategy)
    assert isinstance(strategy2, Strategy)
    
    state1 = strategy1.get_state()
    state2 = strategy2.get_state()
    while ((state1.player_just_moved == 2 and len(state1.get_all_moves()) > 1 and not(state1.py_pachi_board.is_terminal)) or (state2.player_just_moved == 1 and len(state2.get_all_moves()) > 1 and not(state2.py_pachi_board.is_terminal))):
        if state1.player_just_moved == 1:
            m = strategy2.next_move()
        else:
            m = strategy1.next_move()
        print "Best Move: " + str(m) + "\n"
        state1.do_move(m)
        state2.do_move(m)
        if strategy1.verbose:
            print(state1.py_pachi_board)
        elif strategy2.verbose:
            print(state2.py_pachi_board)
    if state1.get_result(state1.player_just_moved) > 0:
        print "Player " + str(state1.player_just_moved) + " wins!"
    elif state1.get_result(state1.player_just_moved) < 0:
        print "Player " + str(3 - state1.player_just_moved) + " wins!"
    else: print "Nobody wins!"
    
if __name__ == "__main__":
    strategy1 = UctStrategy()
    strategy2 = RandomStrategy(verbose=True)
    play_game(strategy1, strategy2)
    
    