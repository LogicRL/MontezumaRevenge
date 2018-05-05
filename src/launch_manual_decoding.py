#!/usr/bin/env python

"""
launch_manual_decoding.py
Launch the Montezuma Revenge game with manual control and symbolic state 
decoding.
"""

__version__     = "0.0.1"
__author__      = "David Qiu"
__email__       = "dq@cs.cmu.edu"
__website__     = "http://www.davidqiu.com/"
__copyright__   = "Copyright (C) 2018, David Qiu. All rights reserved."


import numpy as np
import gym
import time

from utils import LogicRLUtils as Util
from decoder.CNN_state_parser_pytorch import CNNModel as DecoderCNNModel

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pdb, IPython


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


def decodeSymbolicState(decoder, s_dec):
  """
  Decode symbolic state from a lower level state.

  @param s_dec The lower-level decoder state.
  @return The corresponding symbolic state as a set of predicates.
  """

  decoded_predicate_strs = set(decoder.decode_state(s_dec))
  symbolic_state = set()

  for predstr in decoded_predicate_strs:
    predicate = tuple(predstr.split(','))
    symbolic_state.add(predicate)

  return symbolic_state


def print_symbolic_state_transition(s1, s2, prefix=''):
  """
  Print the difference between two symbolic states.

  @param s1 The original symbolic state.
  @param s2 The updated symbolic state.
  @param prefix The prefix added to the front of each line.
  """

  predicates_neg = s1.difference(s2)
  predicates_pos = s2.difference(s1)

  for p in predicates_neg:
    print(prefix + '- ' + str(p))

  for p in predicates_pos:
    print(prefix + '+ ' + str(p))


def main():
  """
  Program entry.
  """

  global human_sets_pause
  global key_printscreen_triggered

  # initialize visualization tool
  matplotlib.interactive(True)

  # initialize symbolic state decoder
  decoder_classes               = [14]
  decoder_label_dir             = '../annotated_data/symbolic_states_room1' 
  decoder_frame_dir             = '../annotated_data/symbolic_states_room1' 
  decoder_predicates_file       = '../annotated_data/predicates.txt'
  decoder_weights_dir           = '../model_weights'
  decoder_pretrained_model_file = decoder_weights_dir + '/parser_epoch_17_loss_7.19790995944436e-05_valacc_0.9992972883597884.t7'

  decoder = DecoderCNNModel(
    decoder_classes,
    pretrained_model_pth=decoder_pretrained_model_file,
    text_dir=decoder_label_dir,
    img_dir=decoder_frame_dir,
    label_file=decoder_predicates_file,
    weights_dir=decoder_weights_dir)

  # initialize the environment
  env = gym.make('MontezumaRevenge-v0')
  s = env.reset()
  s_dec = Util.FrameToDecoderState(s)
  ss = decodeSymbolicState(decoder, s_dec)
  env.render()

  # print initial predicates
  print('initial predicates:')
  for p in ss:
    print('+ %s' % (str(p)))
  print('')

  # register the event handlers
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
      print('env_lives = %s' % (info['ale.lives']))
      last_lives = info['ale.lives']

    if info['ale.lives'] != last_lives:
      print('env_lives = %s (change: %s)' % (
        info['ale.lives'], info['ale.lives'] - last_lives))
      last_lives = info['ale.lives']

    if r != 0:
      print('env_reward = %s' % (r))

    s_dec_next = Util.FrameToDecoderState(s_next)
    ss_next = decodeSymbolicState(decoder, s_dec_next)

    if len(ss.difference(ss_next)) > 0 or len(ss_next.difference(ss)) > 0:
      print_symbolic_state_transition(ss, ss_next)
      print('')
    
    env.render()
    time.sleep(0.05)

    # handle print screen request
    if key_printscreen_triggered:
      key_printscreen_triggered = False
      human_sets_pause = True
      plt.imshow(s_next)
      plt.show()

    # update state
    s = s_next
    s_dec = s_dec_next
    ss = ss_next

    # check game over
    if done:
      print('Game Over.')
      exit()


if __name__ == '__main__':
  main()
