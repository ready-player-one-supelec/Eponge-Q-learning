import numpy as np
import random as rd 

# batch is a database of all the encountered states, and all necessary Q to update the network
#   ---> contains tuples like ( s_t 'union' s_t+1 , action_t , reward_t+1, is_terminal ), here called 'experiment tuples'
#   given that s_t an s_t+1 share memory_len-1 frames in common, a number of memory_len+1 frames is being transmitted
# reward_t+1 is the reward obtained by going from s_t to s_t+1, is_terminal is a Boolean indicating whether s_t+1 is terminal
# memory is an array of size (image.shape) x memory_len, which helps to represent the current state
# current_data is the data of the board at the current time
# return_mini_batch returns the current state (w/ memory), along some other exemples from the batch database 
# chosen randomly to train the network
class State():
    def __init__(self, init_data, memory_len, mini_batch_size, current_reward):
        self.current_data = init_data
        self.memory_len = memory_len
        self.mini_batch_size = mini_batch_size
        self.memory = np.stack([init_data for _ in range(memory_len)], axis=2) 
        self.batch = [] 

    def reset(self, init_data):
        self.current_data = init_data
        self.memory = np.stack([init_data for _ in range(self.memory_len)], axis=2)

    
    def update_batch(self, next_data, next_reward, action, is_terminal):
        self.current_experiment_tuple = (
            np.concatenate([
                np.reshape( next_data, (next_data.shape[0], next_data.shape[1], 1) ),
                self.memory[:,:,:]
            ], axis=2),
            action,
            next_reward,
            is_terminal
        )
        self.batch += [self.current_experiment_tuple]

    def update_state(self, next_data):
        self.current_data = next_data
        self.memory = np.concatenate([
            np.reshape( next_data, (next_data.shape[0], next_data.shape[1], 1) ),
            self.memory[:,:,:-1]
        ], axis=2)
    
    def return_memory(self):
        return np.stack([self.memory], axis=0)
    
    def return_mini_batch(self):
        if self.mini_batch_size == -1:
            return self.batch
        n = min( self.mini_batch_size, len(self.batch) )
        return [self.current_experiment_tuple] + rd.sample(self.batch[:-1], n - 1)  

    



    
