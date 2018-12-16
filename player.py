#! /usr/bin/python3
# -*- coding: utf-8 -*-

import random
import numpy as np

class Player :

    def __init__(self, name, isBot, originalNumberSticks) :
        self.name = name
        self.isBot = isBot
        self.QTable = [[0] * 3 for i in range(1, originalNumberSticks + 1)]
        self.statesSequence = []
        self.explorationRate = 0
        self.learningRate = 0
        self.discountFactor = 0
        self.gamesWon = 0
        self.gamesLost = 0
        self.trainable = True
        self.exploiting = False
        self.playRandomly = False

    def toggleMode(self, bool) :
        self.exploiting = bool
        self.trainable = not bool

    def updateConstants(self, learningRate, discountFactor, explorationRate) :
        if not isinstance(learningRate, type(None)) :
            self.learningRate = learningRate
        if not isinstance(discountFactor, type(None)) :
            self.discountFactor = discountFactor
        if not isinstance(explorationRate, type(None)) :
            self.explorationRate = explorationRate

    def greedyChoice(self, currentState) :
            stateValues = self.QTable[currentState - 1]
            return np.argmax(stateValues) + 1

    def resetStats(self) :
        self.gamesWon = 0
        self.gamesLost = 0

    def updateStats(self, reward) :
        if reward == 1 :
            self.gamesWon += 1
        else :
            self.gamesLost += 1

    def play(self, currentNumberSticks) :
        if self.isBot :
            if not self.playRandomly and (self.exploiting or random.random() > self.explorationRate) :
                action = self.greedyChoice(currentNumberSticks)
            else :
                action = random.randint(1,3)
        else :
            ask = True
            while ask :
                action = input("Choose action: ")
                try :
                    action = int(action)
                except :
                    ask = True
                else :
                    if 0 < action <= 3 :
                        ask = False
        return action

    def addStateSequence(self, currentState, action, reward, nextState) :
        self.statesSequence.append([currentState, action, reward, nextState])

    def correctStateSequence(self, reward, nextState) :
        if len(self.statesSequence) != 0 :
            self.statesSequence[-1][-2:] = [reward, nextState]

    def qLearning(self) :
        self.updateStats(self.statesSequence[-1][2])
        if self.isBot and self.trainable :
            for i in range(len(self.statesSequence)) :
                (state, action, reward, nextState) = self.statesSequence[-i - 1]
                currentQValue = self.QTable[state - 1][action - 1]
                nextStateQValue = 0 if nextState <= 0 else max(self.QTable[nextState - 1])
                newQValue = (1 - self.learningRate) * currentQValue
                newQValue += self.learningRate * (reward + self.discountFactor * nextStateQValue)
                self.QTable[state - 1][action - 1] = newQValue
        self.statesSequence = []


class Players :

    def __init__(self, player1, player2) :
        self.player1 = player1
        self.player2 = player2


    def __getitem__(self, key) :
        if key == 0 :
            return self.player1
        if key == 1 :
            return self.player2
        raise IndexError

    def updateConstants(self, learningRate, discountFactor, explorationRate) :
        self.player1.updateConstants(learningRate, discountFactor, explorationRate)
        self.player2.updateConstants(learningRate, discountFactor, explorationRate)

    def resetStats(self) :
        self.player1.resetStats()
        self.player2.resetStats()

    def qLearning(self) :
        self.player1.qLearning()
        self.player2.qLearning()

    def displayStats(self) :
        print("{} won {} times out of {} games".format(self[0].name, self[0].gamesWon, self[0].gamesWon + self[0].gamesLost))
        print("{} won {} times out of {} games".format(self[1].name, self[1].gamesWon, self[1].gamesWon + self[1].gamesLost))
