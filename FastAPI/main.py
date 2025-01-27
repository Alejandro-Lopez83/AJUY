from fastapi import FastAPI
from routers import autores_db, publicaciones_db, tesis_db, proyecto_db, patentes_db
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() 
app.include_router(autores_db.router)
app.include_router(publicaciones_db.router)
app.include_router(tesis_db.router)
app.include_router(proyecto_db.router)
app.include_router(patentes_db.router)
add_pagination(app) 

#Inicia el server: uvicorn main:app --reload


# Configuración de los orígenes permitidos
origins = ["*"]  # Permitir todos los orígenes. Cambia esto para mayor seguridad.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,  # Permitir cookies o credenciales (opcional)
    allow_methods=["*"],  # Métodos permitidos (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Headers permitidos en las solicitudes
)

@app.get("/")
def read_root():
    return {"message": "CORS configurado correctamente"}

