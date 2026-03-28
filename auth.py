import urllib.request
import urllib.parse
import json
import webbrowser

from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event

# -> permisos dados por el usuario, write -> en este caso solo para disparar la traducción de rvt a svf2
PERMISOS = "data:read data:write data:search viewables:read"

TIEMPO_DE_ESPERA_PARA_EL_PERMISO = 300


def obtener_token(client_id, client_secret, url_callback, url_base):

    url_para_logeo_y_autorizacion = (f"{url_base}/authentication/v2/authorize?response_type=code&client_id={client_id}&redirect_uri={url_callback}&scope={urllib.parse.quote(PERMISOS)}")

    # -> para el do_GET()
    info_de_autorizacion_temporal = {} # -> guarda el codigo que pasa el handler
    evento_disparador_del_codigo  = Event()  # -> avisa que se obtuvo el codigo

    class Handler(BaseHTTPRequestHandler):
        # -> lo que hace el handler cuando llega la petición GET
        def do_GET(self):
            # -> datos que envía Autodesk
            datos_crudos_para_autenficacion = urllib.parse.urlparse(self.path).query

            datos_estructurados_para_autentificacion = urllib.parse.parse_qs(datos_crudos_para_autenficacion)

            if "code" in datos_estructurados_para_autentificacion:
                info_de_autorizacion_temporal["code"] = datos_estructurados_para_autentificacion["code"][0]

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"autentificacion y permiso OK")
                
                evento_disparador_del_codigo.set() # -> se dispara el evento que indica que ya se tiene el codigo de autorización temporal

                Thread(target=self.server.shutdown).start() # -> hilo nuevo para apagar localhost:8080
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"error no se obtuvo ningun codigo")

    server = HTTPServer(("localhost", 8080), Handler)

    # -> hilo para sostener el localhost indefinidamente
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    print(f"tiempo de espera para dar el permiso -> {TIEMPO_DE_ESPERA_PARA_EL_PERMISO}s")

    webbrowser.open(url_para_logeo_y_autorizacion)

    # -> true si el disparador es llamado antes del tiempo de espera
    recibido = evento_disparador_del_codigo.wait(timeout=TIEMPO_DE_ESPERA_PARA_EL_PERMISO)

    if not recibido or not info_de_autorizacion_temporal.get("code"):
        server.shutdown()
        raise RuntimeError(
            f"no se obtuvo el código en el tiempo de espera= {TIEMPO_DE_ESPERA_PARA_EL_PERMISO}s")

    # -> código de permiso temporal
    codigo_de_autorizacion_temporal = info_de_autorizacion_temporal["code"]

    # -> petición del token a Autodesk
    payload = (f"grant_type=authorization_code&code={codigo_de_autorizacion_temporal}&client_id={client_id}&client_secret={client_secret}&redirect_uri={url_callback}") # -> mensaje

    req = urllib.request.Request(f"{url_base}/authentication/v2/token", data=payload.encode(), headers={"Content-Type":"application/x-www-form-urlencoded"},) # -> POST request como tal

    token = json.loads(urllib.request.urlopen(req).read())["access_token"] # -> access_token -> credencial temporal

    return token