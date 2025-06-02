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
    return beneficio_total,peso_total,len(elementos_cubiertos)
