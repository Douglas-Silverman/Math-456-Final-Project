# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 02:03:12 2020

@author: calvi
"""
import math

def poisson(lambdaa, k):
    pmf = ((lambdaa**k) * math.exp(-lambdaa)) / math.factorial(k)
    return pmf

def calculate_win(likely_goals1,likely_goals2):
    probWin = 0
    for i in range (1,5):
        for j in range(0,i):
            probWin += poisson(likely_goals1,i) * poisson(likely_goals2,j)
    return(probWin*100)