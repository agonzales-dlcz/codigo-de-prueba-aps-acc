import base64


def obtener_estado_de_traduccion(agente, urn: str):
    try:
        info_de_traduccion = agente.get(f"/modelderivative/v2/designdata/{urn}/manifest")
        return info_de_traduccion.get("status")
    except:
        return None  # -> no hay traducción


def disparar_traduccion(agente, urn: str) -> bool:
    try:
        agente.post("/modelderivative/v2/designdata/job", {"input":{"urn":urn}, "output":{"formats":[{"type":"svf2", "views":["3d"]}]}, })
        return True
    except:
        return False


def _construir_urn(agente, proyecto_id: str, item: dict): # -> método privado
    try:
        historial_de_versiones_del_agente = agente.get(f"/data/v1/projects/{proyecto_id}/items/{item['id']}/versions")["data"]
        
        ultima_version = historial_de_versiones_del_agente[0]

        ultima_version_id_crudo = ultima_version.get("relationships", {}).get("storage", {}).get("data", {}).get("id", "")

        if ultima_version_id_crudo:
            return base64.urlsafe_b64encode(ultima_version_id_crudo.encode()).rstrip(b"=").decode() # -> urn en bytes

        ultima_version_id_traducida = ultima_version.get("relationships", {}).get("derivatives", {}).get("data", {}).get("id", "")
        
        if ultima_version_id_traducida:
            return base64.urlsafe_b64encode(ultima_version_id_traducida.encode()).rstrip(b"=").decode() # -> urn en bytes

    except:
        pass

    return None


def iterar_modelos(agente, proyecto_id: str, carpeta_id: str):

    try:
        contenido_de_carpeta = agente.get(f"/data/v1/projects/{proyecto_id}/folders/{carpeta_id}/contents")["data"]
    except:
        return None, None

    for item in contenido_de_carpeta:
        tipo_del_item   = item.get("type", "")
        indice_de_atributos  = item.get("attributes", {})

        nombre_del_item = ( indice_de_atributos.get("name") or indice_de_atributos.get("displayName") or indice_de_atributos.get("fileName") or "")

        if tipo_del_item == "items" and nombre_del_item.lower().endswith(".rvt"): # es "items" -> archivo y es .rvt
            urn_rvt = _construir_urn(agente, proyecto_id, item)
            if not urn_rvt:
                continue

            estado = obtener_estado_de_traduccion(agente, urn_rvt)

            if estado in ("success", "complete"):
                return urn_rvt, nombre_del_item

            elif estado in ("inprogress", "pending"):
                print(f"{nombre_del_item} -> traducción en proceso")
                continue

            else:
                traduccion_disparada = disparar_traduccion(agente, urn_rvt)
                if traduccion_disparada:
                    print(f"{nombre_del_item} -> traducción iniciada")
                else:
                    print(f"{nombre_del_item} -> error al iniciar traducción")
                continue

    return None, None


def encontrar_primer_modelo(agente):
    lista_de_hubs = agente.get("/project/v1/hubs")["data"]

    for hub in lista_de_hubs:
        hub_id = hub["id"]
        lista_de_proyectos = agente.get(f"/project/v1/hubs/{hub_id}/projects")["data"]

        for proyecto in lista_de_proyectos:
            proyecto_id = proyecto["id"]
            lista_de_carpetas = agente.get(f"/project/v1/hubs/{hub_id}/projects/{proyecto_id}/topFolders")["data"]

            for carpeta in lista_de_carpetas:
                urn_rvt, nombre_rvt = iterar_modelos(agente, proyecto_id, carpeta["id"])
                if urn_rvt:
                    return urn_rvt, nombre_rvt

    return None, None