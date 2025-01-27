from db.schemas.utilidades_schemas.utilidad_schema import autores_schema


def tesi_schema(tesi) -> dict:
    return {"id": tesi["_id"].__str__(), 
            "Título": tesi["Título"], 
            "Autores": autores_schema(tesi["Autores"]),
            "Director": autores_schema(tesi["Director/a"]),
            "Clasificación_UNESCO": tesi["Clasificación_UNESCO"],
            "Colección": tesi["Colección"],
            "Departamento": tesi["Departamento"],
            "Descripción": tesi["Descripción"],
            "Fecha_de_publicación": tesi["Fecha_de_publicación"],
            "Palabras_clave": tesi["Palabras_clave"],
            "PDF": tesi["PDF"],
            "Resumen": tesi["Resumen"],
            "URI": tesi["URI"]}

def tesis_schema(tesis) -> list[dict]:
    return [tesi_schema(tesi) for tesi in tesis]
