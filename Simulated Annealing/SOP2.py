import random
from operator import itemgetter
import copy
import math
import numpy as np
import csv
import time

def readFile(size, name):
    m = np.zeros((0), dtype=int)
    m_prec = np.zeros((0), dtype=int)
    
    with open(name, newline='') as File:  
        i=0
        for row in File:     
            row = row.rstrip()
            row = row.split(",")
            row = list(map(int, row))
            m_np = np.array(row)
            
            if i < size :
                m = np.append(m, m_np, axis=0)
                #print(m_np)
            else:
                m_prec = np.append(m_prec, m_np, axis=0)
            i+=1
    
    m = np.array(m).reshape(size,size)
    m_prec = np.array(m_prec).reshape(int((len(m_prec)/2)),2)
    return m, m_prec

def corregirPrecedencia(solucion,reglas,nodos):
    j = nodos - 2 # Se empieza por el ultimo elemento para buscar las precedencias, es el indice
    while j >= 1:
        k = solucion[j] # se obtiene el valor del elemento del indice j
        # se seleccionan solo las reglas en las que se incluyen el valor a comprobar
        reglasTemp = []
        for regla in reglas:
            if k == regla[0] or k == regla[1]:
                reglasTemp.append(regla)
        #recorremos la solucion desde el inicio para revisar que se cumplan las reglas
        if len(reglasTemp) > 0:
            for i in range(1,nodos):
                for x in reglasTemp:  
                    if solucion[i] == x[0] and k == x[1]: 
                        solucion[i],solucion[j] = solucion[j],solucion[i]
                        j = i
        j-=1
    return solucion

def solucionInicial(numNodos,reglas):
    solucionTemp = []
    solucion = []
    #generacion de numeros aleatorios con su indice para obtener la primera solucion
    for i in range(numNodos-2):
        solucionTemp.append([i+1,random.random()])
    #Se reordenan para poder decidir en que orden visitar los nodos
    solucionTemp.sort(key=itemgetter(1))
    # El primero nodo debe ser siempre el cero
    solucion.append(0)
    #agregar los demas nodos
    for i in list(solucionTemp):
        solucion.append(i[0])
    #El ultimo nodo debe ser numNodos-1
    solucion.append(numNodos-1)
    solucion = corregirPrecedencia(solucion[:],reglas,numNodos)
    return solucion


def solucionVecino(solucion,reglas):
    #generar las posiciones a cambiar
    pos1 = random.randint(1,len(solucion)-2)
    pos2 = random.randint(1,len(solucion)-2)
    while (pos1 == pos2):
        pos2 = random.randint(1,len(solucion)-2)
    #print(pos1, ',', pos2)
    #Relizamos el cambio de acuerdo a los indices 
    solucion[pos1],solucion[pos2] = solucion[pos2],solucion[pos1]
    solucion = corregirPrecedencia(solucion[:],reglas,len(solucion))
    return solucion

def precedencia(solucion,rules):
    
    #tiene que variar estos arreglos dependiendo de cuantas reglas aya.
    auxB = np.zeros(len(rules))
    cont = 0
    for i in range(len(solucion)):
        for j in range(len(rules)):
            
            if rules[j][0] == solucion[i] :
                auxB[j]+=1
            
            if auxB[j] == 1 :
                if rules[j][1] == solucion[i] :
                    auxB[j]+=1               
    for i in range(len(auxB)):
        if auxB[i] == 2 :
            cont+=1
    return cont

def obtenerCosto(solucion,costos,reglas):
    #obtener el total de nodos, se pone -1 porque no es necesario recorrer el ultimo
    nodos = len(solucion)-1 
    #Se obtiene el costo maximo de la tabla (es el que se usara para la penalización)
    costoMax = max(max(fila) for fila in costos)
    costoTotal = 0
    for i in range(nodos):
        costoTotal += costos[solucion[i]][solucion[i+1]] 
    n = precedencia(solucion,reglas)
    costoTotal += n * costoMax
    return costoTotal

def actualizarTemperatura(temperatura,alpha=0.95):
    return alpha * temperatura;

