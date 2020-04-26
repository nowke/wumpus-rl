from moviepy.editor import ImageSequenceClip
import numpy as np
import os
import gym
import tensorflow as tf


def write_summaries(summary_writer, values, step):
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
                f'Wumpus-v0/{metric}',
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
