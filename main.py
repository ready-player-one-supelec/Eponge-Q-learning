#! /usr/bin/python3
# -*- coding: utf-8 -*-

from game import Game
from player import Player
import random


def gameMaster(game, players) :
    currentPlayer = random.randint(0,1)
    while not game.isOver() :
        currentState = game.currentNumberSticks
        if not players[currentPlayer].isBot :
            game.display(players[currentPlayer].name)
        action = players[currentPlayer].play(currentState)
        reward = game.move(action)
        players[currentPlayer].addStateSequence(currentState, action, reward, game.currentNumberSticks)
        currentPlayer = 1 - currentPlayer
        players[currentPlayer].correctStateSequence(-reward, game.currentNumberSticks)
    print("The Winner is {}".format(players[currentPlayer].name))
    players.qLearning()
    game.reset()
    return players

def setOfGames(nbGames, game, players, learningRate, discountFactor, explorationRate) :
    for i in range(nbGames) :
        print(i)
        players.updateConstants(learningRate, discountFactor, explorationRate ** i)
        gameMaster(game, players)
    return players