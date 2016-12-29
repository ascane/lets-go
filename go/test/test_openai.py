import gym

BLACK = 1
WHITE = 2
 
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

 
black_stone_array = b.get_stones(BLACK)
white_stone_array = b.get_stones(WHITE)
print(white_stone_array)

print(b.black_stones)
print(b.white_stones)

print(b.size)

print(b.get_legal_coords(BLACK, filter_suicides=True))
print(b.coord_to_ij(20))
print(b.ij_to_coord(8, 8))

l = [5, 1, 2, 3]
print(sorted(l)[-1])


# The implemented methods of PyPachiBoard: https://github.com/openai/pachi-py/blob/master/pachi_py/cypachi.pyx#L159
# black (X) = 1
# white (O) = 2
