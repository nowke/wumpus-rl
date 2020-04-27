import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

from utils import ReplayMemory


class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size,
                 input_dims, epsilon_dec=1e-3, epsilon_end=0.01,
                 mem_size=1000000, fname='dqn_model.h5',
                 model_dir='models/dqn_model',
                 ckpt_dir='models/dqn_model/checkpoints',
                 log_dir='logs'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = f'{model_dir}/{fname}'
        self.checkpoint_dir = ckpt_dir
        self.memory = ReplayMemory(mem_size, input_dims)
        self.q_eval = self._get_model(lr, n_actions, input_dims, 256, 256)

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation])
            actions = self.q_eval.predict(state)
            action = np.argmax(actions)
        return action

    def learn(self):
        if self.memory.current_size < self.batch_size:
            return

        states, actions, rewards, states_, dones = \
            self.memory.sample(self.batch_size)

        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_target[batch_index, actions] = rewards + \
            self.gamma * np.max(q_next, axis=1)*dones

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = self.epsilon - self.eps_dec if self.epsilon > \
            self.eps_min else self.eps_min

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)

    def save_checkpoint(self, id):
        self.q_eval.save(f'{self.checkpoint_dir}/{id}.h5')

    def load_checkpoint(self, id):
        self.q_eval = load_model(f'{self.checkpoint_dir}/{id}.h5')

    def _get_model(self, lr, n_actions, input_dims, fc1_dims, fc2_dims):
        model = keras.Sequential([
            keras.layers.Dense(fc1_dims, activation='relu'),
            keras.layers.Dense(fc2_dims, activation='relu'),
            keras.layers.Dense(n_actions, activation=None)])
        model.compile(optimizer=Adam(learning_rate=lr),
                      loss='mean_squared_error')

        return model
