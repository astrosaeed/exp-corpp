#!/usr/bin/env python
import math
import numpy as np

def	create_states(n):
	binlist=[]
	for i in range(int(math.pow(2,n))):
		temp = bin(i)[2:]
		temp_n = n - len(temp)
		for i in range(temp_n):
			temp='0'+temp
		binlist.append(temp)
	binlist.append('term')
	#print binlist
	return binlist
	

def create_states_from_bin(n):
	binlist = create_states(n) 
	states= []

	for bi in binlist:
		if bi !='term':
			s=''
			for number in range(len(bi)):
				if bi[number]=='0':
					s+='not'+'s'+str(number)
				else:
					s+='s'+str(number)
				if number != (len(bi)-1):
					s+='_'
			states.append(s)
	states.append('term')
	return states

def get_string_remainder(s,ind):

	if ind!= len(s)-1 and ind!=0:
		return s[:ind] + s[ind+1:]
	elif ind==0:
		return s[1:]
	elif ind== len(s)-1:
		return s[:ind]

def update_trans_mat(n, trans_mat,action_acc):

	for a,action in enumerate(create_actions(n)):
		if 'express' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):

				init_remainder=get_string_remainder(init_state,idx)

				for e, end_state in enumerate(create_states(n)[:-1]):
	
					end_remainder=get_string_remainder(end_state,idx)

					
					if idx==0:

						if init_state[idx]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc
						elif init_state[idx]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc
						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1.0
					else:
						if init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc*0.2
						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=action_acc
						elif init_state[idx]=='0' and init_state[idx-1]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc*0.2
						elif init_state[idx]=='0' and init_state[idx-1]=='1' and end_state[idx]=='0' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1- action_acc
						elif init_state[idx]=='1' and end_state[idx]=='1' and init_remainder== end_remainder:
							trans_mat[a,i,e]=1.0


		if 'confirm' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)):
				for e, end_state in enumerate(create_states(n)):
					if init_state == end_state:
						trans_mat[a,i,e]=1.0

		
	trans_mat[:,len(create_states(n))-1,len(create_states(n))-1]=1.0

	trans_mat[len(create_actions(n))-1,:,len(create_states(n))-1]=1.0

	return trans_mat


def update_obs_mat(n, obs_mat):
	for a,action in enumerate(create_actions(n)):
		if 'express' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):

				if init_state[idx]=='0':
					obs_mat[a,i,0]=0.1
					obs_mat[a,i,1]=0.2
					obs_mat[a,i,2]=0.7
				elif init_state[idx]=='1':
					obs_mat[a,i,0]=0.2
					obs_mat[a,i,1]=0.1
					obs_mat[a,i,2]=0.7					

		if 'confirm' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)[:-1]):
				if init_state[idx]=='0':
					obs_mat[a,i,0]=0.1
					obs_mat[a,i,1]=0.9
					
				elif init_state[idx]=='1':
					obs_mat[a,i,0]=0.9
					obs_mat[a,i,1]=0.1
						

		
	obs_mat[:,len(create_states(n))-1,2]=1.0

	obs_mat[len(create_actions(n))-1,:,2]=1.0

	return obs_mat

def create_actions(n):

	actions=[]
	for action in range(n):
		actions.append('express_s'+str(action))
	for action in range(n):
		actions.append('confirm_s'+str(action))
	actions.append('terminate')

	return actions

def write_trans_mat(Tr, s,n):

	for a,action in enumerate(create_actions(n)):
		s+='\nT: '+action+'\n'
		for i,init_state in enumerate(create_states(n)):
			for e, end_state in enumerate(create_states(n)):
				s+= str(Tr[a,i,e]) +' '
			s+='\n'

	return s

def write_reward_mat(s,n,bonus,penalty,exp_cost,conf_cost):

	for action in create_actions(n):
		if 'express' in action:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(exp_cost)
		elif 'confirm' in action:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(conf_cost)
		else:
			for state in create_states_from_bin(n):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				elif state ==create_states_from_bin(n)[-2]:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(bonus)
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ str(penalty)

	return s


def write_obs_mat(Ob, s,n):

	for a,action in enumerate(create_actions(n)):
		s+='\nO: '+action+'\n'
		for i,init_state in enumerate(create_states(n)):
			for o, obs in enumerate(['pos','neg','na']):
				s+= str(Ob[a,i,o]) +' '
			s+='\n'

	return s

def writeToFile(s,n):

	f = open(str(n)+".pomdp",'w')
	f.write(s)	
	f.close()

def main():
	
	n=5
	s = ''
	s += 'discount : 0.999\n\nvalues: reward\n\nstates: '
	
	for state in create_states_from_bin(n):
		s += state + ' '

	s+='\nactions:'
	for action in create_actions(n):
		s+=action + ' '

	observations=['pos','neg','na']

	s+='\nobservations: pos neg na'

	s+='\nstart: uniform\n'

	trans_mat = np.zeros((len(create_actions(n)),len(create_states_from_bin(n)),len(create_states_from_bin(n))))

	trans_mat = update_trans_mat(n, trans_mat,0.8)	
	s= write_trans_mat(trans_mat, s,n)

	obs_mat = np.zeros((len(create_actions(n)),len(create_states_from_bin(n)),len(observations)))

	obs_mat = update_obs_mat(n, obs_mat)

	s= write_obs_mat(obs_mat, s,n)

	s=write_reward_mat(s,n,100.0,-100.0,-4.0,-2.0)

	

	writeToFile(s,n)

	





if __name__ == '__main__':

	main()