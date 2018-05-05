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


  def autoplay(self, max_episodes=int(1e6), ss_errtol=0, learn=True, render=False, verbose=False):
    """
    Play autonomously and learn online.

    @param max_episodes The maximum number of episodes to run the AutoAgent.
    @param ss_errtol The symbolic state decoding error tolerance.
    @param learn The switch to enable online learning.
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


def main():
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
  agent = AutoAgent(env, decoder, fname_domain, fname_problem)

  # autoplay
  success = agent.autoplay(ss_errtol=10, render=True, verbose=True)
  print('success: %s' % (success))


if __name__ == '__main__':
  main()
