import os
import gurobipy

from gurobipy import *

m = Model("Arena_Modelado")

cantera = range(2)
construccion = range(3)

x = m.addVars(cantera,construccion,name="x")

DEMANDA = [10,5,10]
CAPAC = [18,14]
COSTOA = [100,120]
COSTOT = [
    [30,60,50],
    [60,30,40]
]

obj = quicksum(
    x[i,j] * (COSTOT[i][j] + COSTOA[i])
    for i in cantera
    for j in construccion
)
m.setObjective(obj)
m.ModelSense = GRB.MINIMIZE

for i in cantera:
    m.addConstr(
        quicksum(x[i,j] for j in construccion) <= CAPAC[i]
    )

for j in construccion:
    m.addConstr(
        quicksum(x[i,j] for i in cantera) == DEMANDA[j]
    )

m.optimize()