import os
from pymongo import MongoClient

# Obtener la variable de entorno directamente
mongodb_url = ("mongodb+srv://alopma83:1234@cluster0.anxmn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Manejar el caso en que no esté configurada
if not mongodb_url:
    raise ValueError("La variable de entorno 'MONGODB_URL' no está configurada.")

# Crear el cliente de MongoDB
db_client = MongoClient(mongodb_url).Proyecto

""" db_client = MongoClient().Proyecto """