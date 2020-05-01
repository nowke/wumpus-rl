import gym_wumpus
import gym
import numpy as np
import sys
import tensorflow as tf
from pathlib import Path

from dqn import Agent
from utils import create_gif


def main(env_name=None):
    ENV_NAME = 'wumpus-v0'
    
    if env_name: ENV_NAME = env_name

    MODEL_DIR = f'models/{ENV_NAME}-dqn'
    MODEL_FILE = f'{ENV_NAME}-dqn.h5'
    CHECKPOINTS_DIR = f'models/{ENV_NAME}-dqn/checkpoints'
    TEST_IMG_DIR = f'tests/{ENV_NAME}-dqn'

    env = gym.make(ENV_NAME)
    env.reset()

    agent = Agent(learning_rate=0.01, gamma=0.95,
                    state_shape=env.observation_space.shape, actions=7,
                    batch_size=64,
                    epsilon_initial=0.0, epsilon_decay=0, epsilon_final=0.0,
                    replay_buffer_capacity=1000000,
                    model_name=MODEL_FILE, model_dir=MODEL_DIR,
                    ckpt_dir=CHECKPOINTS_DIR)
    agent.load_model()

    done = False
    score = 0
    steps_per_episode = 0
    state = env.reset()
    images = [env.render('rgb_array')]
    while not done:
        # Choose action according to policy, and execute
        action = agent.select_action(state)
        state, reward, done, _ = env.step(action)

        score += reward
        steps_per_episode += 1
        images.append(env.render('rgb_array'))

    # Generate GIF for the execution
    create_gif(
        f'{ENV_NAME}.gif',
        np.array(images),
        fps=1.0
    )

    print(
        f'Model \'{str(ENV_NAME)}\', score {score}, steps {steps_per_episode}')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        env_name = sys.argv[2]
    main(env_name)
