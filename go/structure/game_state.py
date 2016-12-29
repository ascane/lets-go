import gym
import board

BLACK = 1
WHITE = 2

env = gym.make('Go9x9-v0')
env.reset()

d = 9
b = board.Board(d)
b.set_boundary('empty') # This can be changed to adversarial.

class GameState(object):
    """A state of the game board, needed in Monte Carlo Tree Search.
       By convention, the players are numbered 1 (Black, X) and 2 (White, O).
    """
    def __init__(self, prune=False, zero_sum=False):
        self.py_pachi_board = env.state.board.clone()
        self.player_just_moved = WHITE # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.nbmoves = 0
        # official_score Ref: https://github.com/openai/pachi-py/blob/9cb949b9d1f2126c4f624f23ee7b982af59f5402/pachi_py/pachi/board.c#L1556
        self.prune = prune
        self.accumulated_reward = [0.0, 0.0] # B/W for immediate reward 
        self.zero_sum = zero_sum
    
    def clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.py_pachi_board = self.py_pachi_board.clone()
        st.player_just_moved = self.player_just_moved
        st.nbmoves = self.nbmoves
        st.accumulated_reward = [self.accumulated_reward[0], self.accumulated_reward[1]]
        return st
    
    def get_immediate_reward(self, coord):
        white_stones = self.py_pachi_board.white_stones
        black_stone = self.py_pachi_board.black_stones
        next_state = self.clone()
        next_state.player_just_moved = 3 - self.player_just_moved
        next_state.py_pachi_board.play_inplace(coord, self.player_just_moved)
        next_white_stones = self.py_pachi_board.white_stones
        next_black_stones = self.py_pachi_board.black_stones
        return b.get_immediate_reward(next_state.player_just_moved, next_white_stones, next_black_stones, white_stones, black_stone)

    def get_moves(self, epsilon=0.):
        """ If not prune, get all possible moves from this state, including not playing any stone (-1),
            else get epsilon-optimal moves.
        """
        all_possible_moves = self.py_pachi_board.get_legal_coords(3 - self.player_just_moved, filter_suicides=True)
        if not(self.prune):
            return all_possible_moves
        else:
            all_rewards = map(self.get_immediate_reward, all_possible_moves)
            best_i = 0
            best_reward = all_rewards[0]
            length = len(all_possible_moves)
            for i in range(length):
                if all_rewards[i] > best_reward:
                    best_i = i
                    best_reward = all_rewards[i]
            result = []
            for i in range(length):
                if all_rewards[i] >= (1 - epsilon) * best_reward - 1e-5:
                    result.append(all_possible_moves[i])
            return result
    
    def do_move(self, coord):
        self.nbmoves += 1
        self.player_just_moved = 3 - self.player_just_moved
        self.py_pachi_board.play_inplace(coord, self.player_just_moved)
        
        if self.prune:
            r = self.get_immediate_reward(coord)
            self.accumulated_reward[self.player_just_moved - 1] += r
            if self.zero_sum:
                self.accumulated_reward[(3 - self.player_just_moved) - 1] -= r
            
        
    def get_result(self, player_just_moved):
        """ Get the game result from the viewpoint of player_just_moved. 
        """
        official_score = self.py_pachi_board.official_score
        if ((official_score > 0 and player_just_moved == WHITE) or (official_score < 0 and player_just_moved == BLACK)):
            return 1
        elif (official_score == 0):
            return 0
        else:
            return -1
