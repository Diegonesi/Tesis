def leer_datos_SUKP(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    # Limpiar espacios y saltos de línea
    lineas = [linea.strip() for linea in lineas if linea.strip()]

    # Extraer valores m, n y capacidad de la mochila
    m = int(lineas[0])
    n = int(lineas[1])
    capacidad = int(lineas[2])

    # Extraer ganancias (profits)
    profits_line = lineas[3]
    profits = list(map(int, profits_line.split()))

    # Extraer pesos (weights)
    weights_line = lineas[4]
    weights = list(map(int, weights_line.split()))

    # Extraer la matriz de relaciones (n filas, cada una con m valores)
    matriz_relaciones = []
    for i in range(5, 5 + m):
        fila = list(map(int, lineas[i].split()))
        matriz_relaciones.append(fila)

    return m, n, capacidad, profits, weights, matriz_relaciones

# Ejemplo de uso:
#ruta = ".\Problemas\Benchmark2.txt"
#m, n, capacidad, profits, weights, matriz_relaciones = leer_datos_SUKP(ruta)

# Mostrar resumen
#print(f"m = {m}, n = {n}, capacidad = {capacidad}")
#print(f"profits (len={len(profits)}): {profits[:5]}...")
#print(f"weights (len={len(weights)}): {weights[:5]}...")
#print(f"relaciones (dim={len(matriz_relaciones)}x{len(matriz_relaciones[0])}): fila 0 = {matriz_relaciones[0][:5]}...")

