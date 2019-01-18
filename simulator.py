#!/usr/bin/env python
from parser import Policy,Solver
from pomdp_parser import Model
import numpy as np

np.set_printoptions(suppress=True)
class Simulator:
	def __init__(self, filename='pomdp.pomdp', output='policy.policy'):

		self.model = Model(filename, parsing_print_flag=False)
		self.policy = Policy(len(self.model.states),len(self.model.actions) ,output)


	def init_belief(self, int_prob):

		l = len(self.model.states)
		b = np.zeros(l)

		# initialize the beliefs of the states with index=0 evenly
		init_belief=[]
		#if int_prob >0.5:
		for i in range(len(self.model.states)):
			if i == 0:
				init_belief.append(1.0)
			else:
				init_belief.append(0)	 
		#else:
		#	init_belief = [0.1,0.1,0.7,0.1, 0]	 
		#int_prob =float(int_prob)
		
		b = np.zeros(len(self.model.states))
		for i in range(len(self.model.states)):
				b[i] = init_belief[i]/sum(init_belief)
		print 'The normalized initial belief would be: '
		print b
#raw_input()
		return b

	def sample (self, alist, distribution):
  
		return np.random.choice(alist, p=distribution)

	def get_state_index(self,state):

		return self.model.states.index(state)


	def robot_nlg(self,a):
		
		if a=='terminate':
			print'Conversation terminated'
		else:
			print'Robot takes action: ' + a 
		
			
		
			
	def human_nlg(self,o):

		if o=='pos':
			print'Human: I see'
		elif o=='neg':
			print'Human: Sorry, I didn\'t catch what you said'
		else:
			pass


	def init_state(self):
	#print self.model.states[0]
		state= 'nots0_nots1' #change it later
		#print '\nRandomly selected state from [not_forward_not_interested,not_forward_interested] =',state
		s_idx = self.get_state_index(state)
		#print s_idx
		return s_idx, state

	def get_obs_index(self, obs):

		return self.model.observations.index(obs)
	def observe(self, a_idx):

				
		p =0.2
		if self.model.actions[a_idx] == 'terminate':
			obs='na'
		elif 'confirm' in self.model.actions[a_idx]:
			obs=self.sample(['pos','neg'],[1-p,p])
		elif 'express' in self.model.actions[a_idx]:
			obs=self.sample(['pos','neg','na'],[0.20,0.1,0.7])

		#if self.model.actions[a_idx] == 'terminate' or 'express' in self.model.actions[a_idx] :
		#	obs='na'
		#else:
		#	obs=self.sample(['pos','neg'],[1-p,p])
		
		#obs = 'na'
		#l=len(self.model.observations)-1
		#o_idx=randint(0,l)
		o_idx=self.get_obs_index(obs)
		print ('observation: ',self.model.observations[o_idx])
		return o_idx

		

	def update(self, a_idx,o_idx,b ):
		b = np.dot(b, self.model.trans_mat[a_idx, :]) 

		b = [b[i] * self.model.obs_mat[a_idx, i, o_idx] for i in range(len(self.model.states))]
			
		b = b / sum(b)
		#raw_input()
		return b



	def run(self):
		print 'Conversation begins'
		#s_idx,temp = self.init_state()
		prob = 0.75
		#if prob >0.5:
			#print 'Assumption: Human might already now statement 1 ' 
		#	print 'Assumptuion: s0 -> s1 \n OR\n Human is already aware of statement 1\n'
		#else:
			#print 'Assumption: Human might already now statement 0 ' 
		#	print 'Assumptuion: s1 -> s0 \nOR\n Human is already aware of statement 0\n'
		b = self.init_belief(prob)
	
		while True:
			print '\n'
			a_idx=self.policy.select_action(b)
			a = self.model.actions[a_idx]
			self.robot_nlg(a)      
			o_idx = self.observe(a_idx)
			o = self.model.observations[o_idx]
			self.human_nlg(o)
			#print a
								#print ('transition matrix shape is', self.model.trans_mat.shape)
								#print self.model.trans_mat[a_idx,:,:]
								#print ('observation matrix shape is', self.model.obs_mat.shape)
								#print self.model.trans_mat[a_idx,:,:]
								#print s_idx
						 #R = R + self.model.reward_mat[a_idx,s_idx]
						#print 'Reward is : ', cost
								#print ('Total reward is,' , cost)              
			b =self.update(a_idx,o_idx, b)
			print b
			#raw_input()


			if 'terminate' in a:

				print ('Conversation ends\n ')

				break
						#cost = cost + self.model.reward_mat[a_idx,s_idx]



def main():
		
		#a=Simulator(filename='2.pomdp', output='2.policy')
		n = FLAGS_n
		a=Simulator(filename=n+'.pomdp', output=n+'.policy')
		a.run()


	   

if __name__=="__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--n', type=str, required=True, default=3,
						help="The number of statements of an explanation")
	args = parser.parse_args()
	for k, v in vars(args).items():
		globals()['FLAGS_%s' % k] = v
	main()

