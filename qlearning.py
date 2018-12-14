import numpy as np 
import random as rd 
from policy import *



class Qlearning():
    def __init__(self,init_state, probability=1, lambda_app=0.9, gamma_red=0.1, policy=DeadOrAlive(-1, 1)):
        self.init_state = init_state
        self.current_state = init_state
        self.Qfunction = {}
        self.Qfunction[ self.current_state.index ] = {}
        self.path = [init_state]
        self.lambda_app = lambda_app
        self.gamma_red = gamma_red
        self.probability = probability
        self.policy = policy
        self.policy.init_Q(self)
    
    def reset(self):
        self.current_state = self.init_state
        self.path = [self.init_state]

    def move(self):
        self.move_one_step()
        while ( self.current_state.reward == 0 ):
            self.move_one_step()
    
    def move_one_step(self):
        
        self.current_state = self.current_state.next_states[ self.choose_next_state_index() ]
        #int_a = int(self.current_state.index)
        #print((int_a//10, int_a%10))
        #input()
        self.init_state_Q() # si on ne connait pas l'état, on crée la Qfunction pour cette état
        self.path += [self.current_state]

    
    def choose_next_state_index(self):
        if rd.random() <= self.probability: #cas où on choisit le cas optimal
            return self.current_state.return_max_state_index()[0]
        else: #cas où on prend un chemin au hasard, ou que tout les chemins sont équivalents de Q-valeur 0
            return self.current_state.return_random_state_index()

    
    def return_random_state_index(self):
        return self.current_state.return_random_state_index()
    
    def return_max_state_index(self):
        return self.current_state.return_max_state_index()
    
    def update_Qfunction(self):
        n = len( self.path )
        if self.current_state.reward == -1: #on a perdu, donc on ne garde que la dernière action
            self.path = self.path[n-2:n]
            n = 2
        for i in range(n - 1, 0, -1):
            s1 = self.path[i].index
            s0 = self.path[i-1].index
            max_Q_s1 = self.path[i].return_max_state_index()[1]
            try:
                Q_s0_s1 = self.Qfunction[s0][s1]
            except:
                Q_s0_s1 = 0
            new_Q_value = self.lambda_app * ( self.path[i].reward + self.gamma_red * max_Q_s1 ) + (1 - self.lambda_app ) * Q_s0_s1
            int_0 = int(s0)
            int_1 = int(s1)
            if new_Q_value != 0:
                self.Qfunction[s0][s1] = new_Q_value
    
    def init_state_Q(self):
        try:
            self.Qfunction[ self.current_state.index ] #si l'état actuel ne connait pas les Q-values de ses voisins, on les lui donne
        except:
            self.Qfunction[ self.current_state.index ] = {}
            self.current_state.init_Q(self.Qfunction[
                self.current_state.index
            ])

    def print_path(self): #A CHANGER
        for a in self.path:
            int_a = int(a.index)
            print((int_a//7, int_a%7), ' , ', a.reward)
            print('----')
    
    def print_Q(self):#A CHANGER
        for a in self.Qfunction:
            if self.Qfunction[a]:
                int_a = int(a)
                print("Noeud ", (int_a//7, int_a%7))
                for b in self.Qfunction[a]:
                    int_b = int(b)
                    print((int_a//7, int_a%7), '  -->  ', (int_b//7, int_b%7), ' Q = ', self.Qfunction[a][b])