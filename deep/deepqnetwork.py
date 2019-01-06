import numpy as np 
import tensorflow as tf 
from network import DummyNetwork, Network
from gameenvironment import GameEnvironment
from state import State
import random as rd

# DeepQLearning implements the deep-q-learning algorithm using an instance of a Network, to predict moves, and a State
# It takes input (dimensions, possible_actions, init_data, env, memory_len, mini_batch_size, gamma)
# - dimensions is a python dictionnary, which feeds the dimensions to the network
# - possible_actions is a list of all possible moves the AI will be able to perform during the game
# - init_data is a numpy ndarray of the data of the board at t=0
# - env is an instance of a GameEnvironment
# - memory_len is an int, which gives the amount of frames to represent a state ( State(t) = [ data(t), data(t-1), ..., data(t-memory_len+1)])
# - mini_batch_size is an int, which gives the size of the batch given to the network to update it 
# - gamma is a float between 0 and 1, that corresponds to the coefficient used to update the network
# It has the following methods :
# init_player, which is called by the game environment on initialisation, to give the network its player number
# reset, that calls the reset method of its state
# return_next_action, that calls the network predict method, and returns its argmax, which corresponds to the chosen action
# move_one_step, 



class DeepQLearning():
    def __init__(self, dimensions, possible_actions, init_data, env, memory_len=1, mini_batch_size=1, gamma=0.8, epsilon=0.1):
        self.init_data = init_data
        self.network = Network(dimensions)
        self.possible_actions = possible_actions #array des actions possibles
        self.env = env
        self.gamma = gamma
        self.memory_len = memory_len
        self.mini_batch_size = mini_batch_size
        self.epsilon = epsilon
    
    def init_player(self, index):
        self.index = index
        self.state = State(
            self.init_data,
            self.memory_len,
            self.mini_batch_size,
            self.env.return_reward(index)
        )
        
    
    def reset(self):
        self.state.reset(
            self.env.return_data()
        )
    


    def return_next_action(self, explore=False):
        return np.argmax(
            self.network.predict(
                self.state.return_memory()
            )
        )
    
    def move_one_step(self, explore=False):
        if explore:
            if rd.random() < self.epsilon:
                next_action = rd.choice(self.possible_actions)
            else:
                next_action = self.return_next_action()
            self.state.update_batch( 
                self.env.return_data(),
                self.env.return_reward(self.index),
                next_action,
                self.env.is_over()
            )

            self.network.update(
                self.state.return_mini_batch(),
                self.gamma
            )

        self.state.update_state(
            self.env.return_data()
        )
    
    def has_failed(self):
        return self.env.has_failed(self.index)




    



     
