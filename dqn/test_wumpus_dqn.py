import gym_wumpus
import gym
import numpy as np
import tensorflow as tf
from pathlib import Path

from dqn import Agent
from utils import create_gif

ENV_NAME = 'wumpus-v0'
MODEL_DIR = f'models/{ENV_NAME}-dqn'
MODEL_FILE = f'{ENV_NAME}-dqn.h5'
CHECKPOINTS_DIR = f'models/{ENV_NAME}-dqn/checkpoints'
TEST_IMG_DIR = f'tests/{ENV_NAME}-dqn'

if __name__ == '__main__':
    env = gym.make(ENV_NAME)
    env.reset()
    checkpoints = list(Path(CHECKPOINTS_DIR).glob('*.h5'))

    for checkpoint in checkpoints:
        ep_id = checkpoint.stem
        agent = Agent(learning_rate=0.01, gamma=0.95,
                      state_shape=env.observation_space.shape, actions=7,
                      batch_size=64,
                      epsilon_initial=0.0, epsilon_decay=0, epsilon_final=0.0,
                      replay_buffer_capacity=1000000,
                      model_name=MODEL_FILE, model_dir=MODEL_DIR,
                      ckpt_dir=CHECKPOINTS_DIR)
        agent.load_checkpoint(ep_id)

        done = False
        score = 0
        steps_per_episode = 0
        state = env.reset()
        images = [env.render('rgb_array')]
        while not done:
            action = agent.select_action(state)
            state, reward, done, _ = env.step(action)
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
