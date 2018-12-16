#! /usr/bin/python3
# -*- coding:utf-8 -*-

import sys
from game import Game
from player import Player, Players
from main import setOfGames


def main() :

    learningRate = 0.01
    originalNumberSticks = 12
    discountFactor = 0.9
    explorationRate = 0.999
    game = Game(originalNumberSticks)

    player1 = Player("Arpad", True, originalNumberSticks)
    player2 = Player("Joanna", True, originalNumberSticks)
    players = Players(player1, player2)

    nbGames = 10000
    setOfGames(nbGames, game, players, learningRate, discountFactor, explorationRate)

    players.resetStats()
    nbGames = 1000000
    players[0].toggleMode(True)
    players[1].toggleMode(True)
    # players[1].isBot = False
    players[1].playRandomly = True

    setOfGames(nbGames, game, players, 0,0,0)
    players.displayStats()

main()
