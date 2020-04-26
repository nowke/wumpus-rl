# Wumpus RL

## Setup Python Environment

#### Create new environment with Python 3.7

```sh
conda create -n wumpus-rl python=3.7
conda activate wumpus-rl
```

#### Install packages

```sh
pip install -r requirements.txt
pip install -e gym-wumpus
```

## Using Wumpus Environment

* The sample code uses `wumpus-v0` environment that is defined inside `gym-wumpus/` folder. 
* This assumes you have already run `pip install -e gym-wumpus` command, which installs the wumpus world as a dependency inside the Python virtual environment.

#### Sample usage execution

```sh
>>> import gym_wumpus   # To be imported before `gym`
>>> import gym

>>> env = gym.make('wumpus-v0') # Initialize wumpus environment
>>> env.reset()
array([1, 1, 0, 0, 0, 0, 0, 0], dtype=uint32)

>>> env.render()
Scores: <Explorer>=0
  0   1   2   3   4   5    time_step=0
|---|---|---|---|---|---|
| # | # | # | # | # | # | 5
|---|---|---|---|---|---|
| # |   |   |   |   | # | 4
|---|---|---|---|---|---|
| # | W | G | P |   | # | 3
|---|---|---|---|---|---|
| # |   |   |   |   | # | 2
|---|---|---|---|---|---|
| # | ^ |   | P |   | # | 1
|---|---|---|---|---|---|
| # | # | # | # | # | # | 0
|---|---|---|---|---|---|

>>> env.step(2)  # Forward action
(array([1, 2, 0, 1, 0, 0, 0, 0], dtype=uint32), -1, False, {})

>>> env.render()
Scores: <Explorer>=-1
  0   1   2   3   4   5    time_step=1
|---|---|---|---|---|---|
| # | # | # | # | # | # | 5
|---|---|---|---|---|---|
| # |   |   |   |   | # | 4
|---|---|---|---|---|---|
| # | W | G | P |   | # | 3
|---|---|---|---|---|---|
| # | ^ |   |   |   | # | 2
|---|---|---|---|---|---|
| # |   |   | P |   | # | 1
|---|---|---|---|---|---|
| # | # | # | # | # | # | 0
|---|---|---|---|---|---|
```

#### Modifying `gym-wumpus` environment

* [`gym-wumpus/gym_wumpus/envs/wumpus_env.py`](gym-wumpus/gym_wumpus/envs/wumpus_env.py) - Defines the `gym.Env` class skeleton for Wumpus World environment. Modify the class to change the behavior.

Once modified, you can use the new enviornment in **two** ways:

1. Reinstall `gym-wumpus` package from the root of the repository

```sh
pip install -e gym-wumpus
```

2. Use the environment directly from the folder (no need to reinstall again and again)

```python
import sys
import gym
sys.path.append('gym-wumpus')  
# NOTE: This assumes you are running this in root of repository
# You can give relative paths or absolute path to `gym-wumpus` folder

from gym_wumpus.envs import WumpusWorld

env = WumpusWorld()

# You can use `env` object just as a regular `gym` environment
env.render()

# Pass `rgb_array` to the `render` method to get numpy array
# of the rendered image --> this can be used to generate GIFs
np_arr_img = env.render('rgb_array')
```

## Using DQN code

#### Running code

Run [`dqn/wumpus_dqn.py`](dqn/wumpus_dqn.py) file

```
cd dqn
./setup.sh
python wumpus_dqn.py
```

Run `clean.sh` to clear out the generated `logs`, `models`, and `tests`

```sh
./clean.sh
```

#### Hyperparameters

Change the hyperparameters inside [`dqn/wumpus_dqn.py`](dqn/wumpus_dqn.py) file

```python

...

episodes = 35000
agent = Agent(gamma=0.95, epsilon=0.9, epsilon_dec=1e-6, lr=0.01, 
            input_dims=env.observation_space.shape,
            n_actions=7, mem_size=1000000, batch_size=64,
            epsilon_end=0.01)

...

```
