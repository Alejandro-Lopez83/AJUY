from fastapi import APIRouter, status
from bson import ObjectId
from db.schemas.publicaciones import publicaciones_schema, publicacion_schema
from db.client import db_client
from db.models.publicaciones import Publicacion
from fastapi_pagination import Page, paginate



router = APIRouter(prefix="/publicaciones", 
                   tags=["publicaciones"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado 123"}})


# Cuenta todas las publicaciones
@router.get("/count", response_model=int)
async def count_publicaciones():
    count = db_client.Proyecto.publicaciones.count_documents({})
    return count


#Encuentra publicacion por id publicacion
@router.get("/{id}", response_model=Publicacion) 
async def publicaciones(id: str) -> Publicacion:
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$lookup": {
            "from": "autores",
            "localField": "Autores",
            "foreignField": "_id",
            "as": "Autores"
        }}
    ]
    publicacion = db_client.Proyecto.publicaciones.aggregate(pipeline).next()
    return publicacion_schema(publicacion)

@router.get("/autor/{id}", response_model= Page[Publicacion])
async def publicaciones(id: str) -> Page[Publicacion]:
    pipeline = [
            {"$match": {"Autores": ObjectId(id)}},
            {"$lookup": {
                "from": "autores",
                "localField": "Autores",
                "foreignField": "_id",
                "as": "Autores"
            }},
            {"$sort": {"Título": 1, "_id": 1}}
        ]
    publicaciones = list(db_client.Proyecto.publicaciones.aggregate(pipeline))
    return paginate(publicaciones_schema(publicaciones))


