import sys
sys.path.append("..")

import gym
import random
from structure import const, game_state

diff = 0

for i in range(100):
    state1 = game_state.GameState(immediate=True)
    state2 = game_state.GameState()
    while ((state1.player_just_moved == 2 and len(state1.get_all_moves()) > 1 and not(state1.py_pachi_board.is_terminal)) or (state2.player_just_moved == 1 and len(state2.get_all_moves()) > 1 and not(state2.py_pachi_board.is_terminal))):
        if state1.player_just_moved == 1:
            m = random.choice(state2.get_all_moves())
        else:
            m = random.choice(state1.get_all_moves())
        state1.do_move(m)
        state2.do_move(m)
        print(state1.py_pachi_board)
     
    delayed = state1.get_result(state1.player_just_moved)   
    state1.immediate = False
    immediate = state1.get_result(state1.player_just_moved)
    if delayed != immediate:
        diff += 1

print diff