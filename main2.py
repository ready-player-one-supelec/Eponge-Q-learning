from state import State
from qlearning import Qlearning
import numpy as np 
import random as rd
import matplotlib.pyplot as plt 

### INITIALISATION DE LA GRILLE ###
d = 7
dimension = (d, d)
radius = d//2
grille = np.zeros(dimension)
iteration = 100
states = []
grille_random = False

if grille_random:
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            reward = 0
            if rd.random() < 0.15 and (i**2 + j**2) >= radius**2:
                grille[(i,j)] = -1
                reward = -1
            #elif rd.random() < 0.05 and (i**2 + j**2) >= radius**2:
            #    grille[(i,j)] = 1
            #    reward = 1
            states += [State(str(i*dimension[0] + j), reward)]

else:
    #grille en zigzag
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            reward = 0
            if i%2 == 1:
                left = i%4==1
                if left and not(j==0):
                    grille[(i,j)] = -1
                    reward = -1
                if not(left) and not(j == dimension[1]-1):
                    grille[(i,j)] = -1
                    reward = -1
            states += [State(str(i*dimension[0] + j), reward)]

            

grille[(d-1, d-1)] = 1
states[-1].reward = 1


for i in range(dimension[0]):
    for j in range(dimension[1]):
        if (i + 1 < dimension[0]):
            states[ i * d + j ].add_next_state( states[ (i + 1) * d + j ] )
        if (i-1 >= 0):
            states[ i * d + j ].add_next_state( states[ (i - 1) * d + j ] )
        if (j-1 >= 0):
            states[ i * d + j ].add_next_state( states[ i * d + (j - 1) ] )
        if (j + 1 < dimension[1]):
            states[ i * d + j ].add_next_state( states[ i * d + (j + 1) ] )


### Impression de la grille
def display_and_save(m, name, save, arrows_to_draw):

    data = m
    heatmap = plt.pcolor(data)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            plt.text(x + 0.5, y + 0.5, '%.2f' % data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='red'
                     )

    plt.colorbar(heatmap)
    for i in range(len(arrows_to_draw)-1):
        i0= arrows_to_draw[i][0]
        j0 = arrows_to_draw[i][1]
        i1 = arrows_to_draw[i+1][0]
        j1 = arrows_to_draw[i+1][1]
        print((i0, j0), '->', (i1, j1))
        color = 'green'
        w = 0.1
        plt.arrow(0.5 + j0, 0.5 + i0, (j1 - j0)*0.5, (i1 - i0)*0.5, width=w, color=color)

    if save:
        plt.savefig('img/' + name + '.png')
    else :
        plt.show()
    plt.clf()

display_and_save(grille, 'grille', True, [])

### APPLICATION DU QLEARNING

Q = Qlearning( states[ 0 ] , probability=1)

for i in range(iteration):

    Q.move()


    Q.update_Qfunction()

    Q.reset()

    if (i%(iteration//10) ==  0 ):
        print('Réalistation : ', i*100/iteration, ' %')
Q.probability = 1

Q.move()


print('_______________________________________________')

chemin = [(int(Q.path[i].index)//d, int(Q.path[i].index)%d) for i in range(len(Q.path))]

display_and_save(grille, 'chemin', True, chemin)






