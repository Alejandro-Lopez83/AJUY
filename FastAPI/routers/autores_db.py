from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from db.schemas.autores import autores_schema, autor_schema
from db.client import db_client
from db.models.autores import Autor
from fastapi_pagination import Page, paginate




router = APIRouter(prefix="/autores", 
                   tags=["autores"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


# Encuentra todos los autores
@router.get("/", response_model=Page[Autor]) 
async def autores() -> Page[Autor]:
    return paginate(autores_schema(db_client.Proyecto.autores.find({}).sort({"Nombre": 1, "_id": 1}).to_list()))

# Cuenta todos los autores
@router.get("/count", response_model=int)
async def count_autores():
    count = db_client.Proyecto.autores.count_documents({})
    return count

# Encuentra un autor por du id
@router.get("/{id}", response_model=Autor)
async def autor(id: str):
    return autor_schema(db_client.Proyecto.autores.find_one({"_id": ObjectId(id)}))

