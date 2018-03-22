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

import pdb


def main():
  fname_domain = '../PDDL/domain.pddl'
  fname_problem = '../PDDL/problem_room1.pddl'

  print('load planning domain and problem:')
  print('  - domain file: %s' % (fname_domain))
  print('  - problem file: %s' % (fname_problem))
  domprob = pddlpy.DomainProblem(fname_domain, fname_problem)
  print('')

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


if __name__ == '__main__':
  main()
