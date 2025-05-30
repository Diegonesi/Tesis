import Extraer_Datos
import numpy as np

def w_adaptativo(x, C, tipo):
    if x == 0:
        return 4  # !nodo paralelizados
    if tipo == 'log':
        return int(np.log(x) / np.log(1/5) + (C + 2))
    elif tipo == 'frac':
        return int(4 / (x) + C)
    elif tipo == 'euler':
        return int(np.exp(-x + 2) + C)
    elif tipo == 'sigmoid':
        return int(10 * 1 / (1 + np.exp(x)) + C)
    else:
        raise ValueError("Tipo de función no reconocida")

def calcular_funcion_objetivo(X, matriz_relacion, pesos, beneficios, capacidad):
    beneficio_total = 0
    peso_total = 0
    elementos_cubiertos = set()
    for j, seleccionado in enumerate(X): #Recorre los items que se escogieron.
        if seleccionado:
            beneficio_total += beneficios[j] #Funcion Objetivo
            cubiertos_por_j = {i for i, val in enumerate(matriz_relacion[j]) if val == 1}
            elementos_cubiertos.update(cubiertos_por_j) # Agrega todos los elementos en que estan en cada item, no se puede.
            #print(f"Elementos del item {j}: {elementos_cubiertos}")
    peso_total = sum(pesos[i] for i in elementos_cubiertos) #Restriccion.
    if peso_total > capacidad:
        return 0  # No cumple la restriccion
    return beneficio_total,peso_total

ruta = ".\Problemas\Benchmark2.txt"
m, n, capacidad, profits, weights, matriz_relaciones = Extraer_Datos.leer_datos_SUKP(ruta)

#print(w_adaptativo(1,3,'log'))
Optimo_global = [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1]

#print(len(Optimo_global))
#print(f"m = {m}, n = {n}, capacidad = {capacidad}")
#print(f"profits (len={len(profits)}): {profits[:5]}...") # m (Sumo todos las filas seleccionadas) 
#print(f"weights (len={len(weights)}): {weights[:5]}...") # n (escojo una fila y multiplico por estos pesos)
#print(f"relaciones (dim={len(matriz_relaciones)}x{len(matriz_relaciones[0])}): fila 0 = {matriz_relaciones[0][:5]}...")

print(calcular_funcion_objetivo(Optimo_global,matriz_relaciones,weights,profits,capacidad))