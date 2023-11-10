import random
import pulp
import copy

#Extraer instancias
def extraeInstancia(path):
    file_aux=[[j for j in i.split(' ')] for i in open(path,'r').read().split('\n')[7:-2]]
    for j in range(1,len(file_aux)):
        for lista in file_aux:
            for i in lista:
                if(i == ''):
                    lista.remove(i)

    for i in range(0,len(file_aux)):
        if(len(file_aux[i])==1):
            file_aux[i-1].append(file_aux[i][0])

    for lista in file_aux:
        if(len(lista) == 1):
            file_aux.remove(lista)

    file = []
    for lista in file_aux:
        lista_aux = [float(numero) for numero in lista]
        file.append(lista_aux)

    return file

files = []

for i in range(1,10+1):
    files.append(extraeInstancia('instancias/inst'+str(i)+'.atsp'))

## Solucion planteamiento DFJ ##
print("Solucion planteamiento DFJ")

inp = -1
print('Ingrese numero de instancia (1-10): ')
while(int(inp) < 1 or int(inp) > 10):
    inp = input('Instancia a resolver: ')

# Funcion que calcula subciclos
def get_plan(r0):
  r=copy.copy(r0)
  ruta = []
  while len(r) != 0:
    plan = [r[0]]
    del (r[0])
    l = 0
    while len(plan) > l:
      l = len(plan)
      for i, j in enumerate(r):
        if plan[-1][1] == j[0]:
          plan.append(j)
          del (r[i])
    ruta.append(plan)
  return(ruta)


# Crear un problema de minimización
problema = pulp.LpProblem("Problema_de_Rutas_Mínimas", pulp.LpMinimize)

#Matriz de costos
c = files[int(inp)-1]

n = len(c)
V = range(n)  # Donde 'n' es el número de pueblos
A = [(i, j) for i in V for j in V if i != j]

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)

# Función objetivo
problema += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A if i!=j)

# Restricciones
for j in V:
    problema += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V:
    problema += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

status = problema.solve()

#Verifica restriccion en subciclos
ruta = [(i,j) for i in V for j in V if i!=j if pulp.value(x[i,j]) == 1]
Q = get_plan(ruta)
sub_ruta = []
while len(Q) != 1:
    for i in range(len(Q)):
        problema += pulp.lpSum(x[Q[i][j][0],Q[i][j][1]] for j in range(len(Q[i]))) <= len(Q[i])-1
    status = problema.solve()
    ruta = [(i, j) for i in V for j in V if i!=j if pulp.value(x[i, j]) == 1]
    Q = get_plan(ruta)
    sub_ruta.append(len(Q))

# Resolver el problema
problema.solve()

print("Ruta:")
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor optimo instancia ("+str(inp)+") = ", pulp.value(problema.objective))