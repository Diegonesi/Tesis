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

#ruta = ".\Problemas\Benchmark2.txt"
#m, n, capacidad, profits, weights, matriz_relaciones = Extraer_Datos.leer_datos_SUKP(ruta)
#print(w_adaptativo(1,3,'log'))

def calcular_peso_total(solucion, matriz_relaciones):
    elementos = set()
    for idx, incluir in enumerate(solucion):
        if incluir:
            elementos.update(np.where(matriz_relaciones[idx])[0])
    return len(elementos)

def calcular_ganancia(solucion, profits):
    return sum(p for p, x in zip(profits, solucion) if x)

def heuristica_estocastica(solucion, profits, matriz_relaciones, capacidad):
    peso = calcular_peso_total(solucion, matriz_relaciones)
    if peso > capacidad:
        return -np.inf
    ganancia = calcular_ganancia(solucion, profits)
    ruido = np.random.normal(0, 1)  # heurística estocástica
    return ganancia + ruido

def generar_vecinos(solucion_actual):
    vecinos = []
    for i in range(len(solucion_actual)):
        if solucion_actual[i] == 0:
            nuevo = solucion_actual.copy()
            nuevo[i] = 1
            vecinos.append(nuevo)
    return vecinos

def beam_search(profits, matriz_relaciones, capacidad, tipo='log', C=2, iteraciones=20):
    n = len(profits)
    solucion_inicial = [0] * n
    haz = [solucion_inicial]
    mejor_solucion = solucion_inicial
    mejor_valor = 0

    for t in range(iteraciones):
        W = w_adaptativo(t, C, tipo)
        candidatos = []

        for s in haz:
            vecinos = generar_vecinos(s)
            for v in vecinos:
                h = heuristica_estocastica(v, profits, matriz_relaciones, capacidad)
                if h > -np.inf:
                    candidatos.append((v, h))

        if not candidatos:
            break

        candidatos.sort(key=lambda x: x[1], reverse=True)
        haz = [x[0] for x in candidatos[:W]]

        for s, h in candidatos[:W]:
            ganancia = calcular_ganancia(s, profits)
            peso = calcular_peso_total(s, matriz_relaciones)
            if peso <= capacidad and ganancia > mejor_valor:
                mejor_valor = ganancia
                mejor_solucion = s

    return mejor_solucion, mejor_valor

# Leer datos
ruta = ".\\Problemas\\Benchmark2.txt"
m, n, capacidad, profits, weights, matriz_relaciones = Extraer_Datos.leer_datos_SUKP(ruta)

# Ejecutar Beam Search
solucion, ganancia = beam_search(profits, matriz_relaciones, capacidad, tipo='log', C=2, iteraciones=25)

print("Ganancia:", ganancia)
print("Solución:", solucion)

