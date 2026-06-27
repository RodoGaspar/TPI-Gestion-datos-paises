"""
TPI - Programación 1 | UTN TUPAD
Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas
"""

import csv
import os

ARCHIVO_CSV = "paises.csv"
CAMPOS = ["nombre","poblacion", "superficie", "continente"]

#---------------------------------------------------------
#       LECTURA / ESCRITURA CSV
#---------------------------------------------------------

def cargar_paises(archivo: str) -> list:
    """Lee el CSV y retorna una lista de diccionarios. Si no existe, retorna lista vacía."""
    paises = []
    if not os.path.exists(archivo):
        print(f"[INFO] El archivo '{archivo}' no existe. Se iniciará con una lista vacía ")
        return paises
    try:
        with open(archivo, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                # Validar que la fila tenga todos los campos esperados, de no ser así la ignora.
                if not all(campo in fila  for campo in CAMPOS):
                    print(f"[ADVERTENCIA] Fila ignorada por formato incorrecto: {fila}")
                    continue
                try:
                    paises.append({
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"].strip()
                    })
                except ValueError:
                    print(f"[ADVERTENCIA] Fila ignorada (valores no numéricos): {fila}")
    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo: {e}")
    return paises
