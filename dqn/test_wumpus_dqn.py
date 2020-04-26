import gym_wumpus
import gym
import numpy as np
import tensorflow as tf
from datetime import datetime

from simple_dqn_tf2 import Agent
from utils import create_gif

MODEL_DIR = 'models/wumpus-v0-dqn'
# MODEL_FILE = 'wumpus-v0-dqn.h5'
MODEL_FILE = 'checkpoints/episode-34000.h5'
CHECKPOINTS_DIR = 'models/wumpus-v0-dqn/checkpoints'
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_DIR = f'logs/{RUN_ID}'
TEST_IMG_DIR = 'tests/wumpus-v0-dqn'

if __name__ == '__main__':
    env = gym.make('wumpus-v0')
    env.reset()
    lr = 0.01
    n_games = 1
    agent = Agent(gamma=0.95, epsilon=0.0, epsilon_dec=0, lr=lr,
                  input_dims=env.observation_space.shape,
                  n_actions=7, mem_size=1000000, batch_size=64,
                  epsilon_end=0.0, fname=MODEL_FILE, model_dir=MODEL_DIR,
                  ckpt_dir=CHECKPOINTS_DIR, log_dir=LOG_DIR)

    agent.load_model()

    for i in range(1, n_games + 1):
        done = False
        score = 0
        observation = env.reset()
        steps_per_episode = 0
        images = []
        images.append(env.render('rgb_array'))
        while not done:
            action = agent.choose_action(observation)
            observation, reward, done, info = env.step(action)
            score += reward
            steps_per_episode += 1
            images.append(env.render('rgb_array'))

        create_gif(
            f'{TEST_IMG_DIR}/episode_{i}.gif',
            np.array(images),
            fps=1.0
        )

        print(f'Episode {i}, score {score}, steps {steps_per_episode}')
