#! /usr/bin/python3
# -*- coding:utf-8 -*-

import dill as pickle
import matplotlib.pyplot as plt

X = dill.load(open("tmp", "rb"))
Xaxis = X["Xaxis"]
Yaxis = Y["Yaxis"]

plt.plot(Xaxis, Yaxis, "b-")
plt.xlabel("Number of games played for learning")
plt.ylabel("Winning rate")
plt.title("AI learnt with another AI, then played against random bot")
plt.plot()
