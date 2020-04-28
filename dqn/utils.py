from moviepy.editor import ImageSequenceClip
import numpy as np
import os
import gym
import tensorflow as tf


class ReplayMemory():
    def __init__(self, capacity, observation_shape):
        """
        Cyclic buffer with fixed `capacity` holding the transition
        tupple <s, a, r, s', done>. Use this for sampling of specified
        batch size during "Experience Replay"
        """
        self.capacity = capacity
        self.dim = observation_shape
        self.current_size = 0

        self.states = np.zeros(
            shape=(capacity, *observation_shape),
            dtype=np.float32
        )
        self.actions = np.zeros(shape=capacity, dtype=np.int32)
        self.rewards = np.zeros(shape=capacity, dtype=np.float32)
        self.next_states = np.zeros(
            shape=(capacity, *observation_shape),
            dtype=np.float32
        )
        self.dones = np.zeros(shape=capacity, dtype=np.int32)

    def store(self, state, action, reward, next_state, done):
        """
        Store the transition tuple <s, a, r, s', done> in the buffer
        """
        # Get the index to store, rotate the buffer
        i = self.current_size % self.capacity

        self.states[i] = state
        self.actions[i] = action
        self.rewards[i] = reward
        self.next_states[i] = next_state
        self.dones[i] = int(not done)

        self.current_size += 1

    def sample(self, size):
        """
        Sample random tuples of `size`
        """
        sample_indices = np.random.choice(
            min(self.capacity, self.current_size),
            size,
            replace=False
        )

        return (
            self.states[sample_indices],
            self.actions[sample_indices],
            self.rewards[sample_indices],
            self.next_states[sample_indices],
            self.dones[sample_indices]
        )


def write_summaries(summary_writer, values, step, env_name):
    descriptions = {
        'epsilon': 'Exploration probability',
        'reward.episode': 'Score for the episode',
        'reward.avg': 'Avg running score (Last 100 episodes)',
        'reward.min': 'Min running score (Last 100 episodes)',
        'reward.max': 'Max running score (Last 100 episodes)',
        'steps.count': 'Steps executed per episode',
    }
    with summary_writer.as_default():
        for metric, value in values.items():
            tf.summary.scalar(
                f'{env_name}/{metric}',
                value,
                step=step,
                description=descriptions[metric]
            )


def create_gif(filename, array, fps=10, scale=1.0):
    """
    Source: https://gist.github.com/nirum/d4224ad3cd0d71bfef6eba8f3d6ffd59
    """
    # ensure that the file has the .gif extension
    fname, _ = os.path.splitext(filename)
    filename = fname + '.gif'

    # copy into the color dimension if the images are black and white
    if array.ndim == 3:
        array = array[..., np.newaxis] * np.ones(3)

    # make the moviepy clip
    clip = ImageSequenceClip(list(array), fps=fps).resize(scale)
    clip.write_gif(filename, fps=fps)
    return clip
