import gurobipy
from gurobipy import *

m = Model("Ejercicio10_3")

paquete = range(3)
pais = range(2)
meta = range(4)

X = m.addVars(paquete, pais, name="X", vtype=GRB.INTEGER)
E = m.addVars(meta, name="E", vtype=GRB.INTEGER)
F = m.addVars(meta, name="F", vtype=GRB.INTEGER)

BENEFICIO = [30,35,54]
HABITANTE = [5000000,6000000]
PESO = [60,90,110] 
COSTO = [300,350,720]

# RESTRICCIONES DURAS
for j in pais:
    m.addConstr(quicksum(X[i,j] for i in paquete) <= 20000)
for j in pais:
    m.addConstr(quicksum(X[i,j]*PESO[i] for i in paquete) <= 1500000)

# RESTRICCIONES METAS
m.addConstr(quicksum(X[i,0] * BENEFICIO[i] for i in paquete) - E[0] + F[0] == 0.2*HABITANTE[0]) 
m.addConstr(quicksum(X[i,1] * BENEFICIO[i] for i in paquete) - E[1] + F[1] == 0.2*HABITANTE[1]) 

m.addConstr(quicksum(X[2,j] for j in pais) - E[2] + F[2] == 3000) 

m.addConstr(quicksum(X[i,j]*COSTO[i] for i in paquete for j in pais) - E[3] + F[3] == 20000000)

m.setObjective((F[0] + F[1]) + F[2] + E[3], GRB.MINIMIZE)
m.optimize()

for v in m.getVars():
    print(v.VarName, '\t', v.X)