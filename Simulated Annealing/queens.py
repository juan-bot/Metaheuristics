import math
import random as rn
import numpy as np
import sys
from random import sample
import time

T=5
L=20
alpha=.99
#sAct= np.array([2, 4, 6, 1, 3, 5,7])
sAct=np.arange(1,1001,dtype=int)
np.random.shuffle(sAct)

sCand=sAct
R=0.6
k=1.380649*pow(10,-23)


def Genera_Vecino(sol):
    #sol = np.zeros(size)
    n1 = rn.randint(0, sol.shape[0]-1)
    n2 = rn.randint(0, sol.shape[0]-1)
    if n1 == n2:
        Genera_Vecino(sol)
    else:
        aux = sol[n1]
        sol[n1]=sol[n2]
        sol[n2]=aux
    return sol

def Costo(r):
    h = 0

    for i in range(r.shape[0]-1):
        for j in range( i + 1, r.shape[0]-1):
            if abs(r[i] - r[j]) == j - i:
                h += 1
    return h

def recocido(sAct,T,L,alpha,R):
    while T > 0.0001 :
        for i in range(L):
            sCand = Genera_Vecino(sAct)
            #print(sCand)
            AE=Costo(sCand) - Costo(sAct)
            if AE >= 0:
                sAct = sCand
            else:
                proba= pow(math.e,-(-AE/(k*T)))
                if proba > R:
                   sAct = sCand 
        T=alpha*T
    return sAct
t_inicial = time.time()          
x = recocido(sAct,T,L,alpha,R)
t_final= time.time()
print("Tiempo transcurrido:", t_final - t_inicial )
