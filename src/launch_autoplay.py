#!/usr/bin/env python

"""
launch_autoplay.py
Launch the Montezuma Revenge game with automatic playing and learning.
"""

__version__     = "0.0.1"
__author__      = "David Qiu"
__email__       = "dq@cs.cmu.edu"
__website__     = "http://www.davidqiu.com/"
__copyright__   = "Copyright (C) 2018, David Qiu. All rights reserved."


import sys
import argparse
import numpy as np
import gym
from collections import deque
from PDDL import PDDLPlanner, show_plan
from utils import LogicRLUtils as Util
from decoder.CNN_state_parser_pytorch import CNNModel as DecoderCNNModel
from RLAgents.RLAgents import RLAgents
from AutoAgent import AutoAgent, print_symbolic_state_transition

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pdb, IPython


def parse_arguments():
    # Command-line flags are defined here.
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_episodes', dest='max_episodes',
                        type=int, default=int(1e6),
                        help="Maximum number of episodes to run the LogicRL agent.")

    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    parser_group = parser.add_mutually_exclusive_group(required=False)
    parser_group.add_argument('--render', dest='render',
                              action='store_true',
                              help="Whether to render the environment.")
    parser_group.add_argument('--no-render', dest='render',
                              action='store_false',
                              help="Whether to render the environment.")
    parser.set_defaults(render=False)

    parser_group = parser.add_mutually_exclusive_group(required=False)
    parser_group.add_argument('--plan', dest='plan',
                              action='store_true',
                              help="Whether to pause while showing the initial plan.")
    parser_group.add_argument('--skip-plan', dest='plan',
                              action='store_false',
                              help="Whether to pause while showing the initial plan.")
    parser.set_defaults(plan=False)

    return parser.parse_args()


def main():
  args = parse_arguments()

  fname_domain = '../PDDL/domain.pddl'
  fname_problem = '../PDDL/problem_room1.pddl'
  
  # initialize environment
  env = gym.make('MontezumaRevenge-v0')

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

  # initialize agent
  static_predicate_operators = [
    'actorRevivesOnSpot',
    'keyReachable',
    'swordReachable',
    'rewardReachable',
    'monsterReachable',
    'pathExistsInRoom',
    'doorPathExistsInRoom',
    'monsterPathExistsInRoom',
    'pathExistsAcrossRooms'
  ]
  agent = AutoAgent(env, decoder, fname_domain, fname_problem, static_predicate_operators)

  # autoplay
  success = agent.autoplay(ss_errtol=10, pause_plan=args.plan, render=args.render, verbose=True)
  print('success: %s' % (success))


if __name__ == '__main__':
  main()
