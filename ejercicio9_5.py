import gurobipy
from gurobipy import *

m = Model("Ejercicio9_5")

planta = range(4)
almacen = range(3)

X = m.addVars(planta,almacen,name="X",vtype=GRB.INTEGER)
Y = m.addVars(planta,name="Y",vtype=GRB.BINARY)

CAPACIDAD = [950,1150,1000,900]
DEMANDA = [1200,900,500]
COSTOF = [600,900,200,800]
COSTOT = [
    [3,2,4],
    [2,4,3],
    [3,5,3],
    [4,3,2]
]

m.setObjective(
    quicksum(X[i,j]*COSTOT[i][j] for i in planta for j in almacen) +
    quicksum(Y[i]*COSTOF[i] for i in planta), GRB.MINIMIZE
)

for i in planta:
    m.addConstr(quicksum(X[i,j] for j in almacen) <= CAPACIDAD[i]*Y[i])
for j in almacen:
    m.addConstr(quicksum(X[i,j] for i in planta) >= DEMANDA[j])

m.optimize()
for v in m.getVars():
    print(v.VarName, '\t', v.X)
