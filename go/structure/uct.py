import numpy as np
import game_state, game_node
import random

def UCT(rootstate, itermax,  verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
    """
    rootnode = game_node.GameNode(state=rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.clone()
        
        # Select
        while node.untried_moves == [] and node.child_nodes != []: # node is fully expanded and non-terminal
            node = node.UCT_select_child()
            state.do_move(node.move)
            
        # Expand
        if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untried_moves) 
            state.do_move(m)
            node = node.add_child(m, state) # add child and descend tree
            
        # Rollout
        # OpenAI Go board has its maximum limit of moves as 4096
        # state.get_moves() always contains -1
        while not(state.py_pachi_board.is_terminal) and state.nbmoves < 4096 and len(state.get_all_moves()) > 1: # while state is non-terminal
            state.do_move(random.choice(state.get_all_moves()), update=False)
        
        # Backpropagate
        while node is not None: # backpropagate from the expanded node and work back to the root node
            node.update(state.get_result(node.player_just_moved)) # state is terminal. Update node with result from POV of node.player_just_moved
            node = node.parent_node

    # Output some information about the tree - can be omitted
    if verbose: 
        print rootnode.tree_to_string(0)
#     else: 
#         print rootnode.children_to_string()

    return sorted(rootnode.child_nodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
                
def UCT_play_game(n_iter=1000, prune1=False, zero_sum1=False, epsilon1=0., prune2=False, zero_sum2=False, epsilon2=0., verbose=False):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    _verbose = verbose
    state1 = game_state.GameState(prune1, zero_sum1, epsilon1)
    state2 = game_state.GameState(prune2, zero_sum2, epsilon2)
    while ((state1.player_just_moved == 2 and len(state1.get_all_moves()) > 1 and not(state1.py_pachi_board.is_terminal)) or (state2.player_just_moved == 1 and len(state2.get_all_moves()) > 1 and not(state2.py_pachi_board.is_terminal))):
        if state1.player_just_moved == 1:
            m = UCT(rootstate=state2, itermax=n_iter, verbose=_verbose)
        else:
            m = UCT(rootstate=state1, itermax=n_iter, verbose=_verbose)
        print "Best Move: " + str(m) + "\n"
        state1.do_move(m)
        state2.do_move(m)
        if _verbose:
            print(state1.py_pachi_board)
    if state1.get_result(state1.player_just_moved) > 0:
        print "Player " + str(state1.player_just_moved) + " wins!"
    elif state1.get_result(state1.player_just_moved) < 0:
        print "Player " + str(3 - state1.player_just_moved) + " wins!"
    else: print "Nobody wins!"
    
if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
    """
    UCT_play_game(n_iter=100, prune1=True, zero_sum1=True, epsilon1=0., prune2=False, zero_sum2=False, epsilon2=0.,verbose=True)
    