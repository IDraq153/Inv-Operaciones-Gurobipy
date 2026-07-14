import os
import gurobipy

from gurobipy import *

m = Model("Pavo_Modelado")

jamonada = range(4)
pavo = range(3)

X = m.addVars(jamonada,pavo,name="X")

CARNEB = [2,5,8]
CARNEN = [5,3,2]
DISPOPAVO = [100,150,200]
COSTOPAVO = [8,9,12]
DEMANDAJAMON = [50,60,70,60]
PROPORCION = [0.4,0.5,0.6,0.7]

obj = (
    quicksum(
        X[i,j]*COSTOPAVO[j]
        for i in jamonada
        for j in pavo
    )
)
m.setObjective(obj)
m.ModelSense = GRB.MINIMIZE

for j in pavo:
    m.addConstr(
        quicksum( X[i,j] for i in jamonada) <= DISPOPAVO[j]
    )

for i in jamonada:
    m.addConstr(
        quicksum(X[i,j]*(CARNEB[j]+CARNEN[j]) for j in pavo) == DEMANDAJAMON[i]
    )

for i in jamonada:
    m.addConstr(
        quicksum(X[i,j]*CARNEB[j] for j in pavo) >= 
        quicksum(X[i,j]*(CARNEB[j]+CARNEN[j]) for j in pavo) *
        PROPORCION[i]
    )

m.optimize()

