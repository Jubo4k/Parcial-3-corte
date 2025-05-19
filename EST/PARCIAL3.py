import os
import re
import requests
import json
from collections import defaultdict

def extraer_datos_archivo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.readlines()
            regex = re.compile(
                r'(?P<ip>\d{1,3}(?:\.\d{1,3}){3}) - - \[(?P<fecha>[^\]]+)\] "(?P<metodo>[A-Z]+) (?P<ruta>\S+)'
            )
            datos = []
            for linea in content:
                match = regex.search(linea)
                if match:
                    datos.append({
                        "ip": match.group("ip"),
                        "fecha": match.group("fecha"),
                        "metodo": match.group("metodo"),
                        "ruta": match.group("ruta")
                    })
            return datos
    except Exception as e:
        print(f"Error leyendo el archivo {file_path}: {e}")
        return []

def agrupar_por_pais(entradas):
    api_url = "http://ip-api.com/json/"
    paises = defaultdict(list)
    cache_ips = {}

    for entrada in entradas:
        ip = entrada["ip"]
        if ip in cache_ips:
            pais = cache_ips[ip]
        else:
            try:
                resp = requests.get(f"{api_url}{ip}", timeout=5)
                data = resp.json()
                pais = data.get("country", "Desconocido")
            except:
                pais = "Desconocido"
            cache_ips[ip] = pais

        paises[pais].append(entrada)

    resultado = []
    for pais, ataques in paises.items():
        resultado.append({
            "country": pais,
            "attacks": ataques
        })
    return resultado

# Carpeta con los archivos de log
carpeta_logs = "C:\\Users\\306\\Downloads\\SotM34\\http"  # Asegúrate de que esta ruta sea válida en tu PC

# Recopilar todos los datos de todos los archivos
todos_los_datos = []
for nombre_archivo in os.listdir(carpeta_logs):
    ruta_archivo = os.path.join(carpeta_logs, nombre_archivo)
    if os.path.isfile(ruta_archivo):
        print(f"Procesando archivo: {nombre_archivo}")
        datos = extraer_datos_archivo(ruta_archivo)
        todos_los_datos.extend(datos)

# Agrupar por país y guardar en JSON
resultado_final = agrupar_por_pais(todos_los_datos)

with open("resultado_final.json", "w", encoding="utf-8") as f:
    json.dump(resultado_final, f, indent=2)

print("✅ Resultado guardado como 'resultado_final.json'")
