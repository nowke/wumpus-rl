import gym
from gym import spaces
import numpy as np
from collections import OrderedDict

from gym_wumpus.utils import wumpus_to_np_array
from .wumpus.wumpus import WumpusWorldScenario, Explorer, Wumpus, Pit, Gold



ACTION_TURN_RIGHT = 'TurnRight'
ACITON_TURN_LEFT = 'TurnLeft'
ACTION_FORWARD = 'Forward'
ACTION_GRAB = 'Grab'
ACTION_CLIMB = 'Climb'
ACTION_SHOOT = 'Shoot'
ACTION_WAIT = 'Wait'


class WumpusWorld(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self):
        self._reset()
        self.actions = [
            ACTION_TURN_RIGHT, ACITON_TURN_LEFT, ACTION_FORWARD,
            ACTION_GRAB, ACTION_CLIMB, ACTION_SHOOT, ACTION_WAIT
        ]
        self.action_space = spaces.Box(
            low=0,
            high=len(self.actions) - 1,
            shape=(1,),
            dtype=np.int32
        )

        """
        [
          x_location (1-4), y_location (1-4), heading (0-N, 1-W, 2-S, 3-E),
          stench, breeze, glitter, bump, scream (0, 1)
        ]
        """
        self.observation_space = spaces.Box(
            low=0,
            high=5,
            shape=(8,),
            dtype=np.int32
        )

    def step(self, action):
        # Check for invalid actions
        action = int(action)
        if action >= len(self.actions) or action < 0:
            action = 6  # Wait

        action = self.actions[action]

        # Execute the action in the environment
        self.env.execute_action(self.agent, action)
        self.env.time_step += 1
        self.env.exogenous_change()

        # Get the current reward
        # `WumpusEnvrionment` gives total score, so we keep track of the
        # previous score to find the difference.
        reward = self.agent.performance_measure - self.previous_score

        ########## SPECIAL CASE reward ##########
        # TODO: Refactor hardcoded locations

        # Case 1 -> Agent has reached `Gold` location
        #   reward = +500
        if self._location == (2, 3) and not self.gold_reward_given:
            if action != ACTION_GRAB:
                reward = 500
                self.gold_reward_given = True

        # Case 2 -> Agent has `Grabbed` the gold
        #   reward = +500
        if self._location == (2, 3) and not self.gold_grab_reward_given:
            if action == ACTION_GRAB:
                self.has_gold = True
                self.gold_grab_reward_given = True
                reward = 500

        # Case 3 -> Agent tries to `Climb` without gold
        #    reward = -1000
        if self._location == (1, 1):
            if action == ACTION_CLIMB:  # Climb
                reward = -1000  # Don't climb without gold :-)

        self.previous_score = self.agent.performance_measure

        # The game is over with 4 conditions
        #   (1) Agent gets killed by wumpus
        #   (2) Agent falls into a pit
        #   (3) Time step is 50  (to limit infinite loops)
        #   (4) Agent has grabbed the gold
        done = self.env.is_done() or self.env.time_step == 50 or self.has_gold

        observation = self._state
        return observation, reward, done, {}

    def reset(self):
        self._reset()
        return self._state

    def render(self, mode='human', close=False):
        env_str = self.env.to_string()
        if mode == 'human':
            print(env_str)
        elif mode == 'rgb_array':
            return wumpus_to_np_array(env_str)

    def _reset(self):
        # TODO: Generalize this to take parameters from outside.
        self.scenario = WumpusWorldScenario(
            agent=Explorer(heading='north', verbose=False),
            objects=[(Wumpus(), (1, 3)),
                     (Pit(), (3, 3)),
                     (Pit(), (3, 1)),
                     (Gold(), (2, 3))],
            width=4,
            height=4,
            entrance=(1, 1),
            trace=False
        )
        self.previous_score = 0
        self.agent = self.scenario.agent
        self.env = self.scenario.env
        self.has_gold = False
        self.gold_reward_given = False
        self.gold_grab_reward_given = False
        self.initial_reward_given = False
        self.wumpus_alive = True

    @property
    def _state(self):
        location = self._location
        percept = self.env.percept(self.agent)
        heading = self.agent.heading

        if percept[4]:
            self.wumpus_alive = False

        return np.array([
            np.uint32(location[0]),
            np.uint32(location[1]),
            np.uint32(heading),
            np.uint32(percept[0]),
            np.uint32(percept[1]),
            np.uint32(percept[2]),
            np.uint32(percept[3]),
            np.uint32(percept[4])]
        )

    @property
    def _location(self):
        return self.agent.location

    @property
    def _percept(self):
        return self.env.percept(self.agent)
