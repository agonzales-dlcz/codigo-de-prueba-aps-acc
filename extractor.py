import os
from datetime import datetime

# -> lista de parámetros a leer
PARAMETROS = [
    "IfcGUID",
    "Type Name",
    "Level",
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


def _lista_de_lineas(elementos: list) -> list[str]:
    encabezado_de_tabla_de_resultados = ["Id"] + PARAMETROS
    lista_de_lineas_tabuladas = ["\t".join(encabezado_de_tabla_de_resultados)]

    for elemento in elementos:
        id_objeto = str(elemento.get("objectid", "")) # -> Id o vacío
        diccionario_de_parametros = leer_parametros(elemento)
        linea_de_valores  = [id_objeto] + [diccionario_de_parametros[parametro] for parametro in PARAMETROS]
        lista_de_lineas_tabuladas.append("\t".join(linea_de_valores))

    return lista_de_lineas_tabuladas


def guardar_txt(colector_de_elementos: list, nombre_de_modelo: str = "", carpeta_de_salida: str = "."):
    os.makedirs(carpeta_de_salida, exist_ok=True) # -> crea carpeta si no existe

    nombre_modelo_corregido = (nombre_de_modelo or "modelo").replace(" ", "_").replace("/", "-").split(".")[0] # -> nombre sin extensión .rvt
    hora_minuto_segundo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_de_txt = f"{nombre_modelo_corregido}_{hora_minuto_segundo}.txt"
    ruta_para_guardar_txt = os.path.join(carpeta_de_salida, nombre_de_txt)

    lista_de_lineas_para_el_txt = _lista_de_lineas(colector_de_elementos) # -> contenido, listado de parametros y valores de todos los elementos

    # -> crea y escribe txt
    with open(ruta_para_guardar_txt, "w", encoding="utf-8") as f:
        for linea in lista_de_lineas_para_el_txt:
            f.write(linea + "\n")

    print(f"archivo {nombre_de_txt} guardado OK")

    return ruta_para_guardar_txt