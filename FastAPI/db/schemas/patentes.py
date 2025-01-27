
from db.schemas.utilidades_schemas.utilidad_schema import autores_schema

def patente_schema(patente) -> dict:
    return {"id": patente["_id"].__str__(), 
            "Título": patente["Título"], 
            "Autores": autores_schema(patente["Autores"]),
            "Colección": patente["Colección"],
            "Fecha_de_publicación": patente["Fecha_de_publicación"],
            "PDF": patente["PDF"],
            "Resumen": patente["Resumen"],
            "URI": patente["URI"],
            "URL": patente["URL"]}
            

def patentes_schema(patentes) -> list[dict]:
    return [patente_schema(patente) for patente in patentes]
