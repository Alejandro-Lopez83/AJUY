

def autor_schema(autor) -> dict:
    return {"id": autor["_id"].__str__(), 
            "Nombre": autor["Nombre"], 
            "Email": autor["Email"]}

def autores_schema(autores) -> list[dict]:
    return [autor_schema(autor) for autor in autores]
