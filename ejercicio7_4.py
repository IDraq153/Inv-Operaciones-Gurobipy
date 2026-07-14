import gurobipy
from gurobipy import *

m = Model("ejercicio7_3")

vehiculo = range(2)
periodo = range(3)

X = m.addVars(vehiculo,periodo,name="X")
P = m.addVars(vehiculo,periodo,name="P", vtype=GRB.INTEGER)
S = m.addVars(vehiculo,periodo,name="S")

INVINI = [200,100]
COSTOP = [6000,7500]
COSTOINV = [150,200]
PRECIO = [8000,9000]
DEMANDA = [
    [1100,1500,1200],
    [600,700,500]
]

obj = (
    quicksum (
        X[i,j]*PRECIO[i]
        -
        P[i,j]*COSTOP[i]
        -
        S[i,j]*COSTOINV[i]
        for i in vehiculo
        for j in periodo
    )
)
m.setObjective(obj)
m.ModelSense = GRB.MAXIMIZE

for i in vehiculo:
        m.addConstr(
            S[i,0] == INVINI[i] + P[i,0] - X[i,0]
        )

for i in vehiculo:
    for j in periodo:
          if j > 0:
                m.addConstr(
                      S[i,j] == S[i,j-1] + P[i,j] - X[i,j]
                )
for j in periodo:
      m.addConstr(
            quicksum(P[i,j] for i in vehiculo) <= 1500
      )

m.addConstr(
      3*P[0,0] >= 2*quicksum(P[i,1] for i in vehiculo)
)
for i in vehiculo:
    for j in periodo:
        m.addConstr(
            X[i,j] <= DEMANDA[i][j]
        )

m.optimize()
for v in m.getVars():
     print(v.VarName, "\t", v.X, "\t", v.RC)
for c in m.getConstrs():
     print(c.ConstrName, "\t", c.slack, "\t", c.pi)
    