import numpy as np 
import random as rd 

class State():
    def __init__(self, index, reward=0):
        self.reward = reward #reward of this state
        self.index = index 
        self.next_states = {} # possible next states
        self.next_states_indexes = []
    
    def init_Q(self, Q_dict):
        self.next_states_Q = Q_dict #on donne le dictionnaire des Q-values des arcs 


    def add_next_state(self, next_state):
        self.next_states[next_state.index] = next_state
        self.next_states_indexes += [next_state.index]

    
    def return_random_state_index(self):
        random_index = rd.choice(
            self.next_states_indexes
        )
        return random_index
    
    def return_max_state_index(self):
        max_indexes = [self.next_states_indexes[0]]
        try:
            max_q = self.next_states_Q[max_indexes[0] ]
    
        except:
            max_q = 0

        for action_index in self.next_states_indexes[1:]:
            try:
                action_q = self.next_states_Q[action_index]
            except:
                action_q = 0
            
            if action_q > max_q:
                max_indexes = [action_index]
                max_q = action_q
            if action_q == max_q:
                max_indexes += [action_index]

        return rd.choice(max_indexes), max_q


