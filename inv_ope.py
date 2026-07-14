import gurobipy
from gurobipy import *

#def de modelo
m = Model("model")

prendas = range(7) #def de amplitud

#def de variable de decisión
X = {}
for i in prendas:
    X[i] = m.addVar(name="X",vtype = GRB.CONTINUOUS)

#estructura de datos
MAXIMO = [300,250,150,200,150,230,500]
DIFICULTAD = [8,7,6,7,5,5,3]
UTILIDAD = [2,2.5,3,2.5,2,2.5,3]

#función objetivo
obj = quicksum(UTILIDAD[i]*X[i] for i in prendas)
m.setObjective(obj)
m.modelSense = GRB.MAXIMIZE

#restricciones
for i in prendas:
    m.addConstr(X[i]<=MAXIMO[i])
    
m.addConstr(quicksum(X[i] for i in prendas)<=1500)

m.addConstr(quicksum(DIFICULTAD[i]*X[i] for i in prendas)<=5*quicksum(X[i] for i in prendas))

m.optimize()
for v in m.getVars():
    print (v.VarName,"\t", v.X,"\t", v.RC)
for c in m.getConstrs():
    print (c.ConstrName,"\t",c.slack,"\t", c.pi)