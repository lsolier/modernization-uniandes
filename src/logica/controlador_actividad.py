
from src.modelo.actividad import Actividad
from src.modelo.declarative_base import engine, Base, session
from src.utils.error_handler import ErrorHandling
from src.utils.app_code_errors import AppCodeErrors
from src.modelo.gasto import Gasto,ActividadGasto
from src.modelo.viajero import Viajero,ActividadViajero


class ControladorActividad:

    def __init__(self):
        super().__init__()
        self._actividades = []
        Base.metadata.create_all(engine)


    def get_all_actividades(self):
            try:
                self._actividades = session.query(Actividad).all()
                if self._actividades == None:
                    self._actividades = []
                return self._actividades
            except:
                ErrorHandling(False, AppCodeErrors.actividad_no_existe)

    def get_actividad(self,nombreActividad):
        try:
            actividad = session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()
            return actividad
        except:
            return ErrorHandling(False, AppCodeErrors.actividad_no_existe)

    def add_actividad(self, nombreActividad):
        try:
            actividad = self.get_actividad(nombreActividad)
            if actividad == None:
                nuevaActividad = Actividad(nombreActividad=nombreActividad, estadoActividad=True)
                session.add(nuevaActividad)
                session.commit()
                return True
            else:
                return False
        except:
            return ErrorHandling(False, AppCodeErrors.actividad_repetida)
    def add_actividad_obj(self,actividad):
        session.add(actividad)
        session.commit()

    def modificar_actividad(self,nombreActividad, nuevoNombre):
        try:
            actividad = self.get_actividad(nombreActividad)
            actividad.nombreActividad = nuevoNombre
            session.commit()
        except:
            return ErrorHandling(False, AppCodeErrors.error_edicion_actividad)

    def editar_actividad_obj(self, actividad):
        try:
            session.add(actividad)
            session.commit()
            return True
        except:
            return False

    def remove_actividad(self, nombreActividad):
        try:

            actividad= session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()
            if actividad != None :
                session.delete(actividad)
                session.commit()
                return True
            else:
                return False
        except:
            return ErrorHandling(False, AppCodeErrors.error_eliminacion_actividad)

    def agregarViajeroActividad(self, viajero, nombreActividad):
        try:
            actividad= session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()
            if actividad != None:
                if self.viajero_existe_en_actividad(viajero,actividad) :
                    return False
                actividad.viajeros.append(viajero)
                session.add(actividad)
                session.commit()
                return True
            raise ErrorHandling(False,AppCodeErrors.actividad_no_existe)
        except:
            raise ErrorHandling(False, AppCodeErrors.error_agregar_viajero_actividad)
    def viajero_existe_en_actividad(self, viajero, actividad):

        for actViajero in actividad.viajeros :
            if actViajero.identificadorViajero == viajero.identificadorViajero:
                return True

        return False
      
    def get_gastos(self, nombreActividad):
        actividad = session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()
        if actividad is None:
            return ErrorHandling(False, AppCodeErrors.error_edicion_actividad)
        return actividad.gastos
    def remove_viajero(self, nombreActividad, identificadorViajero):
        try:
            actividad = session.query(Actividad).filter(Actividad.nombreActividad == nombreActividad).first()
            if actividad != None:
                for viajero in actividad.viajeros:
                    if viajero.identificadorViajero == identificadorViajero:
                        actividad.viajeros.remove(viajero)
            session.add(actividad)
            session.commit()
            return True
        except:
            return False

