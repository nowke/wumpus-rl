from datetime import datetime
import numpy as np
import gym_wumpus
import gym
import tensorflow as tf

from dqn import Agent
from utils import write_summaries

ENV_NAME = 'wumpus-v0'

EPISODES = 35000
SAVE_INTERVAL = 10
CHECKPOINT_INTERVAL = 20
MODEL_DIR = f'models/{ENV_NAME}-dqn'
MODEL_FILE = f'{ENV_NAME}-dqn.h5'
CHECKPOINTS_DIR = f'models/{ENV_NAME}-dqn/checkpoints'
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_DIR = f'logs/{RUN_ID}'


def main():
    # Initialize environment, agent
    env = gym.make(ENV_NAME)
    summary_writer = tf.summary.create_file_writer(LOG_DIR)
    agent = Agent(learning_rate=0.01, gamma=0.95,
                  state_shape=env.observation_space.shape, actions=7,
                  batch_size=64,
                  epsilon_initial=0.9, epsilon_decay=1e-6, epsilon_final=0.01,
                  replay_buffer_capacity=1000000,
                  model_name=MODEL_FILE, model_dir=MODEL_DIR,
                  ckpt_dir=CHECKPOINTS_DIR, log_dir=LOG_DIR)

    scores = []
    for i in range(1, EPISODES + 1):
        done = False
        score = 0
        state = env.reset()
        steps_per_episode = 0

        # Play one episode
        while not done:
            # Choose action (epsilon greedy), and execute
            action = agent.select_action(state)
            next_state, reward, done, _ = env.step(action)
            score += reward

            # Store in experience replay buffer
            agent.store_experience(state, action,
                                   reward, next_state, done)
            state = next_state
            agent.train()
            steps_per_episode += 1
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        min_score = np.min(scores[-100:])
        max_score = np.max(scores[-100:])

        print(
            f'Episode: {i}, Score {score:.2f}, Avg_score {avg_score:.2f}, Epsilon {agent.epsilon:.2f}')

        # Summaries for Tensorboard
        write_summaries(summary_writer, {
            'epsilon': agent.epsilon,
            'reward.episode': score,
            'reward.avg': avg_score,
            'reward.min': min_score,
            'reward.max': max_score,
            'steps.count': steps_per_episode
        }, i, ENV_NAME)

        # Save the model
        if i % SAVE_INTERVAL == 0:
            print(f'Saving model to \'{MODEL_FILE}\' [Overwriting]')
            agent.save_model()

        # Save checkpoint
        if i % CHECKPOINT_INTERVAL == 0:
            print(f'Adding checkpoint: \'{CHECKPOINTS_DIR}/episode-{i}.h5\'')
            agent.save_checkpoint(f'episode-{i}')


if __name__ == '__main__':
    main()
