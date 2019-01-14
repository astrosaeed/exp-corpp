#!/usr/bin/env python

import sys
import numpy as np
from numpy import matrix
from numpy import matlib

class Model(object):
  def __init__(self, filename='program.pomdp', parsing_print_flag=True):

    self.filename = filename
    self.print_flag = parsing_print_flag

    try:
      f = open(self.filename, 'r')
    except:
      print('Error: not be able to read ' + filename)

    self.s = f.read()
    start_states = self.s.find('states:')
    self.states = self.s[start_states + 7 : 
                         self.s.find('\n', start_states)].split()

    start_actions = self.s.find('actions:')
    self.actions = self.s[start_actions + 8 : 
                          self.s.find('\n', start_actions)].split()

    start_observations = self.s.find('observations:')
    self.observations = self.s[start_observations + 13 : 
                               self.s.find('\n', start_observations)].split()

    self.trans_mat = np.ones((len(self.actions), len(self.states), 
                          len(self.states)))
    self.obs_mat = np.ones((len(self.actions), len(self.states),
                            len(self.observations)))
    self.reward_mat = np.zeros((len(self.actions), len(self.states), ))
    
    if self.print_flag:
      print('number of states: ' + str(len(self.states)))
      print(self.states)
      print
      print('number of actions: ' + str(len(self.actions)))
      print(self.actions)
      print
      print('number of observations: ' + str(len(self.observations)))
      print(self.observations)
      print

    self.parse_transition_matrix()
    self.parse_observation_matrix()
    self.parse_reward_matrix()

  def parse_transition_matrix(self):
    from_here = 0
    while True:
      ind = self.s.find('T:', from_here)
      if ind == -1:
        break
      ind_enter = self.s.find('\n', ind)
      next_ind_enter = self.s.find('\n', ind_enter + 1)

      action = self.s[ind + 2 : ind_enter]
      # just to remove extra spaces
      action = action.split()[0]

      if action not in self.actions and action is not '*':
        print('Error in reading action: ' + action)
        sys.exit()

      first_line = self.s[ind_enter + 1 : next_ind_enter]

      if 'identity' in first_line:
        if '*' in action:
          self.trans_mat[:] = np.matlib.identity(len(self.states))
        else:
          self.trans_mat[self.actions.index(action)] = np.matlib.identity(
                                                              len(self.states))
        from_here = next_ind_enter
      elif 'uniform' in first_line:
        if '*' in action:
          self.trans_mat[:] = np.ones((len(self.states), len(self.states, ))) / len(self.states)
        else:
          self.trans_mat[self.actions.index(action)] = np.ones((len(self.states),
                  len(self.states, ))) / len(self.states)
        from_here = next_ind_enter
      else:
        # The current POMDP model does not need this part, so it's not tested -
        # use with your own risk
        start_matrix = ind_enter + 1
        end_matrix = self.s.find('\n\n', start_matrix)
        str_matrix = self.s[start_matrix : end_matrix]
        str_matrix = str_matrix.replace('\n', ';')
        if '*' in action:
          self.trans_mat[:] = np.matrix(str_matrix)
        else:
          self.trans_mat[self.actions.index(action)] = np.matrix(str_matrix)

        from_here = end_matrix

    for i in range(len(self.actions)):
      for j in range(len(self.states)):
        if abs(self.trans_mat[i,j].sum() - 1.0) > 0.00001 :
          print('transition matrix, [' + str(i) + ',' + str(j) + \
                ',:], does not sum to 1: ' + str(self.trans_mat[i,j].sum()))
    
    if self.print_flag:
      print('reading transition matrix successfully')
      print(self.trans_mat.shape)
      print

    return self.trans_mat

  def parse_observation_matrix(self):

    # search the first observation matrix from the first char
    from_here = 0

    while True:
      ind = self.s.find('O:', from_here)
      if ind == -1:
        break
      ind_enter = self.s.find('\n', ind)
      next_ind_enter = self.s.find('\n', ind_enter + 1)

      action = self.s[ind + 2 : ind_enter]

      # just to remove extra spaces
      action = action.split()[0]

      if action not in self.actions and action is not '*':
        print('Error in reading action: ' + action)
        sys.exit()

      # the below code assumes:
      # 1, probability values come instantly below the lines with action name,
      # like "O: ask_i";
      # 2, there is an empty line between two observation matrices
      start_matrix = ind_enter + 1
      end_matrix = self.s.find('\n\n', start_matrix)
      str_matrix = self.s[start_matrix : end_matrix]
      str_matrix = str_matrix.replace('\n', '; ')

      # convert a string separated by "; " into a matrix
      self.obs_mat[self.actions.index(action)] = np.matrix(str_matrix)

      # search the next observation matrix by 'O: '
      from_here = ind_enter

    # sanity check: probabilities sum to 1
    for i in range(len(self.actions)):
      for j in range(len(self.states)):
        if abs(self.obs_mat[i,j].sum() - 1.0) > 0.00001:
          print('observation matrix, [' + i + ',' + j + ',:], does not sum to 1')

    if self.print_flag:
      print('reading observation matrix successfully')
      print(self.obs_mat.shape)
      print

    return self.obs_mat

  def parse_reward_matrix(self):
    # here we assume reward is assigned to (s, a), which means the ending state
    # and observation are not considered --- this assumption holds in most
    # problmes, as far as I know

    # search the first reward matrix from the first char
    from_here = 0

    while True:
      # find the first colon
      ind_colon_first = self.s.find('R:', from_here) + 1

      # if no more 'R:' can be found, then break the while loop
      # for unknown reasons, sometimes it returns 0
      if ind_colon_first <= 0:
        break

      # find the second, third and fourth colons
      ind_colon_second = self.s.find(':', ind_colon_first + 1)
      ind_colon_third = self.s.find(':', ind_colon_second + 1)
      ind_colon_fourth = self.s.find(':', ind_colon_third + 1)

      # find the enter
      ind_enter = self.s.find('\n', ind_colon_fourth)

      action = self.s[ind_colon_first + 1 : ind_colon_second]
      action = action.split()[0]
      if action not in self.actions and action is not '*':
        print('Error in parsing action for reward matrix: ' + action)
        sys.exit()

      state = self.s[ind_colon_second + 1 : ind_colon_third]
      state = state.split()[0]
      if state not in self.states and state is not '*':
        print('Error in parsing state for reward matrix: ' + state)

      value = self.s[self.s.rfind('*', 0, ind_enter) + 1 : ind_enter]
      value = float(value.split()[0])

      if action == '*':
        if state == '*':
          self.reward_mat[:] = value
        else:
          self.reward_mat[:, self.states.index(state)] = value
      else:
        if state == '*':
          self.reward_mat[self.actions.index(action), :] = value
        else:
          self.reward_mat[self.actions.index(action), 
                          self.states.index(state)] = value

      # search the next observation matrix by 'O: '
      from_here = ind_enter

    if self.print_flag:
      print('reading reward matrix successfully')
      print(self.reward_mat.shape)
      print

    return self.reward_mat

def main():
  p = Model()
if __name__ == '__main__':
  main()
