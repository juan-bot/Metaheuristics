import math
import random as rn
import numpy as np
T=5
L=20
alpha=.99
R=0.6
k=1.380649*pow(10,-23)

distancia=np.array([[0, 22, 53, 53],
                    [22, 0, 40, 62],
                    [53, 40, 0, 55],
                    [53, 62, 55, 0]])

flujo=np.array([[0, 3, 0, 2],
                [3, 0, 0, 1],
                [0, 0, 0, 4],
                [2, 1, 4, 0]])

sAct= np.array([2, 1, 4, 3])

sCand=np.array([0,0,0,0])

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

def Costo(sol):
    costo = 0

    for i in range(1,sol.shape[0]):
        i1=sol[i-1]-1
        j1=sol[i]-1
        flow=flujo[i1][j1]
        dist=distancia[i-1][i]
        costo += flow*dist
        print("flujo: [",i1,j1,"]")
        print("distancia: ",distancia[i-1][i])
        print(flow," * ",dist)
        print(i)
    

    return costo

def recocido(sAct,T,L,alpha,R):
    while T > 0.000001 :
        for i in range(L):
            sCand = Genera_Vecino(sAct)
            AE=Costo(sAct) - Costo(sCand)
            if AE >= 0:
                sAct = sCand
            else:
                proba= pow(math.e,-(-AE/(k*T)))
                if proba > R:
                   sAct = sCand 
        T=alpha*T
    return sAct
            
#x = recocido(sAct,T,L,alpha,R)
print(sAct)