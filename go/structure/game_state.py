import gym

BLACK = 1
WHITE = 2

env = gym.make('Go9x9-v0')
env.reset()

class GameState(object):
    """A state of the game board, needed in Monte Carlo Tree Search.
       By convention, the players are numbered 1 (Black, X) and 2 (White, O).
    """
    def __init__(self):
        self.py_pachi_board = env.state.board.clone()
        self.player_just_moved = WHITE # At the root pretend the player just moved is player 2 - player 1 has the first move
        self.nbmoves = 0
        # official_score Ref: https://github.com/openai/pachi-py/blob/9cb949b9d1f2126c4f624f23ee7b982af59f5402/pachi_py/pachi/board.c#L1556
        # self.accumulated_score = [0.0, 0.0] # later for immediate reward
    
    def clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.py_pachi_board = self.py_pachi_board.clone()
        st.player_just_moved = self.player_just_moved
        st.nbmoves = self.nbmoves
        # st.accumulated_score = [self.accumulated_score[0], self.accumulated_score[1]]
        return st

    def get_moves(self):
        """ Get all possible moves from this state, including not playing any stone (-1).
        """
        return self.py_pachi_board.get_legal_coords(3 - self.player_just_moved, filter_suicides=True)
    
    def do_move(self, coord):
        self.nbmoves += 1
        self.player_just_moved = 3 - self.player_just_moved
        self.py_pachi_board.play_inplace(coord, self.player_just_moved)
        
    def get_result(self, player_current):
        """ Get the game result from the viewpoint of player_current. 
        """
        official_score = self.py_pachi_board.official_score
        if ((official_score > 0 and player_current == WHITE) or (official_score < 0 and player_current == BLACK)):
            return 1
        elif (official_score == 0):
            return 0
        else:
            return -1
