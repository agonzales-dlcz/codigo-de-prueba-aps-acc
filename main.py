import os
from dotenv import load_dotenv

from auth import obtener_token
from aps import agente_aps
from iterador import encontrar_todos_los_modelos
from extractor import acumular_filas, guardar_csv

# -> lee info de .env
load_dotenv()

CLIENT_ID = os.getenv("APS_CLIENT_ID")
CLIENT_SECRET = os.getenv("APS_CLIENT_SECRET")
CALLBACK_URL = os.getenv("APS_CALLBACK_URL")
BASE_URL = "https://developer.api.autodesk.com"

PATH_DE_CARPETA_DE_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".", "resultados")


def main():
    # 1 -> autentificación 3-legged -> credenciales temporales
    token = obtener_token(CLIENT_ID, CLIENT_SECRET, CALLBACK_URL, BASE_URL)
    # print("autentificación 3-legged OK\n")

    agente = agente_aps(token, BASE_URL)

    # 2 -> buscar todos los .rvt con traducción svf2 terminada en todos los hubs/proyectos/carpetas/subcarpetas
    lista_de_modelos = encontrar_todos_los_modelos(agente)

    if not lista_de_modelos:
        print("\n-> no hay modelos con traducción svf2 terminada para leer")
        return

    print(f"\n-> {len(lista_de_modelos)} modelo(s) listos para leer\n")

    filas_acumuladas = [] # -> acumula filas de todos los modelos antes de escribir el csv

    for urn_modelo, nombre_modelo in lista_de_modelos:
        print(f"leyendo {nombre_modelo} ...")

        # 3 -> obtener guid de la primera vista 3d
        metadata_del_modelo = agente.get(f"/modelderivative/v2/designdata/{urn_modelo}/metadata")
        lista_de_vistas = metadata_del_modelo["data"]["metadata"]

        if not lista_de_vistas: # -> sin vistas disponibles -> omitir
            print(f"{nombre_modelo} -> sin vistas disponibles, omitido")
            continue

        vista_3d = next((metadata_de_vista for metadata_de_vista in lista_de_vistas if metadata_de_vista.get("role") == "3d"), lista_de_vistas[0]) # -> retorna el primer 3d, si no hay la primera vista en general
        guid_vista_3d = vista_3d["guid"]

        # 4 -> descargar collection de elementos de la vista
        colector_de_elementos = agente.obtener_colector_de_la_vista(urn_modelo, guid_vista_3d)

        if not colector_de_elementos: # -> colección vacía -> omitir
            print(f"{nombre_modelo} -> colección vacía, omitido")
            continue

        # 5 -> acumular filas del modelo en la lista compartida
        nombre_modelo_sin_extension = nombre_modelo.split(".")[0] # -> sin .rvt
        acumular_filas(colector_de_elementos, nombre_modelo_sin_extension, filas_acumuladas)

    # 6 -> escribir csv único con todos los modelos y abrirlo
    if filas_acumuladas:
        guardar_csv(filas_acumuladas, carpeta_de_salida=PATH_DE_CARPETA_DE_SALIDA)
    else:
        print("\n-> no se acumularon elementos para guardar")

if __name__ == "__main__":
    main()
