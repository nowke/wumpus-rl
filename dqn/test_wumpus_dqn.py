import gym_wumpus
import gym
import numpy as np
import tensorflow as tf
from pathlib import Path

from dqn import Agent
from utils import create_gif

MODEL_DIR = 'models/wumpus-v0-dqn'
MODEL_FILE = 'wumpus-v0-dqn.h5'
CHECKPOINTS_DIR = 'models/wumpus-v0-dqn/checkpoints'
TEST_IMG_DIR = 'tests/wumpus-v0-dqn'

if __name__ == '__main__':
    env = gym.make('wumpus-v0')
    env.reset()
    checkpoints = list(Path(CHECKPOINTS_DIR).glob('*.h5'))

    for checkpoint in checkpoints:
        ep_id = checkpoint.stem
        agent = Agent(gamma=0.95, epsilon=0.0, epsilon_dec=0, lr=0.01,
                      input_dims=env.observation_space.shape,
                      n_actions=7, mem_size=1000000, batch_size=64,
                      epsilon_end=0.0, fname=MODEL_FILE, model_dir=MODEL_DIR,
                      ckpt_dir=CHECKPOINTS_DIR)
        agent.load_checkpoint(ep_id)

        done = False
        score = 0
        steps_per_episode = 0
        observation = env.reset()
        images = [env.render('rgb_array')]
        while not done:
            action = agent.choose_action(observation)
            observation, reward, done, info = env.step(action)
            score += reward
            steps_per_episode += 1
            images.append(env.render('rgb_array'))

        create_gif(
            f'{TEST_IMG_DIR}/{ep_id}.gif',
            np.array(images),
            fps=1.0
        )

        print(
            f'Model \'{str(checkpoint)}\', score {score}, steps {steps_per_episode}')
