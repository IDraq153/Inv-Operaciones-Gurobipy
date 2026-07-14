import gurobipy
from gurobipy import *

m = Model("ejercicio7_2")

pastel = range(2)
periodo = range(3)

X = m.addVars(pastel, periodo, name="X")
S = m.addVars(pastel, periodo, name="S")

DEMANDA = [
    [40,30,20],
    [20,30,10]
]

COSTOPRO = [
    [3,3.4,3.8],
    [2.5,2.8,3.4]
]

COSTOINV = [0.5,0.4]

obj = quicksum(
    X[i,j]*COSTOPRO[i][j] +
    S[i,j]*COSTOINV[i]
    for i in pastel
    for j in periodo
)

m.setObjective(obj, GRB.MINIMIZE)

for j in periodo:
    m.addConstr(
        quicksum(X[i,j] for i in pastel) <= 65
    )

for i in pastel:
    m.addConstr(
        S[i,0] == X[i,0] - DEMANDA[i][0]
    )
for i in pastel:
    for j in periodo:
        if j > 0:
            m.addConstr(
                S[i,j] == S[i,j-1] + X[i,j] - DEMANDA[i][j]
            )

m.optimize()