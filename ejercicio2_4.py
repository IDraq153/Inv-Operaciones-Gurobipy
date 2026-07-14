import os
import gurobipy

from gurobipy import *

m = Model("Ceviche_Modelo")

ceviche = range(3)
insumo = range(5)

X = m.addVars(3,name="X")

VENTA = [30,35,28]
VENTAMIN = [500,200,300]
DISPO = [1000,200,100,5000,5000]
COSTO = [24,30,18,0.5,0.1]
INSUMO = [
    [1,0,0,3,3],
    [0,0.5,0,1,0],
    [0.5,0.1,0.3,3,3]
]

obj = ( 
    quicksum(X[i]*VENTA[i] for i in ceviche) - 
    quicksum(
        X[i]*INSUMO[i][j]*COSTO[j] 
        for j in insumo
        for i in ceviche
    ) 
)
m.setObjective(obj)
m.ModelSense = GRB.MAXIMIZE

for i in ceviche:
    m.addConstr(X[i] >= VENTAMIN[i])

for j in insumo:
    m.addConstr(quicksum(X[i]*INSUMO[i][j] for i in ceviche) <= DISPO[j])

m.optimize()

