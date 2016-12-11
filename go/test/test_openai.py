import gym
 
env = gym.make('Go9x9-v0')
env.reset()
env.render()

    
# for i_episode in range(1):
#     observation = env.reset()
#     for t in range(100):
#         env.render()
#         print(observation)
#         print(env.action_space)
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break

b = env.state.board.clone()
b.play_inplace(19, 2)
print(b)
b.play_inplace(20, 1)
print(b)
b.play_inplace(31, 2)
print(b)
# b.play_inplace(coord, color)
# b.official_score()
