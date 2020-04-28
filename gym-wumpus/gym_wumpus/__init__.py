from gym.envs.registration import register

register(
    id='wumpus-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
)

register(
    id='wumpus-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-nr-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'modify_reward': False,
    }
)

register(
    id='wumpus-nr-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'modify_reward': False,
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-nr-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'modify_reward': False,
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l4x4_1-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
    }
)

register(
    id='wumpus-l4x4_1-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l4x4_1-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l4x4_1-nr-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
        'modify_reward': False,
    }
)

register(
    id='wumpus-l4x4_1-nr-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
        'modify_reward': False,
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l4x4_1-nr-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((3, 1), (2, 2)),
        'wumpus': (1, 3),
        'gold': (2, 3),
        'modify_reward': False,
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l4x4_2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
    }
)

register(
    id='wumpus-l4x4_2-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l4x4_2-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l4x4_2-nr-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
        'modify_reward': False,
    }
)

register(
    id='wumpus-l4x4_2-nr-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
        'modify_reward': False,
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l4x4_2-nr-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (4, 4),
        'modify_reward': False,
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l5x5_1-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
    }
)

register(
    id='wumpus-l5x5_1-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l5x5_1-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
        'stochastic_action_prob': 0.9,
    }
)

register(
    id='wumpus-l5x5_1-nr-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
        'modify_reward': False,
    }
)

register(
    id='wumpus-l5x5_1-nr-noise-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
        'modify_reward': False,
        'stochastic_action_prob': 0.8,
    }
)

register(
    id='wumpus-l5x5_1-nr-noise2-v0',
    entry_point='gym_wumpus.envs:WumpusWorld',
    kwargs={
        'width': 5,
        'height': 5,
        'pits': ((4, 1), (3, 3)),
        'wumpus': (3, 4),
        'gold': (2, 5),
        'modify_reward': False,
        'stochastic_action_prob': 0.9,
    }
)
