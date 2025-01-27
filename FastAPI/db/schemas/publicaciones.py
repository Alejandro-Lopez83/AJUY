
from db.schemas.utilidades_schemas.utilidad_schema import autores_schema



def publicacion_schema(publicacion) -> dict:
    return {"id": publicacion["_id"].__str__(), 
            "Título": publicacion["Título"], 
            "Autores": autores_schema(publicacion["Autores"]),
            "Clasificación_UNESCO": publicacion["Clasificación_UNESCO"],
            "Colección": publicacion["Colección"],
            "DOI": publicacion["DOI"],
            "Fecha_de_publicación": publicacion["Fecha_de_publicación"],
            "Fuente": publicacion["Fuente"],
            "ISSN": publicacion["ISSN"],
            "Palabras_clave": publicacion["Palabras_clave"],
            "PDF": publicacion["PDF"],
            "Resumen": publicacion["Resumen"],
            "URI": publicacion["URI"]}

def publicaciones_schema(publicaciones) -> list[dict]:
    return [publicacion_schema(publicacion) for publicacion in publicaciones]

