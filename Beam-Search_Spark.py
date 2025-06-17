import Extraer_Datos
import numpy as np
import time
from pyspark.sql import SparkSession

def w_adaptativo(nivel, parametro_control, tipo_funcion):
    if nivel == 0:
        return 24
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

def seleccion_estocastica(candidatos, w, temperatura=10.0):
    if not candidatos:
        return []
    beneficios = np.array([c[0] for c in candidatos], dtype=np.float64)
    exp_beneficios = np.exp((beneficios - beneficios.max()) / temperatura)
    suma = exp_beneficios.sum()
    if suma == 0:
        probabilidades = np.ones_like(exp_beneficios) / len(exp_beneficios)
    else:
        probabilidades = exp_beneficios / suma
    indices_validos = np.where(probabilidades > 0)[0]
    k = min(w, len(indices_validos))
    if k == 0:
        return []
    indices_seleccionados = np.random.choice(indices_validos, size=k, replace=False, p=probabilidades[indices_validos]/probabilidades[indices_validos].sum())
    seleccionados = [candidatos[i] for i in indices_seleccionados]
    return seleccionados

def generar_solucion_aleatoria(num_items, capacidad, pesos, beneficios, matriz_relacion):
    solucion = [0] * num_items
    indices = list(range(num_items))
    np.random.shuffle(indices)
    for i in indices:
        solucion[i] = 1
        beneficio, peso, _ = calcular_funcion_objetivo(solucion, matriz_relacion, pesos, beneficios, capacidad)
        if peso > capacidad:
            solucion[i] = 0
    return solucion

def beam_search_spark(num_items, capacidad, beneficios, pesos, matriz_relacion, tipo_funcion_haz, parametro_control, archivo_registro, num_nodos):
    spark = SparkSession.builder.master(f"local[{num_nodos}]").appName("BeamSearch-SUKP").getOrCreate()
    sc = spark.sparkContext

    mejor_solucion = None
    mejor_valor = 0
    tiempo_inicio = time.time()

    beam = []

    for nivel in range(num_items):
        candidatos = []
        if nivel == 0:
            w = w_adaptativo(nivel, parametro_control, tipo_funcion_haz)
            soluciones_rdd = sc.parallelize(range(w), numSlices=num_nodos)
            candidatos = soluciones_rdd.map(lambda _: generar_solucion_aleatoria(num_items, capacidad, pesos, beneficios, matriz_relacion)) \
                .map(lambda sol: (calcular_funcion_objetivo(sol, matriz_relacion, pesos, beneficios, capacidad)[0], sol)) \
                .filter(lambda x: x[0] > 0).collect()
        else:
            beam_rdd = sc.parallelize([sol for _, sol in beam], numSlices=num_nodos)
            def expandir(solucion_actual):
                nuevos = []
                for decision in [0, 1]:
                    nueva_solucion = solucion_actual[:]
                    nueva_solucion[nivel] = decision
                    beneficio, peso, elementos_usados = calcular_funcion_objetivo(nueva_solucion, matriz_relacion, pesos, beneficios, capacidad)
                    if peso <= capacidad and beneficio > 0:
                        nuevos.append((beneficio, nueva_solucion, peso, elementos_usados))
                return nuevos

            candidatos = beam_rdd.flatMap(expandir).map(lambda x: (x[0], x[1])).collect()

        # Evaluar mejoras
        for beneficio, sol in candidatos:
            if beneficio > mejor_valor:
                mejor_valor = beneficio
                mejor_solucion = sol
                tiempo_actual = time.time() - tiempo_inicio
                peso_final = calcular_funcion_objetivo(sol, matriz_relacion, pesos, beneficios, capacidad)[1]
                elementos_usados = calcular_funcion_objetivo(sol, matriz_relacion, pesos, beneficios, capacidad)[2]
                with open(archivo_registro, 'a') as f:
                    f.write(f"Valor: {beneficio}, Tiempo: {tiempo_actual:.2f}s, Peso: {peso_final}, Elementos usados: {elementos_usados}, Solucion: {sol}\n")

        w = w_adaptativo(nivel + 1, parametro_control, tipo_funcion_haz)
        beam = seleccion_estocastica(candidatos, w, temperatura=1.0)

        if not beam:
            break

    spark.stop()
    return mejor_solucion, mejor_valor
ruta = "./Problemas/Benchmark1.txt"
num_items, elementos, capacidad, beneficios, pesos, matriz_relaciones = Extraer_Datos.leer_datos_SUKP(ruta)

archivo_registro = "Resultados_Spark_Benchmark1.txt"
num_nodos = 24

mejor_solucion, mejor_valor = beam_search_spark(
    num_items, capacidad, beneficios, pesos, matriz_relaciones,
    tipo_funcion_haz='log', parametro_control=5,
    archivo_registro=archivo_registro,
    num_nodos=num_nodos
)

beneficio, peso_final, elementos_usados = calcular_funcion_objetivo(
    mejor_solucion, matriz_relaciones, pesos, beneficios, capacidad
)

print("Mejor valor encontrado:", beneficio)
print("Peso total:", peso_final, "| Peso maximo:", capacidad)
print("Elementos cubiertos:", elementos_usados)
print("Solución:", mejor_solucion)
