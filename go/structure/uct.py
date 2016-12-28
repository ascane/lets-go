import numpy as np
import game_state, game_node
import random

def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = game_node.GameNode(state = rootstate)

    for i in range(itermax):
        node = rootnode
        state = game_state.GameState()
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
            
        # Rollout - this can often be made orders of magnitude quicker using a state.get_random_move() function
        while not(state.py_pachi_board.is_terminal) and state.nbmoves < 4096 and len(state.get_moves()) > 1: # while state is non-terminal
            state.do_move(random.choice(state.get_moves()))
        
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.update(state.get_result(node.player_just_moved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parent_node

    # Output some information about the tree - can be omitted
    if (verbose): 
        print rootnode.tree_to_string(0)
    else: 
        print rootnode.children_to_string()

    return sorted(rootnode.child_nodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
                
def UCT_play_game(n_iter=1000, verbo=False):
    """ Play a sample game between two UCT players where each player gets a different number 
        of UCT iterations (= simulations = tree nodes).
    """
    state = game_state.GameState()
    while (len(state.get_moves()) > 1):
        print str(state)
        if state.player_just_moved == 1:
            m = UCT(rootstate=state, itermax = n_iter, verbose=verbo) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate=state, itermax=n_iter, verbose=verbo)
        print "Best Move: " + str(m) + "\n"
        state.do_move(m)
        if verbo:
            print(state.py_pachi_board)
    if state.get_result(state.player_just_moved) > 0:
        print "Player " + str(state.player_just_moved) + " wins!"
    elif state.get_result(state.player_just_moved) < 0:
        print "Player " + str(3 - state.player_just_moved) + " wins!"
    else: print "Nobody wins!"
    
if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    UCT_play_game(verbo=True)