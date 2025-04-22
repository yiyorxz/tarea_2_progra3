from sqlalchemy.orm import Session
from models.db_models import DBVuelo
from models.lista_vuelos import ListaVuelos

def crear_vuelo(db: Session, vuelo):
    db_vuelo = DBVuelo(**vuelo.dict())
    db.add(db_vuelo)
    db.commit()
    db.refresh(db_vuelo)
    return db_vuelo

def obtener_vuelo(db: Session, vuelo_id: int):
    return db.query(DBVuelo).filter(DBVuelo.id == vuelo_id).first()

def listar_vuelos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBVuelo).offset(skip).limit(limit).all()

def eliminar_vuelo(db: Session, vuelo_id: int):
    db_vuelo = db.query(DBVuelo).filter(DBVuelo.id == vuelo_id).first()
    if db_vuelo:
        db.delete(db_vuelo)
        db.commit()
        return True
    return False