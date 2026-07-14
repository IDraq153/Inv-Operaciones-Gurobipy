import gurobipy
import os

from gurobipy import *

# DEFINIENDO EL MODELO
m = Model("Maquina_Cortadora")

# DEFINO MIS INDICES
clientes = range(7) # -- i: clientes

# DEFINO MI VARIABLE DE DECISION
X = m.addVars(7,name='X') # -- X: cant de algo segun el cliente
##X = {}
##for i in clientes:
  ##  X[i] = m.addVar(name="X",vtype=GRB.CONTINUOUS)

# DEFINO MI ESTRUCTURA DE DATOS
CANTIDAD = [300,250,150,200,150,230,500]
DIFICULTAD = [8,7,6,7,5,5,3]
UTILIDAD = [2.0,2.5,3.0,2.5,2.0,2.5,3.0]

# DEFINO MI FUNCION OBJETIVO
obj = quicksum(UTILIDAD[i]*X[i] for i in clientes)
m.setObjective(obj)
m.ModelSense = GRB.MAXIMIZE

# DEFINO MIS RESTRICCIONES
m.addConstr(quicksum(X[i] for i in clientes) <= 1500)
# Sumatoria de X[i] <= 1500

for i in clientes:
    m.addConstr(X[i] <= CANTIDAD[i])
# X[i] <= CANTIDAD_i

m.addConstr(
    quicksum(DIFICULTAD[i] * X[i] for i in clientes) <= 5 * quicksum(X[i] for i in clientes)
) # Sumatoria de DIFICULTAD_i * X[i] de 1 a 7 <= 5 * Sumatoria de X[i] de 1 a 7 --> el promedio va asi porque no hay divisiones en gurobipy 

# MUESTRO LOS VALORES Y NUESTRO VALOR OPTIMO
m.optimize()

for v in m.getVars():
    print (v.VarName,"\t", v.X,"\t", v.RC)

for c in m.getConstrs():
    print (c.ConstrName,"\t",c.slack,"\t", c.pi)