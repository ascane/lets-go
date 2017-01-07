import sys
sys.path.append("..")

import gym
from structure import const

CONST = const.CONST

BLACK = CONST.BLACK()
WHITE = CONST.WHITE()
 
env = gym.make('Go9x9-v0')
env.reset()
env.render()

# for i_episode in range(1):
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         print(observation)
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         print(reward)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break

b = env.state.board.clone()
print(b.official_score)
b.play_inplace(19, WHITE) # coord, color
print(b)
print(b.official_score)
b.play_inplace(20, BLACK)
print(b)
print(b.official_score)
b.play_inplace(31, WHITE)
print(b)
print(b.official_score)
if b.is_terminal:
    print("yes")
else:
    print("no")
    
b.play_inplace(b.ij_to_coord(0, 1), BLACK)
b.play_inplace(b.ij_to_coord(1, 0), BLACK)
b.play_inplace(b.ij_to_coord(3, 3), BLACK)
print(b)
print(b.official_score)

 
black_stone_array = b.get_stones(BLACK)
white_stone_array = b.get_stones(WHITE)
print(white_stone_array)

print(b.black_stones)
print(b.white_stones)

W = b.white_stones
print(len(W))

print(b.size)

print(b.get_legal_coords(BLACK, filter_suicides=True))
print(b.coord_to_ij(20))
print(b.ij_to_coord(8, 8))
print(b.ij_to_coord(0, 0))

l = [5, 1, 2, 3]
print(sorted(l)[-1])

a1 = [1, 2, 3]
a2 = [4, 5, 6]
if a1[0] == 1 and a2[0] == 4:
    print "Yep"
    
i, j = b.coord_to_ij(20)
print i
print j

print not(None)


# The implemented methods of PyPachiBoard: https://github.com/openai/pachi-py/blob/master/pachi_py/cypachi.pyx#L159
# black (X) = 1
# white (O) = 2
