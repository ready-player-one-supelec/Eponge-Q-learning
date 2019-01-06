import numpy as np 
from gameenvironment import Tron, TronComputer
from deepqnetwork import DeepQLearning
from network import DummyNetwork
import tensorflow as tf
import time 
import matplotlib.pyplot as plt



image_dimensions = (19, 20)
memory_len = 3
mini_batch_size = -1

input_dimensions = (
    image_dimensions[0],
    image_dimensions[1],
    memory_len
)
init_data = np.zeros(image_dimensions)
init_data[:, 0] = 1
init_data[:, -1] = 1
init_data[0, :] = 1
init_data[-1, :] = 1



dimensions = {
    'input': input_dimensions,
    'conv': [],
    'dense': [10000, 4]
}
iterations = 1000
nb_tests = 100
wins = 0

game_env = Tron(init_data)

Dql = DeepQLearning(dimensions, [0,1,2,3], init_data, game_env,memory_len=memory_len, mini_batch_size=mini_batch_size)

Computer = TronComputer(game_env)

game_env.register_players([
    Dql,
    Computer
])

percentages = []

game_env.show()


for i in range(1, iterations+1):
    while not(game_env.is_over()):
        game_env.update_one_step(explore=True)
        #if i%(iterations//10)==0:
        #    game_env.show()
        #    input("/// APPUYEZ SUR ENTREE ")
    game_env.reset()
    if i%(iterations//100)==0:
        wins = 0
        for j in range(nb_tests):
            while not(game_env.is_over()):
                game_env.update_one_step(explore=False)
            if not(Dql.has_failed()):
                wins += 1
            game_env.reset()
        print("///// PERCENTAGE OF VICTORY : %.2f %% " % (wins*100/nb_tests))
        percentages += [(i,wins*100/nb_tests)]
        #input("APPUYEZ SUR ENTREE >>>")
        #if Dql.has_failed():
        #    print("/// PERDU !")
        #else:
        #    print("/// GAGNE !")
        #input("/// APPUYEZ SUR ENTREE ")
    if i%(iterations//100)==0:
        print("/// COMPLETION : %.2f %%" % (i*100/iterations))

for i in range(nb_tests):
    while not(game_env.is_over()):
        game_env.update_one_step(explore=False)
    if not(Dql.has_failed()):
        wins += 1
    game_env.reset()

print("///// PERCENTAGE OF VICTORY : %.2f %% " % (wins*100/nb_tests))
game_env.show()
while not(game_env.is_over()):
    
    game_env.update_one_step(explore=False)
    game_env.show()

if Dql.has_failed():
    print("PERDU !")
else:
    print("GAGNE !")

x = [a[0] for a in percentages]
y = [a[1] for a in percentages]

plt.plot(x,y)
plt.savefig('percentages_of_victory.png')