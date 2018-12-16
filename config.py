#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
from game import Game
from player import Player, Players
from main import setOfGames
import dill as pickle


def test_unit(numberOfGamesTest, game, players) :
    print("TESTING")
    players[0].toggleMode(True)
    players[1].toggleMode(True)
    players[1].playRandomly = True
    players.resetStats()
    setOfGames(numberOfGamesTest, game, players, 0,0,[0] * numberOfGamesTest)
    player0Win = players[0].gamesWon
    player1Win = players[1].gamesWon
    players[0].toggleMode(False)
    configurePlayer1(players)
    return player0Win, player1Win

def configurePlayer1(players) :
    players[1].exploiting = False
    players[1].trainable = True
    players[1].playRandomly = False
    return players


def main() :

    learningRate = 0.01
    originalNumberSticks = 12
    discountFactor = 0.9
    explorationRate = 0.999
    game = Game(originalNumberSticks)

    player0 = Player("AI", True, originalNumberSticks)
    player1 = Player("Other bot", True, originalNumberSticks)
    players = Players(player0, player1)
    configurePlayer1(players)
    nbGames = 10000
    numberOfGamesTest = 100000
    step = 100 # number of games between each test of our AI
    explorationRateTable = [explorationRate ** i for i in range(nbGames)]

    Xaxis = []
    Yaxis = []

    for i in range(0, nbGames, step) :
        print(i)
        print("LEARNING")
        setOfGames(step, game, players, learningRate, discountFactor, explorationRateTable[i:i+step])
        a,b = test_unit(numberOfGamesTest, game, players)
        Xaxis.append(i)
        Yaxis.append(a / (a + b))

    X = {
        "Xaxis": Xaxis,
        "Yaxis": Yaxis
    }
    pickle.dump(X, open("tmp","wb"))



main()
