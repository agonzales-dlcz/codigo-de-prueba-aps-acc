import urllib.request
import json
import gzip

# -> agente_aps -> como el personaje de un juego -> puede hacer cosas (métodos) y tiene y puede cambiar de 'estados' (información)

class agente_aps:
    
    # -> constructor/instanciador de la clase 'agente_aps'
    def __init__(self, token: str, base_url: str):
        self.token = token
        self.base_url = base_url

    # METODOS

    # -> metodo GET, pide datos al path dado
    def get(self, path: str) -> dict:
        req = urllib.request.Request(f"{self.base_url}{path}", headers={"Authorization": f"Bearer {self.token}"}, ) # -> request

        return json.loads(urllib.request.urlopen(req).read()) # -> resultado en json

    # -> metodo POST, manda y pide datos al path dado
    def post(self, path: str, body: dict) -> dict:
        mensaje = json.dumps(body).encode() # -> mensaje a Autodesk en bytes

        req  = urllib.request.Request(f"{self.base_url}{path}", data=mensaje, headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json", }, ) # -> request

        return json.loads(urllib.request.urlopen(req).read()) # -> resultado en json


    # -> descomprime la respuesta si está comprimida
    @staticmethod # -> metodo estático
    def _descomprimir(data: bytes) -> bytes: # -> metodo privado
        if data[:2] == b"\x1f\x8b": return gzip.decompress(data) # -> si data es gzip -> descomprimir
        return data # -> sino lo devuelve igual

    # -> colección de elementos de la vista por guid del modelo por urn
    def obtener_colector_de_la_vista(self, urn: str, guid: str) -> list:
        
        url = (f"{self.base_url}/modelderivative/v2/designdata/{urn}/metadata/{guid}/properties?forceget=true") # -> instruccion de forzar la lectura de datos de elementos de la vista en cuestión

        req = urllib.request.Request(url, headers={ "Authorization":f"Bearer {self.token}", "Accept-Encoding":"gzip", }, ) # -> requerimiento
        
        try:
            with urllib.request.urlopen(req) as respuesta: # -> respuesta
                datos_crudos  = self._descomprimir(respuesta.read())
                datos_estructurados = json.loads(datos_crudos)

                # -> DESCARGAR COLECCIÓN DE ELEMENTOS DE MODELOS PEQUEÑOS -> directo de 'collection'
                if "data" in datos_estructurados and "collection" in datos_estructurados.get("data", {}):
                    return datos_estructurados["data"]["collection"]

                # -> DESCARGAR COLECCIÓN DE ELEMENTOS DE MODELOS GRANDES -> de un link externo
                if "data" in datos_estructurados and "url" in datos_estructurados.get("data", {}):
                    url_externo = datos_estructurados["data"]["url"] # -> dirección para descargar los datos
                    
                    req2 = urllib.request.Request(url_externo, headers={"Authorization": f"Bearer {self.token}"}, ) # -> requerimiento de descarga de JSON

                    # -> envío y respuesta
                    with urllib.request.urlopen(req2) as respuesta_link_externo:
                        datos_crudos_del_link_externo  = self._descomprimir(respuesta_link_externo.read())

                        datos_estructurados_del_link_externo = json.loads(datos_crudos_del_link_externo)

                        return datos_estructurados_del_link_externo.get("data", {}).get("collection", []) # -> propiedades desde 'collection'

        except urllib.error.HTTPError as e:
            print(f"{e.code} - {e.read().decode()[:200]}")

        return [] # -> si falla el try retorna vacío
