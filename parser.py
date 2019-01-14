#!/usr/bin/env python
import os
import sys
import subprocess
import numpy as np

class Policy:
	def __init__(self,num_states,num_actions, output='program.policy'):
		#f=None
		try:
			f = open(output, 'r')
		#	lines = f.readlines()
		except:
			print('\nError: unable to open file: ' + filename)
		

		lines = f.readlines()

		# the first three and the last lines are not related to the actual policy
		lines = lines[3:]


		self.actions = -1 * np.ones((len(lines), 1, ))
		self.policy = np.zeros((len(lines), num_states, ))

		for i in range(len(lines)):
		# print("this line:\n\n" + lines[i])
			if lines[i].find('/AlphaVector') >= 0:
				break
			l = lines[i].find('"')
			r = lines[i].find('"', l + 1)
			self.actions[i] = int(lines[i][l + 1 : r])

			ll = lines[i].find('>')
			rr = lines[i].find(' <')
			# print(str(i))
			self.policy[i] = np.matrix(lines[i][ll + 1 : rr])
		f.close()


	def select_action(self, b):
	
	# sanity check if probabilities sum up to 1
		if sum(b) - 1.0 > 0.00001:
			print('Error: belief does not sum to 1, diff: ', sum(b)[0] - 1.0)
			sys.exit()

		return int(self.actions[np.argmax(np.dot(self.policy, b.T)), 0])

class Solver:
	def __init__(self):
		path = '/home/saeid/software/sarsop/src/pomdpsol'
		if os.path.exists(path):
			subprocess.check_output(path + ' program.pomdp --timeout 60 --output program.policy', shell=True)
			#subprocess.call(path + ' program.pomdp --timeout 5 --output program.policy', shell=True)

#def main():

#	Policy(5,4)



#if __name__=="__main__":
#	main()