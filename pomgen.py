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
	return binlist
	

def create_states_from_bin(n):
	binlist = create_states(n) 
	states= []

	for bi in binlist:
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

def update_trans_mat(n, trans_mat):
	for a,action in enumerate(create_actions(n)):
		if 'express' in action:
			idx= int(action.split('_')[1][1])
			for i,init_state in enumerate(create_states(n)):

				init_remainder=get_string_remainder(init_state,idx)

				for e, end_state in enumerate(create_states(n)):
	
					end_remainder=get_string_remainder(end_state,idx)
				

					if init_state[idx]=='0' and end_state[idx]=='1' and init_remainder== end_remainder:
						trans_mat[a,i,e]=0.8
					elif init_state[idx]=='0' and end_state[idx]=='0' and init_remainder== end_remainder:
						trans_mat[a,i,e]=0.2
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
			for i,init_state in enumerate(create_states(n)):

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
			for i,init_state in enumerate(create_states(n)):
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

def write_obs_mat(Ob, s,n):

	for a,action in enumerate(create_actions(n)):
		s+='\nO: '+action+'\n'
		for i,init_state in enumerate(create_states(n)):
			for o, obs in enumerate(['pos','neg','na']):
				s+= str(Ob[a,i,o]) +' '
			s+='\n'

	return s

def writeToFile(s):

	f = open("test.pomdp",'w+')
	f.write(s)	
	f.close()

def main():
	

	s = ''
	s += 'discount : 0.999\n\nvalues: reward\n\nstates: '
	
	for state in create_states_from_bin(3):
		s += state + ' '

	s+='\nactions:'
	for action in create_actions(3):
		s+=action + ' '

	observations=['pos','neg','na']

	s+='\nobservations: pos neg na'

	s+='\nstart: uniform\n'

	trans_mat = np.zeros((len(create_actions(3)),9,9))

	trans_mat = update_trans_mat(3, trans_mat)	
	s= write_trans_mat(trans_mat, s,3)

	obs_mat = np.zeros((len(create_actions(3)),9,len(observations)))

	obs_mat = update_obs_mat(3, obs_mat)

	s= write_obs_mat(obs_mat, s,3)

	for action in create_actions(3):
		if 'express' in action:
			for state in create_states_from_bin(3):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ '-4.0'
		elif 'confirm' in action:
			for state in create_states_from_bin(3):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ '-2.0'
		else:
			for state in create_states_from_bin(3):
				if state =='term':
					s+='\nR:'+action+' : '+state+' : * :* '+ '0.0'
				elif state ==create_states_from_bin(3)[-2]:
					s+='\nR:'+action+' : '+state+' : * :* '+ '100.0'
				else:
					s+='\nR:'+action+' : '+state+' : * :* '+ '-100.0'

	writeToFile(s)

	





if __name__ == '__main__':

	main()