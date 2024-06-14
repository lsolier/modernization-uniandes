import unittest
from src.logica.controlador_actividad import ControladorActividad
from src.logica.controlador_viajero import ControladorViajero
from src.logica.controlador_gasto import ControladorGasto
from src.modelo.actividad import Actividad
from faker import Faker
from src.utils.error_handler import ErrorHandling
from src.utils.app_code_errors import AppCodeErrors
from src.modelo.viajero import Viajero, ActividadViajero
from src.modelo.gasto import Gasto, ActividadGasto
from src.modelo.declarative_base import Session
from datetime import date


class test_controlador_actividad(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.data_factory = Faker()
        Faker.seed(1000)
        self.data = []
        self.controladorActividad = ControladorActividad()
        self.controladorGastos = ControladorGasto()
        self.nombreActividadMock = self.data_factory.sentence()
        self.controladorViajero = ControladorViajero()
        self._nombreViajero = self.data_factory.unique.name()
        self._apellido = self.data_factory.unique.name()
        self._viajero = Viajero(nombre=self._nombreViajero,
                          apellido=self._apellido,
                          identificadorViajero=self._nombreViajero + self._apellido)

    def test_a_crearactividadnombreunico_first(self):

        respuestaControlador = self.controladorActividad.add_actividad(self.nombreActividadMock)
        respuesta= self.session.query(Actividad).filter(Actividad.nombreActividad == self.nombreActividadMock).first()
        self.assertEquals(respuestaControlador, True)
        self.assertEquals(respuesta.nombreActividad, self.nombreActividadMock)

    def test_b_getactividad_next(self):
        respuestaControlador= self.controladorActividad.get_actividad(self.nombreActividadMock)
        respuestaEsperada = self.session.query(Actividad).filter(Actividad.nombreActividad == self.nombreActividadMock).first()
        self.assertEquals(respuestaControlador.nombreActividad, respuestaEsperada.nombreActividad)

    def test_c_getallactividades_next(self):
        respuestaControlador = self.controladorActividad.get_all_actividades()
        respuestaEsperada= self.session.query(Actividad).all()
        for actividadRetornada, actividadEsperada in zip(respuestaControlador,respuestaEsperada):
            self.assertEquals(actividadRetornada.nombreActividad,actividadEsperada.nombreActividad)


    def test_d_asociar_viajero_actividad(self):


        self.controladorViajero.agregar_viajero_obj(self._viajero)
        respuestaControlador = self.controladorActividad.agregarViajeroActividad(self._viajero, self.nombreActividadMock)
        respEsperada = self.session.query(Actividad).filter(
            Actividad.nombreActividad == self.nombreActividadMock).first()
        self.assertEquals(respuestaControlador, True)
        self.assertEquals(len(respEsperada.viajeros), 1)


    def test_e_asociar_viajero_actividad_error_viajeroexistente(self):
        errorEsperado = ErrorHandling(False, AppCodeErrors.error_agregar_viajero_actividad_existente)
        respuestaControlador = self.controladorActividad.agregarViajeroActividad(self._viajero, self.nombreActividadMock)

        self.assertEquals(respuestaControlador, False)
        


    def test_d_obtener_gastos_de_una_actividad(self):
        gasto1 = Gasto(fechaGasto= date.today(), concepto="almuerzo", valorGasto=120.00)
        gasto2 = Gasto(fechaGasto= date.today(), concepto="almuerzo", valorGasto=80.00)
        self.controladorGastos.add_gasto_obj(gasto1)
        self.controladorGastos.add_gasto_obj(gasto2)

        gastosMock = [gasto1, gasto2]
        actividadExistente = self.controladorActividad.get_actividad(self.nombreActividadMock)
        actividadExistente.gastos = gastosMock

        self.controladorActividad.add_actividad_obj(actividadExistente)
        gastos = self.controladorActividad.get_gastos(self.nombreActividadMock)
        self.assertTrue(len(gastos) > 0)


    def test_e_deleteactividad_last(self):
        respuestaControlador= self.controladorActividad.remove_actividad(self.nombreActividadMock)
        listaActividadesEsperada= self.session.query(Actividad).all()
        for actividad in listaActividadesEsperada:
            self.assertNotEqual(actividad.nombreActividad,self.nombreActividadMock)

        self.controladorGastos.delete_all_gastos()
        self.controladorViajero.eliminar_viajero(self._nombreViajero, self._apellido)
