'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.adaptador_actividad import AdaptadorActividad
from src.logica.controlador_reporte import ControladorReporte
from src.logica.controlador_actividad import ControladorActividad

class Logica_mock():

    def __init__(self):
        self.controlador_reporte = ControladorReporte()
        self.controlador_actividad = ControladorActividad()
        self.adaptador_actividad= AdaptadorActividad()

        #Este constructor contiene los datos falsos para probar la interfaz
        adaptadorResp = self.adaptador_actividad.listar_actividades()
        if adaptadorResp.status == True:
            self.actividades = adaptadorResp.result

        self.viajeros = [{"Nombre":"Pepe", "Apellido":"Pérez"}, {"Nombre":"Ana", "Apellido":"Andrade"}]
        #self.gastos = [{"Concepto":"Gasto 1", "Fecha": "12-12-2020", "Valor": 10000, "Nombre": "Pepe", "Apellido": "Pérez"}, {"Concepto":"Gasto 2", "Fecha": "12-12-2020", "Valor": 20000, "Nombre":"Ana", "Apellido":"Andrade"}]
        #self.matriz = [["", "Pepe Pérez", "Ana Andrade", "Pedro Navajas" ],["Pepe Pérez", -1, 1200, 1000],["Ana Andrade", 0, -1, 1000], ["Pedro Navajas", 0, 0, -1]]
        #self.gastos_consolidados = [{"Nombre":"Pepe", "Apellido":"Pérez", "Valor":15000}, {"Nombre":"Ana", "Apellido":"Andrade", "Valor":12000},{"Nombre":"Pedro", "Apellido":"Navajas", "Valor":0}]
        self.viajeros_en_actividad = [{"Nombre": "Pepe Pérez", "Presente":True}, {"Nombre": "Ana Andrade", "Presente":True}, {"Nombre":"Pedro Navajas", "Presente":False}]

    def get_gastos_consolidados(self, nombreActividad):
        return self.controlador_reporte.generar_reporte_gastos(nombreActividad)

    def get_gastos_actividad(self, nombreActividad):
        return self.controlador_actividad.get_gastos(nombreActividad)

    def get_matriz_gastos_totales(self, nombreActividad):
        matrizCompensacion = []
        listaCompensacion = self.controlador_reporte.generar_reporte_compensacion(nombreActividad)

        listaViajeros = []
        listaViajeros.append("")
        for compensacion in listaCompensacion:
            viajero = compensacion.get_viajero()
            nombreCompleto = viajero.nombre + " " + viajero.apellido
            listaViajeros.append(nombreCompleto)
        matrizCompensacion.append(listaViajeros)

        gastoTotal = 0
        gastos = self.controlador_actividad.get_gastos(nombreActividad)
        for gasto in gastos:
            gastoTotal = gastoTotal + gasto.valorGasto
        gastoEquitativo = gastoTotal/len(listaCompensacion)

        gatosPorViajero = self.controlador_reporte.generar_reporte_gastos(nombreActividad)
        for compensacion in listaCompensacion:
            listaCompensacionConsolidada = []
            nombreCompleto = compensacion.get_viajero().nombre+ " " + compensacion.get_viajero().apellido
            listaCompensacionConsolidada.append(nombreCompleto)

            identificadorViajero = compensacion.get_viajero().identificadorViajero
            valorCompensacion = compensacion.get_valorCompensacion()
            for gastoPorViajero in gatosPorViajero:
                viajero = gastoPorViajero.obtener_viajero()

                if identificadorViajero == viajero.identificadorViajero:
                    listaCompensacionConsolidada.append(-1)
                else:
                    if valorCompensacion == 0:
                        listaCompensacionConsolidada.append(0)
                    else:
                        gastoRealizadoPorViajero = gastoPorViajero.obtener_gastos_totales()
                        if gastoRealizadoPorViajero <= gastoEquitativo:
                            listaCompensacionConsolidada.append(0)
                        else:
                            compensacionPendiente = gastoRealizadoPorViajero - gastoEquitativo
                            if compensacionPendiente >= valorCompensacion:
                                listaCompensacionConsolidada.append(valorCompensacion)
                                valorCompensacion = 0
                            else:
                                listaCompensacionConsolidada.append(compensacionPendiente)
                                valorCompensacion = valorCompensacion - compensacionPendiente

            matrizCompensacion.append(listaCompensacionConsolidada)
        return matrizCompensacion