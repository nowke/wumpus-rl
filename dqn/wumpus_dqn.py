from simple_dqn_tf2 import Agent
import numpy as np
import gym_wumpus
import gym
from utils import plotLearning
import tensorflow as tf

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    env = gym.make('wumpus-v0')
    lr = 0.01
    n_games = 35000
    agent = Agent(gamma=0.95, epsilon=0.9, epsilon_dec=1e-6, lr=lr, 
                input_dims=env.observation_space.shape,
                n_actions=7, mem_size=1000000, batch_size=64,
                epsilon_end=0.01)
    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])

        e = f'episode: {i}, score {score:.2f}, average_score {avg_score:.2f}, epsilon {agent.epsilon:.2f}\n'
        with open('output.txt', 'a') as f:
            f.write(e)

    filename = 'wumpus.png'
    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)