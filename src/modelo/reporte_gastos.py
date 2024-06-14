
from src.modelo.viajero import Viajero

class ReporteGastos:

    def __init__(self):
        self._viajero = Viajero()
        self._gastosTotales = 0

    def __init__(self, viajero, total):
        self._viajero = viajero
        self._gastosTotales = total

    def obtener_viajero(self):
        return self._viajero

    def obtener_gastos_totales(self):
        return self._gastosTotales

    def set_gastos_totales(self, valor):
        self._gastosTotales = valor