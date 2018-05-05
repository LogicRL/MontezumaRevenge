#!/usr/bin/env python

"""
launch_autoplay_guided.py
Launch the Montezuma Revenge game with automatic playing and learning, where 
expert may guide the agent to learn more efficiently.
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

key_space_pressed = False
key_left_pressed = False
key_up_pressed = False
key_right_pressed = False
key_down_pressed = False

human_agent_action = ACTION_NOOP
human_guiding = False


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

  global human_guiding

  global key_space_pressed
  global key_left_pressed
  global key_up_pressed
  global key_right_pressed
  global key_down_pressed

  # game environment control
  if key == KEY_ESC:
    human_guiding = not human_guiding
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


class AutoAgent(object):
  """
  AutoAgent class.
  """

  def __init__(self, env, decoder, fname_domain, fname_problem):
    super(AutoAgent, self).__init__()
    
    self.env = env
    self.fname_domain = fname_domain
    self.fname_problem = fname_problem

    self.agent_running_cost   = -1
    self.agent_error_state_cost = -3
    self.agent_subgoal_reward = 100
    self.agent_failure_cost   = -100
    self.rl_state_joint = 4
    self.rl_state_shape = (84, 84, self.rl_state_joint)

    # initialize a symbolic planner
    self.planner = PDDLPlanner(fname_domain, fname_problem)
    self.static_predicate_operators = [
      'keyReachable',
      'swordReachable',
      'rewardReachable',
      'pathExistsInRoom',
      'doorPathExistsInRoom',
      'pathExistsAcrossRooms'
    ]

    # construct predefined initial state and static predicates
    self.static_predicates = set()
    self.predefined_initial_state = set()
    for a in self.planner.predefined_initial_state:
      # construct initial state
      self.predefined_initial_state.add(tuple(a.predicate))

      # construct static predicates
      if a.predicate[0] in self.static_predicate_operators:
        self.static_predicates.add(tuple(a.predicate))

    # construct predefined goals
    self.predefined_goals = set()
    for a in self.planner.predefined_goals:
      self.predefined_goals.add(tuple(a.predicate))

    # initialize a symbolic state decoder
    self.decoder = decoder

    # initialize a RLAgents pool
    self.agents = RLAgents(self.rl_state_shape, self.env.action_space.n)
    

  def decodeSymbolicState(self, s_dec):
    """
    Decode symbolic state from a lower level state.

    @param s_dec The lower-level decoder state.
    @return The corresponding symbolic state as a set of predicates.
    """

    decoded_predicate_strs = set(self.decoder.decode_state(s_dec))
    symbolic_state = set()

    for predstr in decoded_predicate_strs:
      predicate = tuple(predstr.split(','))
      symbolic_state.add(predicate)
    
    symbolic_state = symbolic_state.union(self.static_predicates)

    return symbolic_state


  def predictActionByAgent(self, agent_name, s_rl):
    """
    Predict an action to take by an agent at a specific state.

    @param agent_name The name of the agent.
    @param s_rl The lower-level RL state.
    @return The lower-level action predicted by the agent to take.
    """

    a = self.agents.execute(agent_name, s_rl)

    return a


  def feedbackToAgent(self, agent_name, s_rl, a, s_rl_next, r_rl, done):
    """
    Provide feedback to an RL agent.

    @param agent_name The name of the RL agent.
    @param s_rl The RL state the agent was at.
    @param a The lower-level action taken by the agent.
    @param s_rl_next The RL state the agent reached after taking the action.
    @param r_rl The reward received by the agent.
    @param done A boolean indicating if an episode ends.
    """

    self.agents.feedback(agent_name, (s_rl, a, s_rl_next, r_rl, done))


  def findSymbolicPlan(self, ss):
    """
    Find a symbolic plan towards the goal.

    @param ss The symbolic state to start from.
    @return A plan found. `None` will be returned if no plan is found.
    """

    plan = self.planner.find_plan(initial_state=ss, goals=None) # using default goals

    return plan


  def autoplay(self, max_episodes=int(1e6), ss_errtol=0, learn=True, pause_plan=False, render=False, verbose=False):
    """
    Play autonomously and learn online.

    @param max_episodes The maximum number of episodes to run the AutoAgent.
    @param ss_errtol The symbolic state decoding error tolerance.
    @param learn The switch to enable online learning.
    @param pause_plan The switch to pause while showing the initial plan.
    @param render The switch to enable rendering.
    @param verbose The switch to enable verbose log.
    @return A boolean indicating if the agent solve the game within the maximum 
            number of episodes.
    """

    env = self.env

    q_rl_frames = deque(maxlen=self.rl_state_joint)
    q_rl_rewards = deque(maxlen=self.rl_state_joint)

    g = self.predefined_goals # already converted to predicate sets

    # loop through the episodes
    for episode in range(max_episodes):
      if verbose:
        print('')
      print('[ INFO ] episode: %d / %d' % (episode, max_episodes))

      # reset the environment
      frame = env.reset()

      # initialize states
      s_dec = Util.FrameToDecoderState(frame)
      ss = self.decodeSymbolicState(s_dec)
      for i in range(self.rl_state_joint):
        q_rl_frames.append(frame)
        q_rl_rewards.append(0)
      s_rl = Util.FramesToRLState(list(q_rl_frames))

      # render if requested
      if render:
        env.render()

      # find initial symbolic plan
      plan = self.findSymbolicPlan(ss)
      if episode == 0:
        print('initial plan:')
        show_plan(plan)
        if pause_plan:
          print('')
          input('press ENTER to start autoplay..')
        print('')

      done = False
      ss_errcnt = 0
      while not done:
        # check if a feasible plan exists
        if plan is None or len(plan) == 0:
          done = True
          if verbose:
            print('[ INFO ] failed to find feasible plan')
          continue

        # check if the goal already satisfied
        if len(plan) == 1:
          assert(len(plan[0][1].intersection(g)) == len(g))
          done = True
          continue
          if verbose:
            print('[ INFO ] subgoal satisfied')
          
        # extract states and operator from plan
        ss_cur = plan[0][1]
        op_next = plan[1][0]
        ss_next_expected = plan[1][1]

        # predict the lower-level action to take
        agent_name = op_next
        a = self.predictActionByAgent(agent_name, s_rl)

        # human guided action
        if human_guiding:
          a = human_agent_action

        # execute the lower-level action
        frame_next, r_env, done, info = env.step(a)

        # convert states
        s_dec_next = Util.FrameToDecoderState(frame)
        ss_next = self.decodeSymbolicState(s_dec_next)
        q_rl_frames.append(frame)
        s_rl_next = Util.FramesToRLState(list(q_rl_frames))

        # print state transition
        if len(ss.difference(ss_next)) > 0 or len(ss_next.difference(ss)) > 0:
          print_symbolic_state_transition(ss, ss_next)

        # determine reward for RL agent
        r_rl = 0
        if ss_next == ss_cur:
          # assign subtask reward
          r_rl = self.agent_running_cost

          # reset symbolic state error counter
          ss_errcnt = 0

          # print verbose message
          if verbose:
            print('[ INFO ] symbolic state remains (r_rl: %f, op: %s)' % (r_rl, op_next))

        elif ss_next == ss_next_expected:
          # assign subtask reward
          r_rl = self.agent_subgoal_reward

          # reset symbolic state error counter
          ss_errcnt = 0

          # print verbose message
          if verbose:
            print('[ INFO ] symbolic plan step executed (r_rl: %f, op: %s)' % (r_rl, op_next))

          # replan due to symbolic state change
          plan = self.findSymbolicPlan(ss_next)

        elif ss_errcnt < ss_errtol:
          # assign subtask reward
          r_rl = self.agent_error_state_cost

          # accumulate symbolic state error
          ss_errcnt += 1

          # print verbose message
          if verbose:
            print('[ INFO ] symbolic state error detected (errcnt: %d/%d, r_rl: %f, op: %s)' % (ss_errcnt, ss_errtol, r_rl, op_next))

        else:
          # assign subtask reward
          r_rl = self.agent_failure_cost
          done = True

          # print verbose message
          if verbose:
            print('[ INFO ] subtask failed (r_rl: %f, op: %s)' % (r_rl, op_next))

        # update subtask reward queue
        q_rl_rewards.append(r_rl)

        # render if requested
        if render:
          env.render()

        # feedback to agent
        r_rl_mean = np.mean(q_rl_rewards)
        self.feedbackToAgent(agent_name, s_rl, a, s_rl_next, r_rl_mean, done)

        # update states
        frame = frame_next
        s_dec = s_dec_next
        ss = ss_next
        s_rl = s_rl_next

    return False


def parse_arguments():
    # Command-line flags are defined here.
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_episodes', dest='max_episodes',
                        type=int, default=int(1e6),
                        help="Maximum number of episodes to run the LogicRL agent.")

    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
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
  env.reset()
  env.render()

  # register the event handlers
  env.unwrapped.viewer.window.on_key_press = handle_key_press_event
  env.unwrapped.viewer.window.on_key_release = handle_key_release_event

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
  agent = AutoAgent(env, decoder, fname_domain, fname_problem)

  # autoplay
  success = agent.autoplay(ss_errtol=10, pause_plan=args.plan, render=True, verbose=True)
  print('success: %s' % (success))


if __name__ == '__main__':
  main()
