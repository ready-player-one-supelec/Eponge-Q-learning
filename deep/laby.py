from gameenvironment import Labyrinth
from deepqnetwork import DeepQLearning

import matplotlib.pyplot as plt 




image_dimensions = (7, 8)
memory_len = 2
mini_batch_size = 50



input_dimensions = (
    image_dimensions[0]+2,
    image_dimensions[1]+2,
    memory_len
)




dimensions = {
    'input': input_dimensions,
    'conv': [],
    'dense': [2000, 4]
}
iterations = 1000
max_nb_steps = 200
nb_tests = 100
wins = 0

game_env = Labyrinth(image_dimensions)

Dql = DeepQLearning(dimensions, [0,1,2,3], game_env.return_data(), game_env,memory_len=memory_len, mini_batch_size=mini_batch_size, epsilon=0.3)


game_env.register_player(Dql)
game_env.show()
x = range(iterations)
y = [0 for _ in range(iterations)]
for j in range(nb_tests):
    Dql = DeepQLearning(dimensions, [0,1,2,3], game_env.return_data(), game_env,memory_len=memory_len, mini_batch_size=mini_batch_size, epsilon=0.3)
    print(' ///// new player created')
    game_env.register_player(Dql)
    for i in range(iterations):
        steps = 0
        while not( game_env.is_over()) and (max_nb_steps > steps):
            game_env.update_one_step(explore=True)
            steps +=1
        if Dql.has_failed() or steps == max_nb_steps:
            print(j, "eme test", i, "eme itération : PERDU !")

        else:
            print(j, 'eme test',i, "eme itération : GAGNE !")
            y[i]+=1
            Dql.epsilon = Dql.epsilon/2
        game_env.reset()

        #if i%(iterations//10) == 0:
        #    while not(game_env.is_over()):
        #        game_env.update_one_step(explore=False)
        #        game_env.show()
        #        input('>>>')
        #    game_env.reset()

    
#
#while not(game_env.is_over()):
#    game_env.update_one_step(explore=False)
#    game_env.show()
#    input('>>>')


plt.plot(x,y, 'r+')
plt.xlabel("Nombres d'itérations")
plt.ylabel("%% de victoires")

plt.savefig("pourcentages_victoires_labyrinthe.png")
