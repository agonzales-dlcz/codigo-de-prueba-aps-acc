import os
from dotenv import load_dotenv

from auth import obtener_token
from aps import agente_aps
from iterador import encontrar_primer_modelo
from extractor import guardar_txt

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

    # 2 -> buscar primer rvt con traducción svf2 terminada
    urn_modelo, nombre_modelo = encontrar_primer_modelo(agente)

    if not urn_modelo:
        print("\n-> no hay modelos con traducción svf2 terminada para leer")
        return

    print(f"{nombre_modelo} -> OK\n")

    # 3 -> obtener guid de la primera vista 3d
    metadata_del_modelo = agente.get(f"/modelderivative/v2/designdata/{urn_modelo}/metadata")
    lista_de_vistas = metadata_del_modelo["data"]["metadata"]
    vista_3d = next((metadata_de_vista for metadata_de_vista in lista_de_vistas if metadata_de_vista.get("role") == "3d"), lista_de_vistas[0]) # -> retorna el primer 3d, si no hay la primera vista en general
    guid_vista_3d = vista_3d["guid"]

    # 4 -> descargar collection de elementos de la vista
    colector_de_elementos = agente.obtener_colector_de_la_vista(urn_modelo, guid_vista_3d)

    # 5 -> guardar txt de salida
    guardar_txt(colector_de_elementos, nombre_de_modelo=nombre_modelo, carpeta_de_salida=PATH_DE_CARPETA_DE_SALIDA)

if __name__ == "__main__":
    main()