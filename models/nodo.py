# models/nodo.py
class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.siguiente = None
        self.anterior = None