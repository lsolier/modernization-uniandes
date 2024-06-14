
from src.modelo.viajero import  Viajero
class Compensacion:

    def __init__(self, viajero, valor):
        self._viajero = viajero
        self._valorCompensacion = valor

    def get_viajero(self):
        return self._viajero

    def get_valorCompensacion(self):
        return self._valorCompensacion

    def set_valorCompensacion(self, valor):
        self._valorCompensacion = valor