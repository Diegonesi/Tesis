import Extraer_Datos
import numpy as np
import heapq
import time

def w_adaptativo(nivel, parametro_control, tipo_funcion):
    if nivel == 0:
        return 4
    if tipo_funcion == 'log':
        return int(np.log(nivel) / np.log(1 / 5) + (parametro_control + 2))
    elif tipo_funcion == 'frac':
        return int(4 / nivel + parametro_control)
    elif tipo_funcion == 'euler':
        return int(np.exp(-nivel + 2) + parametro_control)
    elif tipo_funcion == 'sigmoid':
        return int(10 / (1 + np.exp(nivel)) + parametro_control)
    else:
        raise ValueError("Tipo de función de ancho de haz no reconocida")

def calcular_funcion_objetivo(solucion, matriz_relacion, pesos, beneficios, capacidad):
    beneficio_total = 0
    elementos_cubiertos = set()
    for j, seleccionado in enumerate(solucion):
        if seleccionado:
            beneficio_total += beneficios[j]
            cubiertos_por_j = {i for i, val in enumerate(matriz_relacion[j]) if val == 1}
            elementos_cubiertos.update(cubiertos_por_j)
    peso_total = sum(pesos[i] for i in elementos_cubiertos)
    if peso_total > capacidad:
        return 0, peso_total, len(elementos_cubiertos)
    return beneficio_total, peso_total, len(elementos_cubiertos)

def registrar_mejora(archivo, valor,pesos, solucion, tiempo, elementos_usados):
    with open(archivo, 'a') as f:
        f.write(f"Valor: {valor}, Tiempo: {tiempo:.4f}s, Peso: {pesos}, Elementos usados: {elementos_usados}, Solucion: {solucion}\n")


def beam_search(num_items, capacidad, beneficios, pesos, matriz_relacion, tipo_funcion_haz, parametro_control, archivo_registro):
    estado_inicial = [0] * num_items
    beam = [(0, estado_inicial)]
    mejor_solucion = estado_inicial
    mejor_valor = 0
    tiempo_inicio = time.time()

    for nivel in range(num_items):
        candidatos = []

        for beneficio_actual, solucion_actual in beam:
            for decision in [0, 1]:
                nueva_solucion = solucion_actual[:]
                nueva_solucion[nivel] = decision
                beneficio, peso, cantidad_elementos_usados = calcular_funcion_objetivo(nueva_solucion, matriz_relacion, pesos, beneficios, capacidad)
                if peso > capacidad or beneficio == 0:
                    continue
                candidatos.append((beneficio, nueva_solucion))
                if beneficio > mejor_valor:
                    mejor_valor = beneficio
                    mejor_solucion = nueva_solucion
                    tiempo_actual = time.time() - tiempo_inicio
                    registrar_mejora(archivo_registro, mejor_valor,peso, mejor_solucion, tiempo_actual, cantidad_elementos_usados)

        w = w_adaptativo(nivel + 1, parametro_control, tipo_funcion_haz)
        beam = heapq.nlargest(w, candidatos, key=lambda x: x[0])

        if not beam:
            break

    return mejor_solucion, mejor_valor

# --- Ejecución del algoritmo ---
ruta = ".\\Problemas\\Benchmark1.txt"
num_items, elementos, capacidad, beneficios, pesos, matriz_relaciones = Extraer_Datos.leer_datos_SUKP(ruta)

archivo_registro = "Resultados_Deterministas_Benchmark1.txt"
mejor_solucion, mejor_valor = beam_search(num_items, capacidad, beneficios, pesos, matriz_relaciones, 'sigmoid', 5, archivo_registro)

beneficio, peso_final, elementos_usados = calcular_funcion_objetivo(mejor_solucion, matriz_relaciones, pesos, beneficios, capacidad)

print("Mejor valor encontrado:", beneficio)
print("Peso total:", peso_final,"| Peso maximo:", capacidad)
print("Elementos cubiertos:", elementos_usados)
print("Solución:", mejor_solucion)
