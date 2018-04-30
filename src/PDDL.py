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


import pddlpy

import pdb, IPython


def show_ground_operators(domprob, operator):
  grounded_operator = list(domprob.ground_operator(operator))
  for op in grounded_operator:
    print(op.operator_name)
    print(' - variable_list: %s' % (op.variable_list))
    print(' - precondition_pos: %s' % (op.precondition_pos))
    print(' - precondition_neg: %s' % (op.precondition_neg))
    print(' - effect_pos: %s' % (op.effect_pos))
    print(' - effect_neg: %s' % (op.effect_neg))
    print('')


def show_domprob_summary(domprob):
  lst_initstates = list(domprob.initialstate())
  print('initial states: %d' % (len(lst_initstates)))
  for i in range(len(lst_initstates)):
    print('  - %s' % (str(lst_initstates[i])))
  print('')

  lst_operators = list(domprob.operators())
  print('operators: %d' % len(lst_operators))
  for i in range(len(lst_operators)):
    print('  - %s' % (str(lst_operators[i])))
  print('')

  lst_goals = list(domprob.goals())
  print('goals: %d' % (len(lst_goals)))
  for i in range(len(lst_goals)):
    print('  - %s' % (str(lst_goals[i])))
  print('')


class PDDLPlanner(object):
  """
  PDDL Planner.
  """

  def __init__(self, domprob):
    """
    Initialize a PDDL planner.

    @param domprob The domain problem definition.
    """

    super(PDDLPlanner, self).__init__()
    
    self.domprob = domprob


  def _Plan(gops, s, g):
    """
    (internal, static)
    Find a plan from the stating state to the goal state.

    @param gopdict The grounded operators dictionary.
    @param s The starting state as a set of predicate tuples.
    @param g The goal state as a set of predicate tuples.
    @return A list of tuples, each of which contains the symbolic action to 
            take and the post-effect (the state to become after the action is 
            taken). The list is defined as the following:
            ```
            [ (a, s_next), ... ]
            ```
            where `a` the symbolic action as a string to take and `s_next` is 
            the symbolic state as a set of predicate tuples to become after the 
            action is taken.
    """

    # TODO

    return []


  def find_plan(self, initial_state=None, goal_state=None):
    """
    Find a plan from the stating state to the goal state.

    @param initial_state The starting state as a set of predicate tuples. 
                         (optinal, default: as defined in `domprob`)
    @param goal_state The goal state as a set of predicate tuples. (optinal, 
                      default: as defined in `domprob`)
    @return A list of tuples, each of which contains the symbolic action to 
            take and the post-effect (the state to become after the action is 
            taken). The list is defined as the following:
            ```
            [ (a, s_next), ... ]
            ```
            where `a` the symbolic action as a string to take and `s_next` is 
            the symbolic state as a set of predicate tuples to become after the 
            action is taken.
    """

    if s is not None:
      s = initial_state
    else:
      s = set()
      initial_state = list(self.domprob.initialstate())
      for a in initial_state:
        s.add(tuple(a.predicate))

    if g is not None:
      g = goal_state
    else:
      g = set()
      goal_state = list(self.domprob.goals())
      for a in goal_state:
        g.add(tuple(a.predicate))

    s = set(s)
    g = set(g)

    # construct grounded operators dictionary
    gops = dict()
    for operator in self.domprob.operators():
      grounded_operator = list(self.domprob.ground_operator(operator))
      gops[operator] = grounded_operator

    # find plan
    plan = PDDLPlanner._Plan(gops, s, g)

    return plan


def main():
  fname_domain = '../PDDL/domain.pddl'
  fname_problem = '../PDDL/problem_room1.pddl'

  print('load planning domain and problem:')
  print('  - domain file: %s' % (fname_domain))
  print('  - problem file: %s' % (fname_problem))
  domprob = pddlpy.DomainProblem(fname_domain, fname_problem)
  print('')

  show_domprob_summary(domprob)

  IPython.embed()


if __name__ == '__main__':
  main()
