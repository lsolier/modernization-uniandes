
import unittest
from faker import Faker
from src.modelo.gasto import Gasto, ActividadGasto
from src.logica.controlador_gasto import ControladorGasto
from src.modelo.declarative_base import Session
from src.modelo.actividad import Actividad
from src.modelo.viajero import Viajero,ActividadViajero
from datetime import date

class TestControladorGasto(unittest.TestCase):

    def setUp(self):
        self.data_factory = Faker()
        Faker.seed(1000)
        self.session= Session()
        self._controladorGasto= ControladorGasto()

    def test_a_add_gasto(self):
        gasto = Gasto( id = 1,
                      fechaGasto= date.today(),
                      concepto = str(self.data_factory.sentence()),
                      valorGasto = self.data_factory.random.randint(0,1000))
        respControlador= self._controladorGasto.add_gasto_obj(gasto)
        respuestaEsp= self.session.query(Gasto).filter(Gasto.concepto == gasto.concepto).first()
        self.assertEquals(respControlador, True)
        self.assertEquals(respuestaEsp.concepto, gasto.concepto)

    def test_b_edit_gasto(self):
        gastoCotrolador = self._controladorGasto.get_gasto(1)
        gastoCotrolador.valorGasto = 123456
        respControlador = self._controladorGasto.edit_gasto(gastoCotrolador)
        respuestaEsp = self.session.query(Gasto).filter(Gasto.id == 1).first()
        self.assertEquals(respControlador, True)
        self.assertEquals(respuestaEsp.valorGasto, 123456)

    def test_c_delete_gasto(self):
        respControlador = self._controladorGasto.delete_gasto(1)
        respuestaEsp = self.session.query(Gasto).filter(Gasto.id == 1).first()
        self.assertEquals(respControlador, True)
        self.assertEquals(respuestaEsp, None)

