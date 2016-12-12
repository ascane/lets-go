import gym
 
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
b.play_inplace(19, 2) # coord, color
print(b)
print(b.official_score)
b.play_inplace(20, 1)
print(b)
print(b.official_score)
b.play_inplace(31, 2)
print(b)
print(b.official_score)
if b.is_terminal:
    print("yes")
else:
    print("no")
