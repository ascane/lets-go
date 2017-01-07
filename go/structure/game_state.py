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
    def __init__(self, prune=False, zero_sum=False, epsilon=0., minmax=False):
        self.py_pachi_board = env.state.board.clone()
        self.player_just_moved = WHITE # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.nbmoves = 0
        # official_score Ref: https://github.com/openai/pachi-py/blob/9cb949b9d1f2126c4f624f23ee7b982af59f5402/pachi_py/pachi/board.c#L1556
        self.prune = prune
        # self.accumulated_reward = [0.0, 0.0] # B/W for immediate reward 
        self.zero_sum = zero_sum
        self.epsilon = epsilon
        self.minmax = minmax
        self.IW = None
        self.IB = None
    
    def clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.py_pachi_board = self.py_pachi_board.clone()
        st.player_just_moved = self.player_just_moved
        st.nbmoves = self.nbmoves
        st.prune = self.prune
        # st.accumulated_reward = [self.accumulated_reward[0], self.accumulated_reward[1]]
        st.zero_sum = self.zero_sum
        st.epsilon = self.epsilon
        st.minmax = self.minmax
        st.IW = self.IW
        st.IB = self.IB
        return st
    
    def get_immediate_reward_aux(self, coord):
        if coord == -1:
            return 0, self.IW, self.IB
        
        white_stones = self.py_pachi_board.white_stones
        black_stones = self.py_pachi_board.black_stones
        next_state = self.clone()
        next_state.player_just_moved = 3 - self.player_just_moved
        next_state.py_pachi_board.play_inplace(coord, next_state.player_just_moved)
        next_white_stones = next_state.py_pachi_board.white_stones
        next_black_stones = next_state.py_pachi_board.black_stones
        return b.get_immediate_reward(next_state.player_just_moved, next_white_stones, next_black_stones, white_stones, black_stones, self.coord_to_idx(coord), self.IW, self.IB)
    
    def get_immediate_reward(self, coord):
        if coord == -1:
            reward = 0
        else:
            reward, _, _ = self.get_immediate_reward_aux(coord)
        if not(self.minmax):
            return reward
        
        next_state = self.clone()
        next_state.do_move(coord)
        next_moves = next_state.get_all_moves()
        next_reward_max, _, _ = next_state.get_immediate_reward_aux(next_moves[0])
        for m in next_moves:
            next_reward, _, _ = next_state.get_immediate_reward_aux(m)
            if next_reward > next_reward_max:
                next_reward_max = next_reward
        return reward - next_reward_max
    
    def coord_to_idx(self, coord):
        i, j = self.py_pachi_board.coord_to_ij(coord)
        return b.coo2idx(i, j)

    def get_all_moves(self):
        """Get all possible moves from this state, including not playing any stone (-1).
        """
        return self.py_pachi_board.get_legal_coords(3 - self.player_just_moved, filter_suicides=True)

    def get_moves(self):
        """ If not prune, get all possible moves from this state, including not playing any stone (-1),
            else get epsilon-optimal moves.
        """
        all_possible_moves = self.get_all_moves()
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
                if all_rewards[i] >= (1 - self.epsilon) * best_reward - 1e-5:
                    result.append(all_possible_moves[i])
            return result
    
    def do_move(self, coord, update=True):
#         if self.prune and update:
#             r = self.get_immediate_reward(coord)
#             self.accumulated_reward[self.player_just_moved - 1] += r
#             if self.zero_sum:
#                 self.accumulated_reward[(3 - self.player_just_moved) - 1] -= r

        if self.prune and update:
            _, self.IW, self.IB = self.get_immediate_reward_aux(coord)
        self.nbmoves += 1
        self.player_just_moved = 3 - self.player_just_moved
        self.py_pachi_board.play_inplace(coord, self.player_just_moved)
        
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
