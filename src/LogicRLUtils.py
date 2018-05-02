#!/usr/bin/env python

"""
LogicRLUtils.py
The general utilities for LogicRL.
"""

__version__     = "0.0.1"
__author__      = "David Qiu"
__email__       = "dq@cs.cmu.edu"
__website__     = "http://www.davidqiu.com/"
__copyright__   = "Copyright (C) 2018, David Qiu. All rights reserved."


import numpy as np

import pdb, IPython


decoder_frame_width = 84
decoder_frame_height = 84

rl_frame_width = 84
rl_frame_height = 84
rl_state_joint = 4


def FrameToDecoderState(frame):
  """
  Convert a raw frame to a decoder state.

  @param frame The raw frame received from environment.
  @return The decoder state converted from the raw frame.
  """

  #TODO

  return None


def FramesToRLState(frames):
  """
  Convert a list of raw frames to a RL agent state.

  @param frames The raw frames to received as a list.
  @return The RL agent state converted from the raw frames.
  """

  assert(len(frames) == rl_state_joint)

  #TODO

  return None

