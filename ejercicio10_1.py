import gurobipy
from gurobipy import *

m = Model("Modelo_Metas")

cosecha = range(5)
destino = range(2)
meta = range(3)

CAPITAL = [3,5,4,2,4]
ALIMENTADOS = [150000,75000,100000,100000,200000]
EMPLEADOS = [10000,15000,12000,13000,15000]
HECTAMAX = [6,4,5,6,5]

X = m.addVars(cosecha,destino, name="X", vtype=GRB.CONTINUOUS)
E = m.addVars(meta, name="E", vtype=GRB.CONTINUOUS)
F = m.addVars(meta, name="F", vtype=GRB.CONTINUOUS)

# RESTRICCIONES DURAS
m.addConstr(quicksum(X[i,j] for i in cosecha for j in destino) <= 15)
for i in cosecha:
    m.addConstr(quicksum(X[i,j] for j in destino) <= HECTAMAX[i])

# RESTRICCIONES METAS
m.addConstr(quicksum(CAPITAL[i]*X[i,0] for i in cosecha) - E[0] + F[0] == 70)
m.addConstr(quicksum(ALIMENTADOS[i]*X[i,1] for i in cosecha) - E[1] + F[1] == 1750000)
m.addConstr(quicksum(EMPLEADOS[i]*X[i,j] for i in cosecha for j in destino) - E[2] + F[2] == 200000)

m.setObjective(1000000*F[0] + 100*(F[1] + F[2]), GRB.MINIMIZE)
m.optimize()

for v in m.getVars():
    print(v.VarName, '\t', v.X)


"""
    PRIORIZACION DE METAS -- sirve solo en la funcion objetivo --
    Mayor prioridad indica un indice de valor de potencia alta
    y asi con mediana y baja
    10^6 - 10^3 - 10^0 orden de prioridades multiplicamos cada F 
"""


