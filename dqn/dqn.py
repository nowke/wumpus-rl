import numpy as np
import tensorflow as tf
from tensorflow import keras

from utils import ReplayMemory


class Agent():
    def __init__(self, learning_rate, gamma, state_shape, actions, batch_size,
                 epsilon_initial=0.9,
                 epsilon_decay=1e-3,
                 epsilon_final=0.01,
                 replay_buffer_capacity=1000000,
                 model_name='dqn_model.h5',
                 model_dir='models/dqn_model',
                 ckpt_dir='models/dqn_model/checkpoints',
                 log_dir='logs'):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.actions = actions
        self.batch_size = batch_size
        self.epsilon = epsilon_initial
        self.epsilon_decay = epsilon_decay
        self.epsilon_final = epsilon_final
        self.buffer = ReplayMemory(replay_buffer_capacity, state_shape)
        self.q_network = self._get_model()

        self.model_file = f'{model_dir}/{model_name}'
        self.checkpoint_dir = ckpt_dir

    def select_action(self, state):
        """Select action according to epsilon greedy policy"""
        if np.random.random() < self.epsilon:
            return np.random.choice(range(self.actions))
        else:
            return np.argmax(self.q_network.predict(np.array([state])))

    def train(self):
        """Optimize the model for the current batch"""
        if self.buffer.current_size >= self.batch_size:
            states, actions, rewards, next_states, dones = self.buffer.sample(
                self.batch_size)

            q_target = np.copy(self.q_network.predict(states))   # Q*(s,a)
            q_values_next = self.q_network.predict(next_states)  # Q*(s',a')

            batch = np.arange(self.batch_size, dtype=np.int32)

            # Bellman equation update
            q_target[batch, actions] = rewards + (self.gamma *
                                                  np.max(q_values_next, axis=1) * dones)

            # Train using fixed q-targets
            self.q_network.train_on_batch(states, q_target)

            # Update epsilon
            if self.epsilon > self.epsilon_final:
                self.epsilon -= self.epsilon_decay
            else:
                self.epsilon = self.epsilon_final

    def store_experience(self, state, action, reward, next_state, done):
        """Store tuple <s, a, r, s', done> to the buffer"""
        self.buffer.store(state, action, reward, next_state, done)

    def save_model(self):
        self.q_network.save(self.model_file)

    def load_model(self):
        self.q_network = keras.models.load_model(self.model_file)

    def save_checkpoint(self, id):
        self.q_network.save(f'{self.checkpoint_dir}/{id}.h5')

    def load_checkpoint(self, id):
        self.q_network = keras.models.load_model(
            f'{self.checkpoint_dir}/{id}.h5')

    def _get_model(self):
        # 2 hidden layers, 1 FC layer
        model = keras.Sequential([
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(self.actions, activation=None)
        ])

        # Use Adam optimizer
        optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        model.compile(optimizer=optimizer, loss='mean_squared_error')

        return model
