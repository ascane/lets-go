# Monte Carlo Tree Search + M-LUCB algorithm

import argparse
import logging
import sys

import gym
import env_runner

# In modules, use `logger = logging.getLogger(__name__)`
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stderr))

class MctsMlucbAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

def complete(results):
    return len(results['episode_lengths']) == 10

def run_mcts_mlucb(env):
    episode_count = 10
    agent = MctsMlucbAgent(env.action_space)

    for i in xrange(episode_count):
        ob = env.reset()
        reward = done = None

        while True:
            action = agent.act(ob, reward, done)
            ob, reward, done, _ = env.step(action)
            if done:
                break

def always_true(id):
    return True

def main():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-b', '--base-dir', help='Set base dir.')
    parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0, help='Set verbosity.')
    args = parser.parse_args()

    if args.verbosity == 0:
        logger.setLevel(logging.INFO)
    elif args.verbosity >= 1:
        logger.setLevel(logging.DEBUG)

    runner = env_runner.EnvRunner('mcts-mlucb-v0', run_mcts_mlucb, complete, base_dir=args.base_dir, video_callable=always_true, env_ids=['Go9x9-v0'])
    runner.run()

    return 0

if __name__ == '__main__':
    sys.exit(main())
