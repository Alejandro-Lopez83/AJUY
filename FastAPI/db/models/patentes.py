from pydantic import BaseModel

class Patente(BaseModel):
    id: str
    Título: str
    Autores: list[str]
    Colección: str | None
    Fecha_de_publicación: str | None
    PDF: str | None
    Resumen: str | None
    URI: str | None
    URL: str | None
   
