from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.session import SessionLocal, engine
from models.db_models import Base
from schemas.vuelos import Vuelo, VueloCreate, EstadoVuelo
from crud.vuelos import crear_vuelo, listar_vuelos, obtener_vuelo, eliminar_vuelo
from models.lista_vuelos import ListaVuelos

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar lista de vuelos
lista_vuelos = None

@app.on_event("startup")
def startup_event():
    global lista_vuelos
    db = SessionLocal()
    lista_vuelos = ListaVuelos(db)
    # Cargar vuelos existentes de la base de datos
    vuelos_db = listar_vuelos(db)
    for vuelo in vuelos_db:
        lista_vuelos.insertar_al_final(vuelo)
    db.close()

@app.post("/vuelos/", response_model=Vuelo)
def crear_vuelo_endpoint(vuelo: VueloCreate, db: Session = Depends(get_db)):
    db_vuelo = crear_vuelo(db, vuelo)
    # Insertar en la lista según el estado
    if vuelo.estado == EstadoVuelo.emergencia:
        lista_vuelos.insertar_al_frente(db_vuelo)
    else:
        lista_vuelos.insertar_al_final(db_vuelo)
    return db_vuelo

@app.get("/vuelos/total", response_model=int)
def obtener_total_vuelos():
    return lista_vuelos.longitud()

@app.get("/vuelos/proximo", response_model=Vuelo)
def obtener_proximo_vuelo():
    vuelo = lista_vuelos.obtener_primero()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos programados")
    return vuelo

@app.get("/vuelos/ultimo", response_model=Vuelo)
def obtener_ultimo_vuelo():
    vuelo = lista_vuelos.obtener_ultimo()
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos programados")
    return vuelo

@app.post("/vuelos/insertar", response_model=Vuelo)
def insertar_vuelo_posicion(vuelo: VueloCreate, posicion: int, db: Session = Depends(get_db)):
    db_vuelo = crear_vuelo(db, vuelo)
    lista_vuelos.insertar_en_posicion(db_vuelo, posicion)
    return db_vuelo

@app.delete("/vuelos/extraer", response_model=Vuelo)
def extraer_vuelo_posicion(posicion: int, db: Session = Depends(get_db)):
    try:
        vuelo = lista_vuelos.extraer_de_posicion(posicion)
        eliminar_vuelo(db, vuelo.id)
        return vuelo
    except IndexError:
        raise HTTPException(status_code=400, detail="Posición inválida")

@app.get("/vuelos/lista", response_model=List[Vuelo])
def listar_todos_vuelos():
    return lista_vuelos.listar_vuelos()

@app.patch("/vuelos/reordenar")
def reordenar_vuelos(posicion_origen: int, posicion_destino: int):
    try:
        lista_vuelos.reordenar_vuelos(posicion_origen, posicion_destino)
        return {"mensaje": "Vuelos reordenados correctamente"}
    except IndexError:
        raise HTTPException(status_code=400, detail="Posiciones inválidas")