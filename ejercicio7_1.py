import gurobipy
from gurobipy import *

m = Model("inventario7_1")

periodo = range(6)

X = m.addVars(periodo, name="X")
S = m.addVars(periodo, name="S")

DEMANDA = [100,250,190,140,220,110]
COSTOPRO = [50,45,55,48,52,50]

obj = (
    quicksum (X[i]*COSTOPRO[i] + S[i]*8
        for i in periodo
    )
)

m.setObjective(obj)
m.ModelSense = GRB.MINIMIZE

m.addConstr(S[0] == 0 + X[0] - DEMANDA[0])

for i in periodo:
    if i > 0:
        m.addConstr(S[i] == S[i-1] + X[i] - DEMANDA[i])

m.optimize()

for v in m.getVars():
    print(v.VarName, "\t", v.X, "\t", v.RC)

for c in m.getConstrs():
    print(c.ConstrName, "\t",c.slack,"\t", c.pi)
