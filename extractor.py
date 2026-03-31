import os
import csv
import subprocess
import sys
from datetime import datetime

# -> lista de parámetros a leer
PARAMETROS = [
    "CSRT-Partida1",
    "CSRT-DescripcionPartida1",
    "CSRT-Bloque",
    "CSRT-Nivel",
    "CSRT-Unidad1",
    "CSRT-FechaInicia1",
    "CSRT-FechaFin1",
    "CSRT-ProtocoloCalidad1",
    "CSRT-FechaAprobacionProtocolo1",
]

def leer_parametros(elemento: dict) -> dict:
    diccionario_de_parametros = {parametro: "" for parametro in PARAMETROS}
    propiedades = elemento.get("properties", {}) # -> obtener propiedades sino vacío

    for grupo_de_propiedades in propiedades.values():
        if not isinstance(grupo_de_propiedades, dict): # -> si el grupo_de_propiedades no es diccionario
            continue
        for parametro in PARAMETROS:
            if parametro in grupo_de_propiedades and diccionario_de_parametros[parametro] == "": # -> parámetro encontrado y aún no asignado → guardar primer valor
                diccionario_de_parametros[parametro] = str(grupo_de_propiedades[parametro])

    return diccionario_de_parametros


def _leer_ifc_guid(elemento: dict) -> str:
    # -> busca IfcGUID en cualquier grupo de propiedades -> identificador persistente del elemento
    propiedades = elemento.get("properties", {})
    for grupo_de_propiedades in propiedades.values():
        if isinstance(grupo_de_propiedades, dict) and "IfcGUID" in grupo_de_propiedades:
            return str(grupo_de_propiedades["IfcGUID"])
    return "" # -> si no tiene IfcGUID retorna vacío


def acumular_filas(colector_de_elementos: list, nombre_de_modelo: str, filas_acumuladas: list):
    # -> agrega las filas del modelo a la lista compartida, sin escribir archivo todavía

    for elemento in colector_de_elementos:
        ifc_guid = _leer_ifc_guid(elemento)
        diccionario_de_parametros = leer_parametros(elemento)
        fila = [nombre_de_modelo, ifc_guid] + [diccionario_de_parametros[parametro] for parametro in PARAMETROS]
        filas_acumuladas.append(fila)


def guardar_csv(filas_acumuladas: list, carpeta_de_salida: str = "."):
    os.makedirs(carpeta_de_salida, exist_ok=True) # -> crea carpeta si no existe

    hora_minuto_segundo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_de_csv = f"extraccion_{hora_minuto_segundo}.csv"
    ruta_para_guardar_csv = os.path.join(carpeta_de_salida, nombre_de_csv)

    encabezado = ["Modelo", "IfcGUID"] + PARAMETROS

    # -> crea y escribe csv con separador tab -> una celda por columna al abrir en Excel
    with open(ruta_para_guardar_csv, "w", encoding="utf-8-sig", newline="") as f: # -> utf-8-sig para que Excel lo abra bien
        escritor = csv.writer(f, delimiter="\t")
        escritor.writerow(encabezado)
        for fila in filas_acumuladas:
            escritor.writerow(fila)

    print(f"\narchivo {nombre_de_csv} guardado OK -> {len(filas_acumuladas)} elementos")

    # -> abrir el csv al terminar según el sistema operativo
    if sys.platform == "win32":
        os.startfile(ruta_para_guardar_csv)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", ruta_para_guardar_csv])
    else:
        subprocess.Popen(["xdg-open", ruta_para_guardar_csv])

    return ruta_para_guardar_csv
