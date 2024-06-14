
from src.logica.controlador_actividad import ControladorActividad
from src.modelo.actividad import Actividad
from src.modelo.reporte_gastos import ReporteGastos
from src.modelo.compensacion import Compensacion
from src.modelo.viajero import Viajero

class ControladorReporte:

    def __init__(self):
        self._controladorActividades= ControladorActividad()



    def generar_reporte_gastos(self, nombreActividad):
        actividades = self._controladorActividades.get_all_actividades()
        actividadEncontrada = Actividad()

        for actividad in actividades:
            if actividad.nombreActividad == nombreActividad:
                actividadEncontrada = actividad
                break

        if actividadEncontrada.nombreActividad == None:
            return "No se genera reporte porque no existe la actividad en el sistema"

        if not actividadEncontrada.gastos or not actividadEncontrada.viajeros:
            return "No se genera reporte porque no hay gastos o viajeros asociados a la actividad"

        listaGastos = []
        for viajero in actividadEncontrada.viajeros:
            reporteGastoViajero = ReporteGastos(viajero, 0)
            for gasto in actividadEncontrada.gastos:
                if viajero.identificadorViajero == gasto.viajero[0].identificadorViajero:
                    reporteGastoViajero.set_gastos_totales(reporteGastoViajero.obtener_gastos_totales() + gasto.valorGasto)

            listaGastos.append(reporteGastoViajero)

        return listaGastos

    def generar_reporte_compensacion(self, nombreActividad):
        actividades = self._controladorActividades.get_all_actividades()
        actividadEncontrada = Actividad()
        for actividad in actividades:
            if actividad.nombreActividad == nombreActividad:
                actividadEncontrada = actividad
                break

        if actividadEncontrada.nombreActividad == None:
            return "No se genera reporte porque no existe la actividad en el sistema"

        if not actividadEncontrada.gastos or not actividadEncontrada.viajeros:
            return "No se genera reporte porque no hay gastos o viajeros asociados a la actividad"

        gastoTotal = 0
        for gasto in actividadEncontrada.gastos:
            gastoTotal = gastoTotal + gasto.valorGasto
        aporteIndividual = gastoTotal/len(actividadEncontrada.viajeros)

        gastosPorViajeroEnActividad = self.generar_reporte_gastos(nombreActividad)

        listaCompensacion = []
        for gastosPorViajero in gastosPorViajeroEnActividad:
            compensacion = Compensacion(gastosPorViajero.obtener_viajero(), 0)
            if (gastosPorViajero.obtener_gastos_totales() < aporteIndividual):
                valorCompensacion = aporteIndividual - gastosPorViajero.obtener_gastos_totales()
                compensacion.set_valorCompensacion(valorCompensacion)
            listaCompensacion.append(compensacion)

        return listaCompensacion