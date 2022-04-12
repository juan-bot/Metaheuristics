import math
import random as rn
import numpy as np
import sys
import time as t
sys.setrecursionlimit(100000000)

tam = 50
v=np.random.randint(1,20, size=(tam)) 
p=np.random.randint(1,20, size=(tam))
#v=np.array([5,22,12,10,8,14,10,18,10,6,13,11,7,3,15,19,20,21,16,9,13,10,15,12,17])
#p=np.array([4,19,8,6,9,16,10,15,7,8,10,10,5,1,17,21,15,10,8,10,11,8,10,8,21])
cap=50
T=60
L=30
alpha=.95
size = v.shape[0]
sAct= np.zeros(size)
sCand=sAct
R=0.6
k=1.380649*pow(10,-23)



def Genera_Vecino(sol, size, cap):
    r = rn.randint(0, size-1)
    
    if sol[r] == 0:
        sol[r] = 1
    else:
        sol[r] = 0
    pSol = pesos(sol,size)
    while pSol > cap:
        i = rn.randint(0,size-1)
        sol[i] = 0
        pSol = pesos(sol,size)
        
    return sol

def Costo(sol,size):
    f=0
    for i in range(size):
        if sol[i] == 1:
            f+=v[i]
    return f

def pesos(sol,size):
    f=0
    for i in range(size):
        if sol[i] == 1:
            f+=p[i]
    return f

def recocido(sAct,T,L,alpha,R):
    while T > 0.00001 :
        for i in range(L):
            sCand = Genera_Vecino(sAct,size,cap)
            AE=Costo(sCand,size) - Costo(sAct,size)
            if AE >= 0:
                sAct = sCand
            else:
                proba= pow(math.e,-(-AE/(k*T)))
                if proba > R:
                   sAct = sCand 
        T=alpha*T
    return sAct

t_ini = t.time()            
x = recocido(sAct,T,L,alpha,R)
t_fin = t.time()
#print("Solucion optima: ", x)
print("Tiempo: ", t_fin - t_ini)
val = 0
cos = 0
for i in range(size):
    if x[i] == 1:
        val += v[i]
        cos += p[i]
print("valor total de la solucion: ", val)
print("sumatoria de pesos: ", cos)
print("capacidad ",cap)