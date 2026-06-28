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

def guardar_paises(paises: list, archivo: str) -> None:
    """ Escribe la lista de paises en el CSV """
    try:
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            entrada = csv.DictWriter(f, fieldnames=CAMPOS)
            entrada.writeheader()
            entrada.writerows(paises)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo {e}")

#---------------------------------------------------------
#       FUNCIONES DE ENTRADA
#---------------------------------------------------------

def pedir_entero(mensaje: str, minimo: int = 0) -> int:
    """Solicita un entero válido >= minimo."""
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        print(f"[ERROR] Ingresá un número entero mayor o igual a {minimo}.")


def pedir_texto(mensaje: str) -> str:
    """ Solicita un texto no vacío """
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("[ERROR] El campo no puede estar vacío.")


#---------------------------------------------------------
#       FUNCIONALIDADES PRINCIPALES
#---------------------------------------------------------

def agregar_pais(paises: list) -> None:
    """ Agrega un nuevo pais a la lista. No permite campos vacíos """
    print("\n --- AGREGAR PAÍS ---")
    nombre = pedir_texto("Ingrese el nombre del país: ")

    # Verifica que no esté duplicado
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            print(f"[ERROR] ya existe un país con el nombre {nombre}")
            return
    poblacion = pedir_entero("Ingrese la población: ", minimo = 1)
    superficie = pedir_entero("Ingrese la superficie en km²: ", minimo = 1)
    continente = pedir_texto("Ingrese el continente: ")

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })
    print(f"[OK] País '{nombre}' agregado correctamente.")



def actualizar_pais(paises: list) -> None:
    """ Actualiza población o superficie de un país existente """
    print("\n── ACTUALIZAR PAÍS ──")
    nombre = pedir_texto("Nombre del país a actualizar: ")
    pais = buscar_exacto(paises, nombre)

    if pais is None:
        print(f"[ERROR] No se encontró el país '{nombre}'")
        return
    
    print(f"Datos actuales → Población: {pais['poblacion']:,} | Superficie: {pais['superficie']:,} km²")

    pais["poblacion"] = pedir_entero("Nueva Población: ", minimo = 1 )
    pais["superficie"] = pedir_entero("Nueva Superficie: ", minimo = 1)
    print("[OK] Datos actualizados correctamente.")

def buscar_pais(paises: list) -> None:
    """ Busca países con coincidencia parcial o exacta """
    print("\n --- BUSCAR PAÍS ---")
    termino = pedir_texto("Ingresa el nombre del país o parte de el: ").lower()
    resultados = []
    for p in paises:
        if termino in p["nombre"].lower():
            resultados.append(p)
    
    if not resultados:
        print("[INFO] No se encontraron coincidencias.")
    else:
        print(f"\n{len(resultados)} resultado(s) encontrado(s):")
        mostrar_tabla(resultados)

#---- FILTROS ----

def filtrar_paises(paises: list) -> None:
    """ Submenú de filtros. """
    print("\n --- FILTRAR PAISES ---")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        _filtrar_por_continente(paises)
    elif opcion == "2":
        _filtrar_por_rango(paises, campo="poblacion", unidad="habitantes")
    elif opcion == "3":
        _filtrar_por_rango(paises, campo="superficie", unidad="km²")
    else:
        print("[ERROR] Opción no válida.")

def _filtrar_por_continente(paises):
    continente = pedir_texto("Ingrese el continente").lower()
    resultados = []
    for p in paises:
        if continente == p["continente"].lower():
            resultados.append(p)
    _mostrar_resultado(resultados, f"continente '{continente.title()}'")

def _filtrar_por_rango(paises: list, campo: str, unidad: str) -> None:
    print(f"Ingrese el rango de {campo} en {unidad}")
    minimo = pedir_entero(" Minimo: ", minimo = 0)
    maximo = pedir_entero(" Máximo", minimo = 0)
    if minimo > maximo:
        print("[ERROR] El mínimo no puede ser mayor que el máximo.")
        return
    resultados = []
    for p in paises:
        if minimo <= p[campo] <= maximo:
            resultados.append(p)
    _mostrar_resultado(resultados, f"{campo} entre {minimo:,} y {maximo:,} {unidad}")

#---- ORDENAMIENTOS ----

def ordenar_paises(paises: list) -> None:
    """ Submenú de ordenamiento """
    print("\n --- ORDENAR PAÍSES ---")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    opcion = input("Opción: ").strip()

    campos_map = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in campos_map:
        print("[ERROR] Opción no válida.")
        return
 
    campo = campos_map[opcion]
    if opcion != "1":
        direccion = input("¿Orden ascendente o descendente? (a/d): ").strip().lower()
        descendente = (direccion == "d")
    else:
        descendente = False
    
    def obtener_valor(p):
        return p[campo]
    
    ordenados = sorted(paises, key=obtener_valor, reverse=descendente)
    orden_texto = "descendente" if descendente else "ascendente"
    print(f"\nPaíses ordenados por {campo} ({orden_texto}):")
    _mostrar_tabla(ordenados)

#---- ORDENAMIENTOS ----


#---------------------------------------------------------
#       FUNCIONES DE PRESENTACIÓN
#---------------------------------------------------------

def buscar_exacto(paises: list, nombre: str) -> None:
    """ Retorna el diccionario con el país buscado """
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            return p
    return None
