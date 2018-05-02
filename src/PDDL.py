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
from collections import deque

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


def show_plan(plan):
  initial_state = plan[0][1]
  goal_state = plan[-1][1]

  print('initial_state: %s' % (initial_state))
  print('')

  print('plan:')
  for i_step_prev in range(len(plan) - 1):
    i_step = i_step_prev + 1
    opstr, state = plan[i_step]
    print(opstr)
  print('')
  
  print('goal_state: %s' % (goal_state))
  print('')


class PDDLPlanner(object):
  """
  PDDL Planner.
  """

  def __init__(self, fname_domain, fname_problem):
    """
    Initialize a PDDL planner.

    @param domprob The domain problem definition.
    """

    super(PDDLPlanner, self).__init__()
    
    self.fname_domain = fname_domain
    self.fname_problem = fname_problem

    # initialize domain problem definitions
    domprob = pddlpy.DomainProblem(self.fname_domain, self.fname_problem)

    self.predefined_initial_state = domprob.initialstate()
    self.predefined_goal_state = domprob.goals()
    self.operators = domprob.operators()

    # generate grounded operators dictionary
    # note: a new domain problem object needs to be initialized from PDDL files 
    #       everytime a new grounded operator is going to be generated, because 
    #       of the `ground_operator` bug in the `pddlpy` library.
    self.grounded_operators_dict = dict()
    for operator in self.operators:
      domprob = pddlpy.DomainProblem(self.fname_domain, self.fname_problem)
      grounded_operator = list(domprob.ground_operator(operator))
      self.grounded_operators_dict[operator] = grounded_operator


  def _ConstructPlanFromVisits(visited, s, sg):
    """
    (internal, static)
    Construct a plan from visits.

    @param visited The visited trajectory.
    @param s The starting state as a set of predicate tuples.
    @param sg The goal state as a set of predicate tuples.
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

    s = frozenset(s)
    sg = frozenset(sg)
    
    assert(sg in visited)

    plan = []

    # construct plan by backtracking
    s_parent = sg
    while s_parent is not None:
      s_cur = s_parent
      s_parent, opstr = visited[s_cur]
      plan.append((opstr, s_cur))

    # convert the plan to a ordered list
    plan.reverse()

    # validate initial state
    assert(plan[0][0] is None)
    assert(plan[0][1] == s)

    return plan


  def _ConstructOperatorStr(op):
    """
    (internal, static)
    Construct grounded operator string with variables.

    @param op The operator to be converted to a string.
    @return A string of the grounded operator string with variables.
    """

    oplst = [op.operator_name]
    for var_name in op.variable_list:
      oplst.append(op.variable_list[var_name])

    opstr = str(tuple(oplst))

    return opstr


  def _Plan(gops, s, g):
    """
    (internal, static)
    Find a plan from the stating state to the goal state.

    @param gopdict The grounded operators dictionary.
    @param s The starting state as a set of predicate tuples.
    @param g The goals as a set of predicate tuples.
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

    visited = dict() # state -> (parent_state, operator)
    q = deque()

    # initialize the search queue
    q.append((None, None, s)) # (parent_state, operator, state)

    # search for plan with breadth-first search
    while len(q) > 0:
      v = q.popleft()
      s_cur = v[2]
      visited[frozenset(s_cur)] = (frozenset(v[0]) if v[0] is not None else None, v[1])
      
      # search each grounded operator
      for gop_name in gops:
        # retrieve grounded operator
        gop = gops[gop_name]

        # search each grounded operator instance
        for op in gop:
          opstr = PDDLPlanner._ConstructOperatorStr(op)

          # validate operator name
          assert(gop_name == op.operator_name)

          # check operator candidate
          if (len(op.precondition_pos.intersection(s_cur)) == len(op.precondition_pos) and
              len(op.precondition_neg.intersection(s_cur)) == 0):
            s_next = s_cur.copy()

            # remove negative effect
            s_next.difference_update(op.effect_neg)

            # append positive effect
            s_next = list(s_next)
            s_next.extend(list(op.effect_pos))
            s_next = set(s_next)

            # check if goal reached, and construct plan if so
            if len(s_next.intersection(g)) == len(g):
              sg = s_next
              visited[frozenset(sg)] = (frozenset(s_cur), opstr)
              return PDDLPlanner._ConstructPlanFromVisits(visited, s, sg)

            # check if already visited, and append to search queue if not
            if frozenset(s_next) not in visited:
              q.append((s_cur, opstr, s_next))
              #print(opstr)

    return None


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

    if initial_state is not None:
      s = initial_state
    else:
      s = set()
      initial_state = list(self.predefined_initial_state)
      for a in initial_state:
        s.add(tuple(a.predicate))

    if goal_state is not None:
      g = goal_state
    else:
      g = set()
      goal_state = list(self.predefined_goal_state)
      for a in goal_state:
        g.add(tuple(a.predicate))

    s = set(s)
    g = set(g)

    # find plan
    plan = PDDLPlanner._Plan(self.grounded_operators_dict, s, g)

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

  planner = PDDLPlanner(fname_domain, fname_problem)
  plan = planner.find_plan()
  show_plan(plan)

  #IPython.embed()


if __name__ == '__main__':
  main()
