import unittest

from src.logica.controlador_viajero import ControladorViajero
from src.modelo.viajero import Viajero
from src.modelo.actividad import Actividad
from src.modelo.gasto import Gasto
from src.modelo.declarative_base import Session

from faker import Faker

class ViajeroTestCase(unittest.TestCase):

    def setUp(self):
        self.controlador_viajero = ControladorViajero()
        self.session = Session()

        self.data_factory = Faker()
        Faker.seed(1000)

        '''Creamos 10 datos en data y creamos los viajeros'''
        self.data = []
        self.viajeros = []

        for i in range(0, 10):
            nombre = self.data_factory.unique.first_name()
            apellido = self.data_factory.unique.last_name()
            fake_data = (nombre, apellido, (nombre+apellido))
            self.data.append(fake_data)

            viajero_fake = Viajero(nombre=self.data[-1][0],
                                   apellido=self.data[-1][1],
                                   identificadorViajero=self.data[-1][2],
                                   actividades=[],
                                   gastos=[])
            self.viajeros.append(viajero_fake)
            self.session.add(self.viajeros[-1])

        '''Persiste los objetos en este setUp no se cierra la sesión para usar los viajeros en las pruebas'''
        self.session.commit()

    def test_constructor(self):
        for viajero, dato in zip(self.viajeros, self.data):
            self.assertEqual(viajero.nombre, dato[0])
            self.assertEqual(viajero.apellido, dato[1])
            self.assertEqual(viajero.identificadorViajero, dato[2])

    def test_agregar_viajero(self):
        resultado = self.controlador_viajero.agregar_viajero(nombre="Luis", apellido="Solier")
        self.assertEqual(resultado, True)

    def test_verificar_almacenamiento_viajero_bd(self):
        self.session = Session()
        self.controlador_viajero.agregar_viajero(nombre="Luis", apellido="Solier")
        viajero = self.session.query(Viajero).filter(Viajero.identificadorViajero == 'LuisSolier').first()
        self.assertEqual(viajero.nombre, 'Luis')
        self.assertEqual(viajero.apellido, 'Solier')

    def test_no_agregar_viajero_repetido(self):
        resultado = self.controlador_viajero.agregar_viajero(nombre="Luis", apellido="Solier")
        self.assertEqual(resultado, True)
        resultado = self.controlador_viajero.agregar_viajero(nombre="Luis", apellido="Solier")
        self.assertEqual(resultado, False)

    def test_editar_viajero(self):
        viajeroExistente = self.viajeros[-1]
        resultado = self.controlador_viajero.editar_viajero(nombre=viajeroExistente.nombre, apellido=viajeroExistente.apellido, nuevoNombre="Nick", nuevoApellido="Solier")
        self.assertEqual(resultado, True)

    def test_no_editar_viajero_cuando_no_existe(self):
        viajeroExistente = self.viajeros[-1]
        nombreInexistente = viajeroExistente.nombre+'X'
        apellidoInexistente = viajeroExistente.apellido+'Y'
        resultado = self.controlador_viajero.editar_viajero(nombre=nombreInexistente, apellido=apellidoInexistente, nuevoNombre="Nick", nuevoApellido="Solier")
        self.assertEqual(resultado, False)

    def test_verificar_modificacion_viajero_bd(self):
        self.session = Session()
        viajeroExistente = self.viajeros[-1]
        self.controlador_viajero.editar_viajero(nombre=viajeroExistente.nombre, apellido=viajeroExistente.apellido, nuevoNombre="Pepe", nuevoApellido="Perez")
        viajero = self.session.query(Viajero).filter(Viajero.identificadorViajero == 'PepePerez').first()
        self.assertEqual(viajero.nombre, 'Pepe')
        self.assertEqual(viajero.apellido, 'Perez')

    def test_eliminar_viajero(self):
        viajeroExistente = self.viajeros[-1]
        resultado = self.controlador_viajero.eliminar_viajero(nombre=viajeroExistente.nombre, apellido=viajeroExistente.apellido)
        self.assertEqual(resultado, True)

    def test_no_eliminar_viajero_cuando_no_existe(self):
        viajeroExistente = self.viajeros[-1]
        nombreInexistente = viajeroExistente.nombre + 'X'
        apellidoInexistente = viajeroExistente.apellido + 'Y'
        resultado = self.controlador_viajero.eliminar_viajero(nombre=nombreInexistente, apellido=apellidoInexistente)
        self.assertEqual(resultado, False)

    def test_verificar_eliminacion_viajero_bd(self):
        self.session = Session()
        viajerosBD = self.session.query(Viajero).all()
        self.assertEqual(len(viajerosBD), 10)
        viajeroExistente = self.viajeros[-1]
        resultado = self.controlador_viajero.eliminar_viajero(nombre=viajeroExistente.nombre, apellido=viajeroExistente.apellido)
        self.assertEqual(resultado, True)
        viajerosBD = self.session.query(Viajero).all()
        self.assertEqual(len(viajerosBD), 9)

    def test_verificar_obtener_todos_viajeros(self):
        viajeros = self.controlador_viajero.get_viajeros()
        self.assertGreater(len(viajeros), 0)

    def test_verificar_obtener_viajero_existente(self):
        viajeroExistente = self.viajeros[-1]
        viajero = self.controlador_viajero.get_viajero(nombre=viajeroExistente.nombre, apellido=viajeroExistente.apellido)
        self.assertIsNotNone(viajero)

    def test_verificar_obtener_none_cuando_viajero_no_existe(self):
        viajeroExistente = self.viajeros[-1]
        nombreInexistente = viajeroExistente.nombre + 'X'
        apellidoInexistente = viajeroExistente.apellido + 'Y'
        viajero = self.controlador_viajero.get_viajero(nombre=nombreInexistente, apellido=apellidoInexistente)
        self.assertIsNone(viajero)

    def tearDown(self):
        '''Abre la session'''
        self.session = Session()

        viajeros = self.session.query(Viajero).all()
        for viajero in viajeros:
            self.session.delete(viajero)

        self.session.commit()
        self.session.close()

