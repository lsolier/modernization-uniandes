import unittest
from datetime import date
from faker import Faker

from src.logica.adaptador_actividad import AdaptadorActividad
from src.logica.controlador_actividad import ControladorActividad
from src.logica.controlador_viajero import ControladorViajero
from src.logica.controlador_gasto import ControladorGasto
from src.modelo.declarative_base import Session
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.viajero import Viajero
from src.utils.app_code_errors import AppCodeErrors


class test_adaptador_actividad(unittest.TestCase):

    def setUp(self):
        self.data_factory = Faker()
        Faker.seed(1000)
        self.actividad1 = Actividad()
        self.viajero3 = Viajero()
        self.gasto3 = Gasto()
        self.controladorActividad = ControladorActividad()
        self.controladorGastos = ControladorGasto()
        self.controladorViajero = ControladorViajero()
        self._adaptadorActividad= AdaptadorActividad()
        self.session = Session()
        self.inicializar_mocks()


    def test_a_mostrar_lista_de_actividades(self):
        respuestaAdaptador = self._adaptadorActividad.listar_actividades()
        actividadesEsperadas =self.session.query(Actividad).all()

        self.assertEquals(respuestaAdaptador.status, True)
        for actividad, actividadEsp in zip(respuestaAdaptador.result,actividadesEsperadas):
            self.assertEquals(actividad.nombreActividad,actividadEsp.nombreActividad)

    def test_b_ver_gastos_actividad(self):
        respuestaAdaptador = self._adaptadorActividad.ver_gastos_actividad("actividadLLena")
        actividadEsperada = self.session.query(Actividad).filter(Actividad.nombreActividad == "actividadLLena").first()

        self.assertEquals(respuestaAdaptador.status, True)
        for gasto, gastoEsp in zip(respuestaAdaptador.result, actividadEsperada.gastos):
            self.assertEquals(gasto.id, gastoEsp.id)

    def test_c_agregar_actividad(self):
        nombreActividad = self.data_factory.sentence()
        respuestaAñadir = self._adaptadorActividad.agregar_actividad(nombreActividad)
        actividadesperada = self.session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()

        self.assertEquals(respuestaAñadir.status, True)
        self.assertEquals(respuestaAñadir.result, "")
        self.assertEquals(actividadesperada.nombreActividad, nombreActividad)

    def test_d_agregar_viajero_actividad(self):
        actividadAntes = self.session.query(Actividad).filter(Actividad.nombreActividad == "actividadLLena").first()
        respuestaAdaptador = self._adaptadorActividad.agregar_viajero_actividad("actividadLLena",self.viajero3.nombre,self.viajero3.apellido)
        actividadEsperada = self.session.query(Actividad).filter(Actividad.nombreActividad == "actividadLLena").first()

        self.assertEquals(respuestaAdaptador.status, True)
        self.assertEquals(respuestaAdaptador.result, "")

    def test_e_editar_actividad_true(self):
        nombreActividad = self.data_factory.sentence()
        nuevoNombre = self.data_factory.sentence()
        respuestaAñadir = self._adaptadorActividad.agregar_actividad(nombreActividad)
        respuestaAdaptador = self._adaptadorActividad.editar_actividad(nombreActividad, nuevoNombre)
        respuestaEsperada = self.session.query(Actividad).filter(Actividad.nombreActividad == nuevoNombre).first()

        self.assertEquals(respuestaAdaptador.status, True)
        self.assertEquals(respuestaAdaptador.result, "")
        self.assertEquals(respuestaEsperada.nombreActividad, nuevoNombre)

    def test_f_editar_actividad_false(self):
        nuevoNombre = self.data_factory.sentence()
        respuestaAdaptador = self._adaptadorActividad.editar_actividad("actividadLLena", nuevoNombre)

        self.assertEquals(respuestaAdaptador.status, False)
        self.assertEquals(respuestaAdaptador.result, AppCodeErrors.error_edicion_actividad)

    def test_g_eliminar_actividad_true(self):
        nombreActividad = self.data_factory.sentence()
        respuestaAñadir = self._adaptadorActividad.agregar_actividad(nombreActividad)

        respuestaAdaptador = self._adaptadorActividad.eliminar_actividad(nombreActividad)
        respuestaEsperada = self.session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()

        self.assertEquals(respuestaAdaptador.status, True)
        self.assertEquals(respuestaAdaptador.result, "")
        self.assertEquals(respuestaEsperada, None)

    def test_h_eliminar_actividad_false(self):
        respuestaAdaptador = self._adaptadorActividad.eliminar_actividad("actividadLLena")
        self.assertEquals(respuestaAdaptador.status, False)
        self.assertEquals(respuestaAdaptador.result, AppCodeErrors.error_eliminacion_actividad)

    def test_i_agregar_gasto_actividad(self):
        """actividadAntes = self.session.query(Actividad).filter(Actividad.nombreActividad == "actividadLLena").first()"""
        actividadAntes = self.controladorActividad.get_actividad("actividadLLena")
        respuestaAdaptador = self._adaptadorActividad.add_gasto_actividad("actividadLLena", self.gasto3)
        actividadEsperada = self.controladorActividad.get_actividad("actividadLLena")

        self.assertEquals(respuestaAdaptador.status, True)
        self.assertEquals(respuestaAdaptador.result, "")

    def test_j_editar_gasto(self):
        gastos = self.controladorActividad.get_gastos("actividadLLena")
        gastosAnterior = self.session.query(Gasto).filter(Gasto.id == gastos[0].id).first()
        gastoEditado = gastos[0]
        gastoEditado.concepto = self.data_factory.sentence()
        respuestaAdaptador = self._adaptadorActividad.editar_gasto("actividadLLena", gastoEditado)
        nuevoGasto = self.session.query(Gasto).filter(Gasto.id == gastos[0].id).first()

        self.assertEquals(respuestaAdaptador.status, True)
        self.assertEquals(respuestaAdaptador.result, "")

    def tearDown(self):
        actividades = self.session.query(Actividad).all()
        viajeros = self.session.query(Viajero).all()
        gastos = self.session.query(Gasto).all()
        for actividad in actividades:
            self.session.delete(actividad)
        self.session.commit()
        for viajero in viajeros:
            self.session.delete(viajero)
        self.session.commit()
        for gasto in gastos:
            self.session.delete(gasto)

        self.session.commit()



    def inicializar_mocks(self):
        self.actividad1 = Actividad(nombreActividad="actividadLLena", estadoActividad=True)

        viajero1 = Viajero(nombre="pepe", apellido="1", identificadorViajero="pepe1")
        viajero2 = Viajero(nombre="pepe", apellido="2", identificadorViajero="pepe2")
        self.viajero3 = Viajero(nombre="pepe", apellido="3", identificadorViajero="pepe3")

        self.controladorViajero.agregar_viajero_obj(viajero1)
        self.controladorViajero.agregar_viajero_obj(viajero2)
        self.controladorViajero.agregar_viajero_obj(self.viajero3)

        gasto1 = Gasto(fechaGasto=date.today(), concepto="test gasto 1", valorGasto=3000)
        gasto2 = Gasto(fechaGasto=date.today(), concepto="test gasto 2", valorGasto=1500)
        self.gasto3 = Gasto(fechaGasto=date.today(), concepto="test gasto 3", valorGasto=1500)


        gasto1.viajero = [viajero1]
        gasto2.viajero = [viajero2]
        self.gasto3.viajero = [self.viajero3]

        self.controladorGastos.add_gasto_obj(gasto1)
        self.controladorGastos.add_gasto_obj(gasto2)
        self.controladorGastos.add_gasto_obj(self.gasto3)

        viajero1.gastos = [gasto1]
        viajero2.gastos = [gasto2]


        self.controladorViajero.agregar_viajero_obj(viajero1)
        self.controladorViajero.agregar_viajero_obj(viajero2)
        self.controladorViajero.agregar_viajero_obj(self.viajero3)

        self.actividad1.viajeros = [viajero1, viajero2]
        self.actividad1.gastos = [gasto1, gasto2]

        self.controladorActividad.add_actividad_obj(self.actividad1)
