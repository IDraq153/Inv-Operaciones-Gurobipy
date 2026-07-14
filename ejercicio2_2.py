import os 
import gurobipy

from gurobipy import *

m = Model("Proc_Lingote")

alambre = range(3)
proceso = range(3)

X = m.addVars(alambre,name="X")

LINGOTE = [80,60,50]
PRECIO = [4,5,6]
TIEMPO = [150,120,100]
CAPAPRODU = [
    [0.02,0.10,0.05],
    [0.06,0.08,0.04],
    [0.20,0.06,0.03]
]

obj = quicksum(X[i]*PRECIO[i] for i in alambre)
m.setObjective(obj)
m.ModelSense = GRB.MAXIMIZE

for j in proceso:
    m.addConstr (
        quicksum(CAPAPRODU[i][j] * X[i] for i in alambre) <= TIEMPO[j]
    )

for i in alambre:
    m.addConstr(X[i] <= LINGOTE[i] * 1000)

m.optimize()
for v in m.getVars():
    print (v.VarName,"\t", v.X,"\t", v.RC)

for c in m.getConstrs():
    print (c.ConstrName,"\t",c.slack,"\t", c.pi)