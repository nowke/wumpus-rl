from .wumpus.wumpus import *
import gym
from gym import spaces
import numpy as np
from collections import OrderedDict

class WumpusWorld(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        self._reset()
        self.actions = [
            'TurnRight', 'TurnLeft', 'Forward', 'Grab', 
            'Climb', 'Shoot', 'Wait'
        ]
        self.action_space = spaces.Box(low=0, high=len(self.actions)-1, shape=(1,), dtype=np.uint8)
        self.observation_space = spaces.MultiDiscrete([5, 5, 4, 2, 2, 2, 2, 2])
        
    def step(self, action):
        action = int(action)
        if action >= len(self.actions) or action < 0:
            action = 6 # Wait
        self.env.execute_action(self.agent, self.actions[action])
        self.env.time_step += 1
        self.env.exogenous_change()
        reward = self.agent.performance_measure - self.previous_score
        
        observation = self._state
        
        #### SPECIAL CASE reward #####
        if self._location == (2,3) and not self.gold_reward_given: # TODO: Refactor hardcoded location
            if action == 3:
                self.has_gold = True
                reward = 500   # Grab
            else:
                reward = 250   # Gold state
            self.gold_reward_given = True
        elif self._location == (1,1): # TODO: Refactor hardocded location
            if self.has_gold and not self.initial_reward_given:
                reward = 50
                self.initial_reward_given = True
            elif action == 4: # Climb
                reward = -1000 # Don't climb without gold :-)
        #### SPECIAL CASE reward #####
            
        self.previous_score = self.agent.performance_measure
        done = self.env.is_done()
        
        return observation, reward, done, {}
    
    def reset(self):
        self.previous_score = 0
        self._reset()
        return self._state
    
    def render(self, mode='human', close=False):
        print(self.env.to_string())
        
    def _reset(self):
        self.scenario = WumpusWorldScenario(
            agent = Explorer(heading='north', verbose=False),
            objects = [(Wumpus(),(1,3)),
                       (Pit(),(3,3)),
                       (Pit(),(3,1)),
                       (Gold(),(2,3))],
            width = 4, 
            height = 4, 
            entrance = (1,1),
            trace=False
        )
        self.agent = self.scenario.agent
        self.env = self.scenario.env
        self.has_gold = False
        self.gold_reward_given = False
        self.initial_reward_given = False
        
    @property
    def _state(self):
        location = self._location
        percept = self.env.percept(self.agent)
        heading = self.agent.heading
        
        return np.array([location[0], location[1], heading, int(percept[0]), 
                         int(percept[1]), int(percept[2]), int(percept[3]), 
                         int(percept[4])])
        
    @property
    def _location(self): return self.agent.location
    
    @property
    def _percept(self): return self.env.percept(self.agent)
    
    # @property
    # def spec(self):
    #     return WumpusWorld.Spec
    
    # class Spec():
    #     id = "wumpus-v0"