

import unittest
from datetime import date
from src.logica.controlador_actividad import ControladorActividad
from src.logica.controlador_reporte import ControladorReporte
from src.logica.controlador_gasto import ControladorGasto
from src.logica.controlador_viajero import ControladorViajero
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero,ActividadViajero
from src.modelo.gasto import Gasto,ActividadGasto
from src.modelo.reporte_gastos import ReporteGastos
from faker import Faker
import random

class test_controlador_actividad(unittest.TestCase):

    def setUp(self):
        self.actividad1 = Actividad()
        self.actividad2 = Actividad()
        self.actividad3 = Actividad()
        self._controladorReporte = ControladorReporte()
        self.controladorActividad= ControladorActividad()
        self._controladorViajero = ControladorViajero()
        self._controladorGasto = ControladorGasto()
        self.inicializar_actividades()



    def test_a_generar_reporte_cuando_actividad_noexiste(self):
        self.assertEqual(self._controladorReporte.generar_reporte_gastos("actividadNoExiste"),
                         "No se genera reporte porque no existe la actividad en el sistema")


    def test_b_generar_reporte_cuando_viajeros_esvacio(self):
        self.controladorActividad.add_actividad_obj(self.actividad1)
        self.controladorActividad.add_actividad_obj(self.actividad2)
        self.controladorActividad.add_actividad_obj(self.actividad3)

        self.assertEqual(self._controladorReporte.generar_reporte_gastos("actividadVacia"),
                         "No se genera reporte porque no hay gastos o viajeros asociados a la actividad")

    def test_c_generar_reporte_cuando_actividad_vacia(self):
        self.assertEqual(self._controladorReporte.generar_reporte_gastos("actividadVacia"), "No se genera reporte porque no hay gastos o viajeros asociados a la actividad")

    def test_d_generar_reporte_cuando_haygastos(self):
        totalViajero1= ReporteGastos(Viajero(nombre="pepe", apellido="1", identificadorViajero="pepe1"), 3000)
        totalViajero2= ReporteGastos(Viajero(nombre="pepe", apellido="2", identificadorViajero="pepe2"), 1000)
        totalViajero3= ReporteGastos(Viajero(nombre="pepe", apellido="3", identificadorViajero="pepe3"), 2000)
        listaGastos= [totalViajero1,totalViajero2,totalViajero3]

        reporteGenerado = self._controladorReporte.generar_reporte_gastos("actividadLLena")

        for i in range(len(reporteGenerado)):
            identificador = reporteGenerado[i].obtener_viajero().identificadorViajero
            identificadorEsperado = listaGastos[i].obtener_viajero().identificadorViajero

            dinero = reporteGenerado[i].obtener_gastos_totales()
            dineroEsperado = listaGastos[i].obtener_gastos_totales()

            self.assertEqual(identificador, identificadorEsperado)
            self.assertEqual(dinero, dineroEsperado)


    def test_e_generar_reporte_cuando_unviajero_tienegastos(self):

        totalViajero1= ReporteGastos(Viajero(nombre="pepe", apellido="1", identificadorViajero="pepe1"), 4000)
        totalViajero2= ReporteGastos(Viajero(nombre="pepe", apellido="2", identificadorViajero="pepe2"), 0)
        totalViajero3= ReporteGastos(Viajero(nombre="pepe", apellido="3", identificadorViajero="pepe3"), 0)
        listaGastos= [totalViajero1,totalViajero2,totalViajero3]

        reporteGenerado = self._controladorReporte.generar_reporte_gastos("actividadGastosViajero1")
        for i in range(len(reporteGenerado)):
            identificador = reporteGenerado[i].obtener_viajero().identificadorViajero
            identificadorEsperado = listaGastos[i].obtener_viajero().identificadorViajero

            dinero = reporteGenerado[i].obtener_gastos_totales()
            dineroEsperado = listaGastos[i].obtener_gastos_totales()

            self.assertEqual(identificador, identificadorEsperado)
            self.assertEqual(dinero, dineroEsperado)


        self.controladorActividad.remove_actividad("actividadLLena")
        self.controladorActividad.remove_actividad("actividadVacia")
        self.controladorActividad.remove_actividad("actividadGastosViajero1")
        self._controladorGasto.delete_all_gastos()

    def inicializar_actividades(self):

        self.actividad1 = Actividad(nombreActividad="actividadLLena", estadoActividad=True)
        self.actividad2 = Actividad(nombreActividad="actividadVacia", estadoActividad=True, gastos=[], viajeros=[])
        self.actividad3 = Actividad(nombreActividad="actividadGastosViajero1", estadoActividad=True)

        viajero1 = Viajero(nombre="pepe", apellido="1", identificadorViajero="pepe1")
        viajero2 = Viajero(nombre="pepe", apellido="2", identificadorViajero="pepe2")
        viajero3 = Viajero(nombre="pepe", apellido="3", identificadorViajero="pepe3")

        self._controladorViajero.agregar_viajero_obj(viajero1)
        self._controladorViajero.agregar_viajero_obj(viajero2)
        self._controladorViajero.agregar_viajero_obj(viajero3)

        gasto1 = Gasto(fechaGasto=date.today(), concepto="test gasto 1", valorGasto=3000)
        gasto2 = Gasto(fechaGasto=date.today(), concepto="test gasto 2", valorGasto=1000)
        gasto3 = Gasto(fechaGasto=date.today(), concepto="test gasto 3", valorGasto=2000)

        gasto5 = Gasto(fechaGasto=date.today(), concepto="test gasto 5", valorGasto=2000)
        gasto6 = Gasto(fechaGasto=date.today(), concepto="test gasto 6", valorGasto=2000)



        gasto1.viajero = [viajero1]
        gasto2.viajero = [viajero2]
        gasto3.viajero = [viajero3]
        gasto5.viajero = [viajero1]
        gasto6.viajero = [viajero1]

        self._controladorGasto.add_gasto_obj(gasto1)
        self._controladorGasto.add_gasto_obj(gasto2)
        self._controladorGasto.add_gasto_obj(gasto3)
        self._controladorGasto.add_gasto_obj(gasto5)
        self._controladorGasto.add_gasto_obj(gasto6)

        viajero1.gastos = [gasto1, gasto5, gasto6]
        viajero2.gastos = [gasto2]
        viajero3.gastos = [gasto3]

        self._controladorViajero.agregar_viajero_obj(viajero1)
        self._controladorViajero.agregar_viajero_obj(viajero2)
        self._controladorViajero.agregar_viajero_obj(viajero3)

        self.actividad1.viajeros = [viajero1, viajero2, viajero3]
        self.actividad1.gastos = [gasto1, gasto2, gasto3]

        self.actividad3.viajeros = [viajero1, viajero2, viajero3]
        self.actividad3.gastos = [gasto5,gasto6]


