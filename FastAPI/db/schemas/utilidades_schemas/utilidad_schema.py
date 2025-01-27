
def autores_schema(autores_id) -> list[str]:
    return [autor_id.__str__() for autor_id in autores_id]
