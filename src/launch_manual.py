#!/usr/bin/env python

"""
launch_manual.py
Launch the Montezuma Revenge game with manual control.
"""

__version__     = "0.0.1"
__author__      = "David Qiu"
__email__       = "dq@cs.cmu.edu"
__website__     = "http://www.davidqiu.com/"
__copyright__   = "Copyright (C) 2018, David Qiu. All rights reserved."


import numpy as np
import gym
import time

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pdb


KEY_SPACE = ord(' ') # 32
KEY_A = ord('a') # 97
KEY_W = ord('w') # 119
KEY_D = ord('d') # 100
KEY_S = ord('s') # 115
KEY_P = ord('p') # 112
KEY_LEFT = 65361
KEY_UP = 65362
KEY_RIGHT = 65363
KEY_DOWN = 65364
KEY_ESC = 65307

ACTION_NOOP = 0
ACTION_FIRE = 1
ACTION_UP = 2
ACTION_RIGHT = 3
ACTION_LEFT = 4
ACTION_DOWN = 5
ACTION_UPRIGHT = 6
ACTION_UPLEFT = 7
ACTION_DOWNRIGHT = 8
ACTION_DOWNLEFT = 9
ACTION_UPFIRE = 10
ACTION_RIGHTFIRE = 11
ACTION_LEFTFIRE = 12
ACTION_DOWNFIRE = 13
ACTION_UPRIGHTFIRE = 14
ACTION_UPLEFTFIRE = 15
ACTION_DOWNRIGHTFIRE = 16
ACTION_DOWNLEFTFIRE = 17

key_printscreen_triggered = False

key_space_pressed = False
key_left_pressed = False
key_up_pressed = False
key_right_pressed = False
key_down_pressed = False

human_agent_action = ACTION_NOOP
human_sets_pause = False


def update_human_agent_action():
  """
  Update the human agent action according to the pressed keys.
  """

  global human_agent_action

  if key_up_pressed and key_left_pressed and key_space_pressed:
    human_agent_action = ACTION_UPLEFTFIRE
    return

  if key_up_pressed and key_right_pressed and key_space_pressed:
    human_agent_action = ACTION_UPRIGHTFIRE
    return

  if key_down_pressed and key_left_pressed and key_space_pressed:
    human_agent_action = ACTION_DOWNLEFTFIRE
    return

  if key_down_pressed and key_right_pressed and key_space_pressed:
    human_agent_action = ACTION_DOWNRIGHTFIRE
    return

  if key_up_pressed and key_left_pressed:
    human_agent_action = ACTION_UPLEFT
    return

  if key_up_pressed and key_right_pressed:
    human_agent_action = ACTION_UPRIGHT
    return

  if key_down_pressed and key_left_pressed:
    human_agent_action = ACTION_DOWNLEFT
    return

  if key_down_pressed and key_right_pressed:
    human_agent_action = ACTION_DOWNRIGHT
    return

  if key_up_pressed and key_space_pressed:
    human_agent_action = ACTION_UPFIRE
    return

  if key_down_pressed and key_space_pressed:
    human_agent_action = ACTION_DOWNFIRE
    return

  if key_left_pressed and key_space_pressed:
    human_agent_action = ACTION_LEFTFIRE
    return

  if key_right_pressed and key_space_pressed:
    human_agent_action = ACTION_RIGHTFIRE
    return

  if key_up_pressed:
    human_agent_action = ACTION_UP
    return

  if key_down_pressed:
    human_agent_action = ACTION_DOWN
    return

  if key_left_pressed:
    human_agent_action = ACTION_LEFT
    return

  if key_right_pressed:
    human_agent_action = ACTION_RIGHT
    return

  if key_space_pressed:
    human_agent_action = ACTION_FIRE
    return

  human_agent_action = ACTION_NOOP


def handle_key_press_event(key, mod):
  """
  Key press event handler.
  """

  global human_sets_pause
  global key_printscreen_triggered

  global key_space_pressed
  global key_left_pressed
  global key_up_pressed
  global key_right_pressed
  global key_down_pressed

  # game environment control
  if key == KEY_ESC:
    human_sets_pause = not human_sets_pause
    return

  if key == KEY_P:
    key_printscreen_triggered = True
    return

  # agent control
  if key == KEY_SPACE:
    key_space_pressed = True
  
  if key == KEY_W or key == KEY_UP:
    key_up_pressed = True

  if key == KEY_S or key == KEY_DOWN:
    key_down_pressed = True

  if key == KEY_A or key == KEY_LEFT:
    key_left_pressed = True

  if key == KEY_D or key == KEY_RIGHT:
    key_right_pressed = True

  update_human_agent_action()


def handle_key_release_event(key, mod):
  """
  Key release event handler.
  """

  global key_space_pressed
  global key_left_pressed
  global key_up_pressed
  global key_right_pressed
  global key_down_pressed

  # agent control
  if key == KEY_SPACE:
    key_space_pressed = False
  
  if key == KEY_W or key == KEY_UP:
    key_up_pressed = False

  if key == KEY_S or key == KEY_DOWN:
    key_down_pressed = False

  if key == KEY_A or key == KEY_LEFT:
    key_left_pressed = False

  if key == KEY_D or key == KEY_RIGHT:
    key_right_pressed = False

  update_human_agent_action()


def main():
  """
  Program entry.
  """

  global human_sets_pause
  global key_printscreen_triggered

  # Initialize visualization tool
  matplotlib.interactive(True)

  # Initialize the environment
  env = gym.make('MontezumaRevenge-v0')
  env.reset()
  env.render()

  # Register the event handlers
  env.unwrapped.viewer.window.on_key_press = handle_key_press_event
  env.unwrapped.viewer.window.on_key_release = handle_key_release_event

  last_lives = None
  while True:
    # check pause
    while human_sets_pause:
      env.render()
      time.sleep(0.1)

    # environment roll forward
    s_next, r, done, info = env.step(human_agent_action)

    if last_lives is None:
      print('lives = %s' % (info['ale.lives']))
      last_lives = info['ale.lives']

    if info['ale.lives'] != last_lives:
      print('lives = %s (change: %s)' % (
        info['ale.lives'], info['ale.lives'] - last_lives))
      last_lives = info['ale.lives']
    
    if r != 0:
      print('reward = %s' % (r))
    
    env.render()
    time.sleep(0.05)

    # handle print screen request
    if key_printscreen_triggered:
      key_printscreen_triggered = False
      human_sets_pause = True
      plt.imshow(s_next)
      plt.show()

    # check game over
    if done:
      print('Game Over.')
      exit()


if __name__ == '__main__':
  main()
