from db.schemas.utilidades_schemas.utilidad_schema import autores_schema


def proyecto_schema(proyecto) -> dict:
    return {"id": proyecto["_id"].__str__(), 
            "Título": proyecto["Título"], 
            "Investigadores": autores_schema(proyecto["Investigadores"]),
            "fecha_de_inicio": proyecto["Fecha de inicio"],
            "organismo_financiador": proyecto["Organismo Financiador"],
            "Referencia": proyecto["Referencia"],
            "Tipo": proyecto["Tipo"],
            "URL_del_proyecto": proyecto["URL del Proyecto"]}
            

def proyectos_schema(proyectos) -> list[dict]:
    return [proyecto_schema(proyecto) for proyecto in proyectos]