def recocidoSimulado(temperaturaActual,temperaturaFinal,costos,reglas,alpha=0.95,equilibrio=1):
    solucionActual = solucionInicial(nodos,reglas) # Se crea la solucion inicial
    mejorSolucion = copy.deepcopy(solucionActual)
    # mientras no se alcance la temperatura final se debe seguir obteniendo nuevas soluciones
    iteraciones=1 #
    while (temperaturaActual>temperaturaFinal):
        i = 0
      # Mientras el numero de iteraciones no alcance la condicion de equilibrio, al alcanzarla la temperatura disminute
        while (i<equilibrio):
            solVecino = solucionVecino(solucionActual[:],reglas)
            # calcular la diferencia entre el costo de la solicion actual y la solucion vecina
            diferenciaCosto = obtenerCosto(solucionActual,costos,reglas) - obtenerCosto(solVecino,costos,reglas)
            # si el costo es mayor a cero indica que la solucion si mejoro
            if(diferenciaCosto > 0): 
              #la solucion vecino se vuelve la solucion actual (se usa la funcion deepcopy para que no sea una referencia)
                solucionActual = copy.deepcopy(solVecino)
            # si no es mejor entonces por probabilidad se decide si se acepta la nueva solucion
            else:
                try:
                    ans = math.exp(-diferenciaCosto/temperaturaActual)
                except OverflowError:
                    ans = float("inf")
                if(random.uniform(0, 1) < ans):
                    solucionActual = copy.deepcopy(solVecino)
            i += 1
            #Solo comprobar parala mejor solucion
            diferenciaCosto = obtenerCosto(mejorSolucion,costos,reglas) - obtenerCosto(solVecino,costos,reglas)
            if(diferenciaCosto > 0): 
                #la solucion vecino se vuelve la mejor solucion
                mejorSolucion = copy.deepcopy(solVecino)
      # Actualizar la temperatura
        temperaturaActual = actualizarTemperatura(temperaturaActual,alpha)
        iteraciones += 1
    print("Mejor solucion por el metodo:")
    print(solucionActual)
    print(obtenerCosto(solucionActual,costos,reglas))  
    print("Total iteraciones: ", iteraciones)
    return solucionActual,mejorSolucion

name = 'datos50.csv'
nodos = 50
temperaturaInicial = 1000.0
temperaturaFinal = 0.01
alpha = 0.5
equilibrio = 5 # cada cuantos pasos se actualiza la temperatura
costos, reglas = readFile(nodos, name)
t_inicial = time.time()
solucion,mejorSolucion =  recocidoSimulado(temperaturaInicial,temperaturaFinal,costos,reglas)
t_final= time.time()
print(precedencia(solucion,reglas))
print("Mejor solucion en todas las iteraciones")
print(mejorSolucion)
print(obtenerCosto(mejorSolucion,costos,reglas))
print(precedencia(mejorSolucion,reglas))
print("Tiempo transcurrido:", round(t_final - t_inicial, 5))

'''
#parametros
name = 'datos100.csv'
nodos = 100
temperaturaInicial = 1000.0
temperaturaFinal = 0.01
alpha = 0.5
equilibrio = 5 # cada cuantos pasos se actualiza la temperatura
costos, reglas = readFile(nodos, name)
t_inicial = time.time()
solucion,mejorSolucion =  recocidoSimulado(temperaturaInicial,temperaturaFinal,costos,reglas)
t_final= time.time()
print(presedencia(solucion,reglas))
print("Mejor solucion en todas las iteraciones")
print(mejorSolucion)
print(obtenerCosto(mejorSolucion,costos,reglas))
print(presedencia(mejorSolucion,reglas))
print("Tiempo transcurrido:", round(t_final - t_inicial, 5))
'''

'''
#parametros
name = 'datos500.csv'
nodos = 500
temperaturaInicial = 1000.0
temperaturaFinal = 0.01
alpha = 0.5
equilibrio = 1 # cada cuantos pasos se actualiza la temperatura
costos, reglas = readFile(nodos, name)
t_inicial = time.time()
solucion,mejorSolucion =  recocidoSimulado(temperaturaInicial,temperaturaFinal,costos,reglas)
t_final= time.time()
print(presedencia(solucion,reglas))
print("Mejor solucion en todas las iteraciones")
print(mejorSolucion)
print(obtenerCosto(mejorSolucion,costos,reglas))
print(presedencia(mejorSolucion,reglas))
print("Tiempo transcurrido:", round(t_final - t_inicial, 5))
'''




