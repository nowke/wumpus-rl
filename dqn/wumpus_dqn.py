from simple_dqn_tf2 import Agent
import numpy as np
import gym_wumpus
import gym
from utils import plotLearning, write_summaries
import tensorflow as tf

SAVE_INTERVAL = 10
MODEL_FILE = 'models/wumpus-v0-dqn.h5'
LOG_DIR = 'logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(
    log_dir=LOG_DIR, histogram_freq=1)


if __name__ == '__main__':
    env = gym.make('wumpus-v0')
    lr = 0.01
    n_games = 35000
    summary_writer = tf.summary.create_file_writer(LOG_DIR)
    agent = Agent(gamma=0.95, epsilon=0.9, epsilon_dec=1e-6, lr=lr,
                  input_dims=env.observation_space.shape,
                  n_actions=7, mem_size=1000000, batch_size=64,
                  epsilon_end=0.01, fname=MODEL_FILE, log_dir=LOG_DIR)
    scores = []
    eps_history = []

    for i in range(1, n_games + 1):
        done = False
        score = 0
        observation = env.reset()
        steps_per_episode = 0
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action,
                                   reward, observation_, done)
            observation = observation_
            agent.learn()
            steps_per_episode += 1
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        min_score = np.min(scores[-100:])
        max_score = np.max(scores[-100:])

        e = f'episode: {i}, score {score:.2f}, average_score {avg_score:.2f}, epsilon {agent.epsilon:.2f}\n'
        with open('output.txt', 'a') as f:
            f.write(e)

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
            print(f'Saving model to {MODEL_FILE} [Overwriting]')
            agent.save_model()

    filename = 'wumpus.png'
    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
