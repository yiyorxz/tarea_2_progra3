# models/lista_vuelos.py
from models.nodo import Nodo

class ListaVuelos:
    def __init__(self, db_session):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
        self.session = db_session
    
    def insertar_al_frente(self, vuelo):
        """Inserta un vuelo al inicio (para emergencias)"""
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        self.tamano += 1
    
    def insertar_al_final(self, vuelo):
        """Inserta un vuelo al final (vuelos regulares)"""
        nuevo_nodo = Nodo(vuelo)
        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamano += 1
    
    def obtener_primero(self):
        """Retorna el primer vuelo sin removerlo"""
        if self.cabeza is None:
            return None
        return self.cabeza.vuelo
    
    def obtener_ultimo(self):
        """Retorna el último vuelo sin removerlo"""
        if self.cola is None:
            return None
        return self.cola.vuelo
    
    def longitud(self):
        """Retorna el número total de vuelos"""
        return self.tamano
    
    def insertar_en_posicion(self, vuelo, posicion):
        """Inserta un vuelo en una posición específica"""
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
    
    def extraer_de_posicion(self, posicion):
        """Remueve y retorna el vuelo en la posición dada"""
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
        return vuelo
    
    def listar_vuelos(self):
        """Retorna todos los vuelos en orden"""
        vuelos = []
        actual = self.cabeza
        while actual is not None:
            vuelos.append(actual.vuelo)
            actual = actual.siguiente
        return vuelos
    
    def reordenar_vuelos(self, posicion_origen, posicion_destino):
        """Reordena vuelos moviendo uno de posición"""
        if posicion_origen < 0 or posicion_origen >= self.tamano or \
           posicion_destino < 0 or posicion_destino >= self.tamano:
            raise IndexError("Posiciones fuera de rango")
        
        vuelo = self.extraer_de_posicion(posicion_origen)
        self.insertar_en_posicion(vuelo, posicion_destino)