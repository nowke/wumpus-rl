from datetime import datetime
import numpy as np
import gym_wumpus
import gym
import tensorflow as tf

from dqn import Agent
from utils import write_summaries

SAVE_INTERVAL = 100
CHECKPOINT_INTERVAL = 2000
MODEL_DIR = 'models/wumpus-v0-dqn'
MODEL_FILE = 'wumpus-v0-dqn.h5'
CHECKPOINTS_DIR = 'models/wumpus-v0-dqn/checkpoints'
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_DIR = f'logs/{RUN_ID}'


if __name__ == '__main__':
    env = gym.make('wumpus-v0')
    episodes = 35000
    summary_writer = tf.summary.create_file_writer(LOG_DIR)
    agent = Agent(gamma=0.95, epsilon=0.9, epsilon_dec=1e-6, lr=0.01,
                  input_dims=env.observation_space.shape,
                  n_actions=7, mem_size=1000000, batch_size=64,
                  epsilon_end=0.01, fname=MODEL_FILE, model_dir=MODEL_DIR,
                  ckpt_dir=CHECKPOINTS_DIR, log_dir=LOG_DIR)

    scores = []
    for i in range(1, episodes + 1):
        done = False
        score = 0
        state = env.reset()
        steps_per_episode = 0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(state, action,
                                   reward, next_state, done)
            state = next_state
            agent.learn()
            steps_per_episode += 1
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        min_score = np.min(scores[-100:])
        max_score = np.max(scores[-100:])

        print(
            f'episode: {i}, score {score:.2f}, avg_score {avg_score:.2f}, epsilon {agent.epsilon:.2f}')

        write_summaries(summary_writer, {
            'epsilon': agent.epsilon,
            'reward.episode': score,
            'reward.avg': avg_score,
            'reward.min': min_score,
            'reward.max': max_score,
            'steps.count': steps_per_episode
        }, i)

        # Save the model
        if i % SAVE_INTERVAL == 0:
            print(f'Saving model to \'{MODEL_FILE}\' [Overwriting]')
            agent.save_model()

        # Save checkpoint
        if i % CHECKPOINT_INTERVAL == 0:
            print(f'Adding checkpoint: \'{CHECKPOINTS_DIR}/episode-{i}.h5\'')
            agent.save_checkpoint(f'episode-{i}')
