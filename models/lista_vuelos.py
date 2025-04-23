# models/lista_vuelos.py
from models.nodo import Nodo
from sqlalchemy.orm import Session
from models.db_models import DBVuelo

class ListaVuelos:
    def __init__(self, db_session: Session):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
        self.session = db_session
    
    def actualizar_posiciones_db(self):
        """Actualiza todas las posiciones en la base de datos según el orden actual"""
        actual = self.cabeza
        posicion = 0
        while actual is not None:
            vuelo_db = self.session.query(DBVuelo).filter(DBVuelo.id == actual.vuelo.id).first()
            if vuelo_db:
                vuelo_db.posicion = posicion
            posicion += 1
            actual = actual.siguiente
        self.session.commit()
    
    def insertar_al_frente(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamano += 1
        self.actualizar_posiciones_db()
    
    def insertar_al_final(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamano += 1
        self.actualizar_posiciones_db()
    
    def obtener_primero(self):
        return self.cabeza.vuelo if self.cabeza else None
    
    def obtener_ultimo(self):
        return self.cola.vuelo if self.cola else None
    
    def longitud(self):
        return self.tamano
    
    def insertar_en_posicion(self, vuelo, posicion):
        if posicion < 0 or posicion > self.tamano:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.tamano:
            self.insertar_al_final(vuelo)
        else:
            nuevo_nodo = Nodo(vuelo)
            actual = self.cabeza
            for _ in range(posicion - 1):
                actual = actual.siguiente
            
            nuevo_nodo.siguiente = actual.siguiente
            nuevo_nodo.anterior = actual
            actual.siguiente.anterior = nuevo_nodo
            actual.siguiente = nuevo_nodo
            self.tamano += 1
            self.actualizar_posiciones_db()
    
    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.tamano:
            raise IndexError("Posición fuera de rango")
        
        if posicion == 0:
            vuelo = self.cabeza.vuelo
            if self.cabeza.siguiente is None:
                self.cabeza = self.cola = None
            else:
                self.cabeza = self.cabeza.siguiente
                self.cabeza.anterior = None
        elif posicion == self.tamano - 1:
            vuelo = self.cola.vuelo
            self.cola = self.cola.anterior
            self.cola.siguiente = None
        else:
            actual = self.cabeza
            for _ in range(posicion):
                actual = actual.siguiente
            
            actual.anterior.siguiente = actual.siguiente
            actual.siguiente.anterior = actual.anterior
            vuelo = actual.vuelo
        
        self.tamano -= 1
        self.actualizar_posiciones_db()
        return vuelo
    
    def listar_vuelos(self):
        vuelos = []
        actual = self.cabeza
        while actual is not None:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos
    
    def reordenar_vuelos(self, posicion_origen, posicion_destino):
        if posicion_origen < 0 or posicion_origen >= self.tamano or \
           posicion_destino < 0 or posicion_destino >= self.tamano:
            raise IndexError("Posiciones fuera de rango")
        
        vuelo = self.extraer_de_posicion(posicion_origen)
        self.insertar_en_posicion(vuelo, posicion_destino)