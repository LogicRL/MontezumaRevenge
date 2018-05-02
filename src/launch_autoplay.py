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
import LogicRLUtils as Util
from decoder.CNN_state_parser_pytorch import CNNModel as DecoderCNNModel

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pdb


class AutoAgent(object):
  """
  AutoAgent class.
  """

  def __init__(self, env, decoder, fname_domain, fname_problem):
    super(AutoAgent, self).__init__()
    
    self.env = env
    self.fname_domain = fname_domain
    self.fname_problem = fname_problem

    self.agent_running_cost   = -1e-4
    self.agent_subgoal_reward = 1
    self.agent_failure_cost   = -1
    self.rl_state_joint = 4

    # initialize a symbolic planner
    self.planner = PDDLPlanner(fname_domain, fname_problem)

    # initialize a symbolic state decoder
    self.decoder = decoder

    # initialize a RLAgents pool
    #TODO
    

  def decodeSymbolicState(self, s_dec):
    """
    Decode symbolic state from a lower level state.

    @param s_dec The lower-level decoder state.
    @return The corresponding symbolic state as a set of predicates.
    """

    symbolic_state = set()

    #TODO

    return symbolic_state


  def predictActionByAgent(self, agent_name, s_rl):
    """
    Predict an action to take by an agent at a specific state.

    @param agent_name The name of the agent.
    @param s_rl The lower-level RL state.
    @return The lower-level action predicted by the agent to take.
    """

    a = None

    #TODO

    return a


  def feedbackToAgent(self, agent_name, s_rl, a, s_rl_next, r):
    """
    Provide feedback to an RL agent.

    @param agent_name The name of the RL agent.
    @param s_rl The RL state the agent was at.
    @param a The lower-level action taken by the agent.
    @param s_rl_next The RL state the agent reached after taking the action.
    @param r The reward received by the agent.
    """

    #TODO


  def findSymbolicPlan(self, ss):
    """
    Find a symbolic plan towards the goal.

    @param ss The symbolic state to start from.
    @return A plan found. `None` will be returned if no plan is found.
    """

    plan = self.planner.find_plan(initial_state=ss, goals=None) # using default goals

    return plan


  def extractNextStepFromPlan(self, plan):
    """
    Extract the next step from a plan.

    @param plan The symbolic plan.
    @return A 2-tuple of the next action to take and the expected next symbolic 
            state after the action has been successfully executed, which is 
            defined in the form `()`
    """

    if len(plan) == 0 or plan is None:
      return (None, None)

    return plan[0]


  def autoplay(self, max_episodes=1e6, learn=True, render=False):
    """
    Play autonomously and learn online.

    @param max_episodes The maximum number of episodes to run the AutoAgent.
    @param learn The switch to enable online learning.
    @param render The switch to enable rendering.
    @return A boolean indicating if the agent solve the game within the maximum 
            number of episodes.
    """

    q_rl_frames = deque(maxlen=self.rl_state_joint)

    # loop through the episodes
    for episode in range(max_episodes):
      # reset the environment
      frame = env.reset()

      # initialize states
      s_dec = Util.FrameToDecoderState(frame)
      for i in range(self.rl_state_joint):
        q_rl_frames.append(frame)
      s_rl = Util.FramesToRLState(q_rl_frames)

      # render if requested
      if render:
        env.render()

      done = False
      while not done:
        # find the next symbolic operation
        ss = self.decodeSymbolicState(s_dec)
        plan = self.findPlan(ss)
        op_next, ss_next = self.extractNextStepFromPlan(plan)

        # reset the environment if no plan is found
        if ss_next is None:
          continue

        # indicate success if the goal is reached
        if op_next is None and ss_next is not None:
          return True

        # predict the lower-level action to take
        agent_name = op_next
        a = self.predictActionByAgent(agent_name, s_rl)

        # execute the lower-level action
        frame_next, r_env, done, info = env.step(a)

        # convert states
        s_dec_next = Util.FrameToDecoderState(frame)
        q_rl_frames.append(frame)
        s_rl_next = Util.FramesToRLState(q_rl_frames)

        # render if requested
        if render:
          env.render()

        # feedback to agent
        r_rl = 0
        if s_dec_next == s_dec:
          r_rl = self.agent_running_cost
        elif s_dec_next == ss_next:
          r_rl = self.agent_subgoal_reward
        else:
          r_rl = self.agent_failure_cost
          done = True
        self.feedbackToAgent(agent_name, s_rl, a, s_rl_next, r_rl)

        # update states
        frame = frame_next
        s_dec = s_dec_next
        s_rl = s_rl_next


def main():
  fname_domain = '../PDDL/domain.pddl'
  fname_problem = '../PDDL/problem_room1.pddl'
  
  env = gym.make('MontezumaRevenge-ram-v0')

  decoder_classes = [15]
  decoder = DecoderCNNModel(decoder_classes)

  agent = AutoAgent(env, decoder, fname_domain, fname_problem)

  success = agent.autoplay()
  print('success: %s' % (success))


if __name__ == '__main__':
  main()
