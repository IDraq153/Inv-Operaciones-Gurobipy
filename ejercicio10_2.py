import gurobipy
from gurobipy import *

m = Model("Modelo_Metas")

pack = range(3)
pais = range(2)
meta = range(4)

X = m.addVars(pack,pais, name="X", vtype=GRB.INTEGER)
E = m.addVars(meta, name="E", vtype=GRB.INTEGER)
F = m.addVars(meta, name="F", vtype=GRB.INTEGER)

BENEFICIO = [30,35,54]
COSTO = [300,350,720]
PESO = [60,90,110]
HABITANTE = [5000000, 6000000]
PACKMAX = 20000
PESOMAX = 1500000

# RESTRICCIONES DURAS
for j in pais:
    m.addConstr(quicksum(X[i,j] for i in pack) <= PACKMAX)
for j in pais:
    m.addConstr(quicksum(X[i,j]*PESO[i] for i in pack) <= PESOMAX) 

# RESTRICCIONES META
# -- mayor igual quitamos el exceso y sumanos faltante
m.addConstr(quicksum(X[i,0] * BENEFICIO[i] for i in pack) - E[0] + F[0] == 0.2*HABITANTE[0])
m.addConstr(quicksum(X[i,1] * BENEFICIO[i] for i in pack) - E[1] + F[1] == 0.2*HABITANTE[1])

# -- mayor igual quitamos el exceso y sumanos faltante
m.addConstr(quicksum(X[2,j] for j in pais) - E[2] + F[2] == 3000)

# -- menor igual quitamos exceso y sumamos faltante
m.addConstr(quicksum(X[i,j]*COSTO[i] for i in pack for j in pais) - E[3] + F[3] == 20000000)

# EQUIVALENCIAS
# -- 1M de dolares equivale a 1000 parquetes supremos
# m.setObjective((1000000/1000)*(7000/100000)*(F[0] + F[1]) + (1000000/1000)*F[2] + E[3], GRB.MINIMIZE)

m.setObjective(70*(F[0] + F[1]) + 1000*F[2] + E[3], GRB.MINIMIZE)
m.optimize()

for v in m.getVars():
    print(v.VarName, '\t', v.Xn)
