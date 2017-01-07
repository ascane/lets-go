import game_state
import uct
import random
from abc import abstractmethod

class Strategy(object):
    """An abstract class for a game strategy.
    """
    @abstractmethod
    def get_state(self):
        pass
    
    @abstractmethod
    def next_move(self):
        pass
        
class UctStrategy(Strategy):
    """A game strategy based on UCT.
    """
    def __init__(self, n_iter=1000, prune=False, zero_sum=False, epsilon=0., minmax=False, immediate=False, verbose=False):
        self.n_iter = n_iter
        self.prune = prune
        self.zero_sum = zero_sum
        self.epsilon = epsilon
        self.minmax = minmax
        self.verbose = verbose
        self.immediate = immediate
        self.state = None
        
    def get_state(self):
        if not(self.state):
            self.state = game_state.GameState(self.prune, self.zero_sum, self.epsilon, self.minmax, self.immediate)
        return self.state
    
    def next_move(self):
        return uct.UCT(self.state, self.n_iter, self.verbose)
    
    def reset(self):
        self.state = None
    
class RandomStrategy(Strategy):
    """A random game strategy, i.e. takes a random action among all possibilities at each move.
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.state = None
        
    def get_state(self):
        if not(self.state):
            self.state = game_state.GameState()
        return self.state
    
    def next_move(self):
        return random.choice(self.get_state().get_all_moves())
    
    def reset(self):
        self.state = None
    
def play_game(strategy1, strategy2):
    """Play a simple game between two players. The first player (black, X) plays with strategy1
       and the second (whtie, O) with strategy2.
    """
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
        return state1.player_just_moved
    elif state1.get_result(state1.player_just_moved) < 0:
        print "Player " + str(3 - state1.player_just_moved) + " wins!"
        return 3 - state1.player_just_moved
    else:
        print "Nobody wins!"
        return 0
    
    
if __name__ == "__main__":
    strategy0 = UctStrategy()
    strategy1 = UctStrategy(n_iter=10, prune=True, zero_sum=False, epsilon=0., minmax=True)
    strategy2 = RandomStrategy(verbose=True)
    strategy3 = UctStrategy(n_iter=1000, prune=False, zero_sum=False, epsilon=0., minmax=True, immediate=True)
    play_game(strategy0, strategy2)
    
#     wins = [0, 0]
#     strategy1 = UctStrategy()
#     strategy2 = RandomStrategy(verbose=True)
#     for i in range(100):
#         strategy1.reset()
#         strategy2.reset()
#         result = play_game(strategy1, strategy2)
#         if result != 0:
#             wins[result - 1] += 1
#     print "Strategy1: " + str(wins[0]) + " wins. Strategy2: " + str(wins[1]) + " wins."
    
    