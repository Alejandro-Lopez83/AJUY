from fastapi import APIRouter, status
from bson import ObjectId
from db.schemas.tesis import tesis_schema, tesi_schema
from db.client import db_client
from db.models.tesis import Tesis
from fastapi_pagination import Page, paginate



router = APIRouter(prefix="/tesis", 
                   tags=["tesis"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado 123"}})


# Cuenta todas las tesis
@router.get("/count", response_model=int)
async def count_tesis():
    count = db_client.Proyecto.tesis.count_documents({})
    return count

# Encuentra tesis por id tesis
@router.get("/{id}", response_model=Tesis) 
async def tesis(id: str) -> Tesis:
    pipeline = [
        {"$match": {"_id": ObjectId(id)}},
        {"$lookup": {
            "from": "autores",
            "localField": "Autores",
            "foreignField": "_id",
            "as": "Autores"
        }},
        {"$lookup": {
            "from": "autores",
            "localField": "Director/a",
            "foreignField": "_id",
            "as": "Director/a"
        }}
    ]
    tesis = db_client.Proyecto.tesis.aggregate(pipeline).next()
    return tesi_schema(tesis)

# Encuentra tesis por id autor
@router.get("/autor/{id}", response_model=Page[Tesis])
async def tesis(id: str) -> Page[Tesis]:
    pipeline = [
        {"$match": {"$or": [{"Autores": ObjectId(id)}, {"Director/a": ObjectId(id)}]}},
        {"$lookup": {
            "from": "autores",
            "localField": "Autores",
            "foreignField": "_id",
            "as": "Autores"
        }},
        {"$lookup": {
            "from": "autores",
            "localField": "Director/a",
            "foreignField": "_id",
            "as": "Director/a"
        }},
        {"$sort": {"Título": 1, "_id": 1}}
    ]
    tesis = list(db_client.Proyecto.tesis.aggregate(pipeline))
    return paginate(tesis_schema(tesis))