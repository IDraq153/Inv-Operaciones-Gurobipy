import os 
import gurobipy

from gurobipy import *

m = Model("Sopas_Opt")

sopa = range(3)
insumo = range(4)
tia = range(2)

X = m.addVars(sopa, name="X")
Y = m.addVars(sopa, tia, name="Y")

PRECIO = [30,35,25]
COSTO = [20,30,5,10]
DISPO = [80,40,200,150]
VENTAMIN = [250,100,300]
COSTOT = [
    [20,25],
    [20,30],
    [30,20]
]
REQUE = [
    [0.30,0,0.25,0.25],
    [0,0.30,0.10,0.50],
    [0.15,0.15,1,0.25]
]

obj = (
    quicksum(
        X[i]*PRECIO[i]
        for i in sopa
    ) +
    quicksum(
        Y[i,k]*PRECIO[i]
        for i in sopa
        for k in tia
    ) -
    quicksum(
        COSTO[j]*X[i]*REQUE[i][j]
        for i in sopa
        for j in insumo
    ) -
    quicksum(
        Y[i,k]*COSTOT[i][k]
        for i in sopa
        for k in tia
    )
)

m.setObjective(obj)
m.ModelSense = GRB.MAXIMIZE

for j in insumo:
    m.addConstr(quicksum(REQUE[i][j]*X[i] for i in sopa) <= DISPO[j])


for i in sopa:
    m.addConstr(quicksum(Y[i,k] for k in tia) <= X[i])

m.addConstr(X[i] + quicksum(Y[i,k] for k in tia) >= VENTAMIN[i])

m.optimize()