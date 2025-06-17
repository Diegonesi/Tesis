import re
import pandas as pd
import os

# Ruta base de los archivos
base_path = 'C://Users//diego//Downloads//programacion//Tesis//Resultados estocasticos spark//Nodos = 24//'

# Expresión regular para extraer "Valor" y "Tiempo"
patron = re.compile(r'Valor:\s*(\d+),\s*Tiempo:\s*([\d.]+)s')

# Lista para almacenar todos los resultados
todos_los_datos = []
# Recorrer benchmarks del 1 al 8
for benchmark in range(1, 9):
    carpeta = f'Beanchmark{benchmark}'
    for sufijo in ['', '-2', '-3']:
        archivo = f'Resultados_Spark_Benchmark{benchmark}{sufijo}.txt'
        ruta_archivo = os.path.join(base_path, carpeta, archivo)
        if not os.path.exists(ruta_archivo):
            print(f'Archivo no encontrado: {ruta_archivo}')
            continue
        with open(ruta_archivo, 'r') as f:
            for linea in f:
                match = patron.search(linea)
                if match:
                    valor = int(match.group(1))
                    tiempo = float(match.group(2))
                    todos_los_datos.append({
                        'Benchmark': benchmark,
                        'Subindice': sufijo if sufijo else '-1',
                        'Valor': valor,
                        'Tiempo (s)': tiempo
                    })

# Crear un DataFrame con todos los datos
df = pd.DataFrame(todos_los_datos)

# Guardar en un archivo Excel
df.to_excel('todos_los_resultados_valor_tiempo.xlsx', index=False)

print("Archivo Excel generado: todos_los_resultados_valor_tiempo.xlsx")
