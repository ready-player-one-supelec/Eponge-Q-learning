import tensorflow as tf 
import numpy as np


class DummyNetwork():
    def __init__(self, dimensions):
        self.name = 'dummy'
    
    def predict(self, data):

        print('prédisez une direction')
        a = int(input('>>> '))
        res = np.zeros((4, 1))
        res[(a, 0)] = 1
        return res
    
    def update(self, data):
        print('/// NETWORK WAS UPDATED ///')
        pass

class Network():
    def __init__(self, dimensions):
        tf.keras.backend.clear_session()
        self.dimensions = dimensions
        input_added = False
        memory_len = dimensions['input'][2]
        self.model = tf.keras.models.Sequential()
        for dim in dimensions['conv']:
            if not(input_added):
                input_added = True
                self.model.add(tf.keras.layers.Conv2D(dim,input_shape=dimensions['input'], kernel_size=(4,4), activation=tf.nn.relu))

            else:
                self.model.add(tf.keras.layers.Conv2D(dim, kernel_size=(4,4), activation=tf.nn.relu))

            self.model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))

        if not(input_added):
            self.model.add(tf.keras.layers.Flatten(input_shape=dimensions['input']))
            input_added = True
        else:
            self.model.add(tf.keras.layers.Flatten())
        for dim in dimensions['dense'][:-1]:
            self.model.add(tf.keras.layers.Dense(dim, activation=tf.nn.tanh))

        self.model.add(tf.keras.layers.Dense(dimensions['dense'][-1], activation=tf.keras.activations.linear))
        self.model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='mean_squared_error',
              metrics=['accuracy'])

    
    def predict(self, states):
        return self.model.predict(states)
    
    def update(self, experiment_tuples, gamma):
        memories_t0 = [ element[0][:,:,1:] for element in experiment_tuples]
        memories_t1 = [ element[0][:,:,:-1] for element in experiment_tuples]
        actions = [ element[1] for element in experiment_tuples ]
        rewards = [ element[2] for element in experiment_tuples ]
        are_terminal = [ element[3] for element in experiment_tuples ]
        
        train_set = np.stack(
            memories_t0,
            axis=0
        )

        next_step_set = np.stack(
            memories_t1,
            axis=0
        )

        train_labels = self.model.predict(train_set)

        next_step_labels = self.model.predict(next_step_set)


        #aimed_Q = np.zeros((train_set.shape[0], self.dimensions['dense'][-1]))
        aimed_Q = np.array(train_labels)
        for i in range(train_set.shape[0]):
            max_index = np.argmax(next_step_labels[i, :])
            aimed_Q[ i, actions[i] ] = rewards[i] + gamma * ( 1 - are_terminal[i] ) * next_step_labels[i, max_index]

        self.model.fit(train_set, aimed_Q, verbose=0, epochs=1, batch_size=aimed_Q.shape[0])

