#!/usr/bin/env python

"""
launch_random.py
Launch the Montezuma Revenge game with random control.
"""

__version__     = "0.0.1"
__author__      = "David Qiu"
__email__       = "dq@cs.cmu.edu"
__website__     = "http://www.davidqiu.com/"
__copyright__   = "Copyright (C) 2018, David Qiu. All rights reserved."


import numpy as np
import gym

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pdb


def main():
  env = gym.make('MontezumaRevenge-ram-v0')
  env.reset()
  env.render()

  for t in range(1000):
    s_next, r, done, _ = env.step(env.action_space.sample())
    env.render()

    if done:
      print('Game Over.')
      exit()


if __name__ == '__main__':
  main()
