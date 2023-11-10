import random
import pulp

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

## Solucion planteamiento GG ##
print("Solucion planteamiento GG")

inp = -1
print('Ingrese numero de instancia (1-10): ')
while(int(inp) < 1 or int(inp) > 10):
    inp = input('Instancia a resolver: ')


# Crear un problema de minimización
problema = pulp.LpProblem("Problema_de_Rutas_Mínimas", pulp.LpMinimize)

#Matriz de costos
c = files[int(inp)-1]

n = len(c)
V = range(n)  # Donde 'n' es el número de pueblos
A = [(i, j) for i in V for j in V if i != j]

# Variables binarias x_ij
x = pulp.LpVariable.dicts("x", A, 0, 1, pulp.LpBinary)
g = pulp.LpVariable.dicts("g", A, 0, n, pulp.LpInteger )

# Función objetivo
problema += pulp.lpSum(c[i][j] * x[(i, j)] for (i, j) in A)

# Restricciones
for i in V:
    problema += pulp.lpSum(x[(i, j)] for j in V if i != j) == 1

for j in V:
    problema += pulp.lpSum(x[(i, j)] for i in V if i != j) == 1

for i in V:
    if(i>=1):
        g1 = (g[(i,j)] for j in V if i != j)
        g2 = (g[(j,i)] for j in V if j>=1 and i != j)
        problema += pulp.lpSum(g1) - pulp.lpSum(g2) == 1

for i in V:
    for j in V:
        if i!=j:
            problema += g[i,j] <= (n-1)*x[(i,j)]

# Resolver el problema
problema.solve()

# Imprimir la solución
print("Ruta:")
for (i, j) in A:
    if x[(i, j)].varValue == 1:
        print(f"x({i},{j}) = 1")
print("Valor optimo instancia ("+str(inp)+") = ", pulp.value(problema.objective))