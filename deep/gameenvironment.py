import matplotlib.pyplot as plt 
import random as rd 
import numpy as np


# In order to adapt our Qlearning algortihm to different games, we must give it a game environment, which contains :
# - an __init__ method
# - a register_players method, which lets player player subscribe to the game, and the give the players their "number"
# - a reset method, to put the game back to the beginning 
# - a return_data method, which returns the content of the game screen at the given time
# - an update method, which given a certain action, updates the content of the game screen accordingly
# - a has_failed method, which indicates if the player has lost
# - a is_over method, which indicates if this is game over, ie if the current state is terminal
# - a return_reward method, which returns the reward associated of the current state, depending on the player
# - a show method, which displays the game screen 

class GameEnvironment():
    def __init__(self, init_data):
        self.init_data = np.array(init_data)
        self.data = init_data
    
    def register_players(self):
        pass
    
    def reset(self):
        self.data = self.init_data[:, :]

    def return_data(self):
        return self.data
    
    def update(self, action):
        self.data = self.data
    
    def has_failed(self):
        return True
    
    def is_over(self):
        return True
    def show(self):
        pass
    
    def return_reward(self):
        pass
        

class Tron(GameEnvironment):
    def __init__(self, init_data):
        self.init_data = np.array(init_data)
        self.data = init_data
        self.dimensions = self.data.shape




    
    def register_players(self, players):
        self.players = players
        self.players_position = [
            (
                self.dimensions[0]//2, 
                1
            ),
            (
                self.dimensions[0]//2,
                self.dimensions[1]-2
            )
        ]
        self.players_failed = [
            False,
            False
        ]
        
        players[0].init_player(0)
        players[1].init_player(1)
        self.mark_spots()

    
    def reset(self):
        self.data = np.array(self.init_data)
        self.players_position = [
            (
                self.dimensions[0]//2, 
                1
            ),
            (
                self.dimensions[0]//2,
                self.dimensions[1]-2
            )
        ]
        self.players_failed = [
            False,
            False
        ]
        self.mark_spots()
        for player in self.players:
            player.reset()


    def update_one_step(self, explore=False):

        self.players_position = [
            self.next_position(
                self.players_position[i],
                self.players[i].return_next_action(explore=explore)
            )
            for i in range(len(self.players))
        ]

        self.players_failed = [ ( self.data[position]==1 ) for position in self.players_position ]

        for player in self.players:
            player.move_one_step(explore=explore)
        
    
        self.mark_spots()


    
    def next_position(self, player_position, action):
        d0, d1 = self.dimensions
        if action==0:#droite
            next_player_position = (
                player_position[0],
                (player_position[1] + 1 )%d1
            )
        elif action==1:#gauche
            next_player_position = (
                player_position[0],
                (player_position[1] - 1 )%d1
            )
        elif action==2:#haut
            next_player_position = (
                (player_position[0] + 1 )%d0,
                player_position[1]
            )
        elif action==3:#bas
            next_player_position = (
                (player_position[0] - 1 )%d0,
                player_position[1]
            )
        return next_player_position
    def mark_spots(self):
        for position in self.players_position:
            self.mark_spot_player(position)


    def mark_spot_player(self, position):
        self.data[position] = 1

    def return_data(self):
        return self.data
    
    def has_failed(self, index):
        return self.players_failed[index]
    
    def is_over(self):
        return any(self.players_failed)
    
    def return_reward(self, index):
        if self.players_failed[index]:
            return -10
        elif any(self.players_failed):
            return 10
        return -2

    def show(self):
        res = ''
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                if self.players_position[0]== (i,j):
                    res += ' @ '
                elif self.players_position[1] == (i,j):
                    res += ' X '
                else:
                    if self.data[i,j] == 1:
                        res += ' % '
                    else:
                        res += '   '
            res +='\n'
        print(res)

class TronComputer():
    def __init__(self, env):
        self.env = env
    
    def init_player(self, index):
        self.index = index
        self.direction = index 
        self.position = self.env.players_position[index]

    def reset(self):
        self.position = self.env.players_position[self.index]

    def return_next_action(self, explore=False):
        res = self.direction
        dir_possibles = []
        for i in range(4):
            if self.env.return_data()[
                self.env.next_position(
                    self.position,
                    ((self.direction+i+1)%4)
                ) ] == 0:
                dir_possibles += [(self.direction + i + 1)%4]
        if len(dir_possibles)>0:
            res = rd.choice(dir_possibles)
        self.direction = res
        return res
    def move_one_step(self, explore=False):
        self.position = self.env.players_position[self.index]


class Labyrinth():
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.data = np.zeros(
            (
                self.dimensions[0]+2,
                self.dimensions[1]+2
            )
        )
        self.reward = np.zeros(
            (
                self.dimensions[0]+2,
                self.dimensions[1]+2
            )
        )
        self.reward[-1, :] = -1
        self.reward[0, :] = -1
        self.reward[:, -1] = -1
        self.reward[:, 0] = -1
        
        for i in range(1, dimensions[0]+1):
            for j in range(1, dimensions[1]+1):
                if (i-1)%2 == 1:
                    left = (i-1)%4==1
                    if left and not(j==1):
                        self.reward[(i,j)] = -1
                    if not(left) and not(j == dimensions[1]):
                        self.reward[(i,j)] = -1
        self.reward[
            (
                dimensions[0],
                dimensions[1]
            )
        ] = 1
        
    def register_player(self, player):
        self.player = player
        self.player_position = (1,1)
        self.data[self.player_position] = 1
        self.player.init_player(0)
    
    def reset(self):
        self.player_position = (1,1)
        self.data[:,:] = 0
        self.data[(1,1)]=1
        self.player.reset()
    
    def return_data(self):
        return self.data
    
    def next_position(self, player_position, action):
        d0, d1 = self.dimensions
        if action==0:#droite
            next_player_position = (
                player_position[0],
                (player_position[1] + 1 )
            )
        elif action==1:#gauche
            next_player_position = (
                player_position[0],
                (player_position[1] - 1 )
            )
        elif action==2:#haut
            next_player_position = (
                (player_position[0] + 1 ),
                player_position[1]
            )
        elif action==3:#bas
            next_player_position = (
                (player_position[0] - 1 ),
                player_position[1]
            )
        return next_player_position
    

    def update_one_step(self, explore=False):
        self.player_position = self.next_position(self.player_position, self.player.return_next_action(explore=explore))
        self.data[:,:] = 0
        self.data[self.player_position] = 1
        self.player.move_one_step(explore=explore)
    
    def is_over(self):
        return self.reward[self.player_position]==-1 or self.reward[self.player_position]==1
    
    def has_failed(self, index):
        return self.reward[self.player_position]==-1
    
    def return_reward(self, index):
        return 10*(self.reward[self.player_position]) - 1

    def show(self):
        res = ''
        d0, d1 = self.dimensions
        for i in range(d0 + 2):
            for j in range(d1+2):
                if self.player_position == (i,j):
                    if self.reward[i,j]==-1:
                        res += 'X@X'
                    else:
                        res+= ' @ '
                elif self.reward[i,j]==1:
                    res += ' O '
                elif self.reward[i,j]==-1:
                    res += 'XXX'
                else:
                    res += '   '
            res += '\n'
        print(res)


