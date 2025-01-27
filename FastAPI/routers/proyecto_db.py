from fastapi import APIRouter, status
from bson import ObjectId
from db.schemas.proyectos import proyectos_schema, proyecto_schema
from db.client import db_client
from db.models.proyectos import Proyecto
from fastapi_pagination import Page, paginate



router = APIRouter(prefix="/proyectos", 
                   tags=["proyectos"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado 123"}})


# Cuenta todos los proyectos
@router.get("/count", response_model=int)
async def count_proyectos():
    count = db_client.Proyecto.proyectos.count_documents({})
    return count


#Encuentra proyecto por id proyecto
@router.get("/{id}", response_model=Proyecto) 
async def proyectos(id: str) -> Proyecto:
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$lookup": {
            "from": "autores",
            "localField": "Investigadores",
            "foreignField": "_id",
            "as": "Investigadores"
        }}
    ]
    proyecto = db_client.Proyecto.proyectos.aggregate(pipeline).next()
    return proyecto_schema(proyecto)

#Encuentra proyectos por id investigador
@router.get("/autor/{id}", response_model=Page[Proyecto]) 
async def proyectos(id: str) -> Page[Proyecto]:
    pipeline = [
            {"$match": {"Investigadores": ObjectId(id)}},
            {"$lookup": {
                "from": "autores",
                "localField": "Investigadores",
                "foreignField": "_id",
                "as": "Investigadores"
            }},
            {"$sort": {"Título": 1, "_id": 1}}
        ]
    proyectos = list(db_client.Proyecto.proyectos.aggregate(pipeline))
    return paginate(proyectos_schema(proyectos))
