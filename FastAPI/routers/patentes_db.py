from fastapi import APIRouter, status
from bson import ObjectId
from db.schemas.patentes import patentes_schema, patente_schema
from db.client import db_client
from db.models.patentes import Patente
from fastapi_pagination import Page, paginate



router = APIRouter(prefix="/patentes", 
                   tags=["patentes"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado 123"}})

""" #Encuentra Patente por id patente
@router.get("/{id}", response_model=Patente) 
async def patentes(id: str) -> Patente:
    return patente_schema(db_client.patentes.find_one()) """

# Cuenta todas las patentes
@router.get("/count", response_model=int)
async def count_patentes():
    count = db_client.Proyecto.patentes.count_documents({})
    return count


@router.get("/{id}", response_model=Patente) 
async def patentes(id: str) -> Patente:
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$lookup": {
            "from": "autores",
            "localField": "Autores",
            "foreignField": "_id",
            "as": "Autores"
        }}
    ]
    patente = db_client.Proyecto.patentes.aggregate(pipeline).next()
    return patente_schema(patente)


#Encuentra Patente por id autor
@router.get("/autor/{id}", response_model= Page[Patente])
async def patentes(id: str) -> Page[Patente]:
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
    patentes = list(db_client.Proyecto.patentes.aggregate(pipeline))
    return paginate(patentes_schema(patentes))
