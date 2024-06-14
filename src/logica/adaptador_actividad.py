from src.logica.controlador_actividad import ControladorActividad
from src.logica.controlador_gasto import ControladorGasto
from src.logica.controlador_viajero import ControladorViajero
from src.utils.app_code_errors import AppCodeErrors
from src.utils.logic_response import logicResponse


class AdaptadorActividad:


    def __init__(self):
        self._controlador_actividad = ControladorActividad()
        self._controlador_gasto = ControladorGasto()
        self._controlador_viajero = ControladorViajero()

    def listar_actividades(self):
            listaActividades = self._controlador_actividad.get_all_actividades()
            if listaActividades != None:
                return logicResponse(True, listaActividades)
            else :
                return logicResponse(False, [])

    def ver_gastos_actividad(self, nombreActividad):
        try:
            gastosActividad = self._controlador_actividad.get_gastos(nombreActividad)
            if gastosActividad != None:
                return logicResponse(True, gastosActividad)
            else:
                return logicResponse(True, [])
        except:
            return logicResponse(False, [])

    def agregar_actividad(self, nombreActividad):
        try:
            resp = self._controlador_actividad.add_actividad(nombreActividad)
            if resp == True:
                return logicResponse(True, "")
            else:
                return  logicResponse(False, AppCodeErrors.actividad_repetida)
        except:
            return logicResponse(False, "")

    def agregar_viajero_actividad(self, nombreActividad, nombreViajero, apellidoViajero):
        try:
            viajero = self._controlador_viajero.get_viajero(nombreViajero,apellidoViajero)
            resp = self._controlador_actividad.agregarViajeroActividad(viajero,nombreActividad)
            if resp != None:
                return logicResponse(True, "")
            else:
                return logicResponse(False, AppCodeErrors.error_agregar_viajero_actividad)
        except:
            return logicResponse(False, AppCodeErrors.error_agregar_viajero_actividad)

    def editar_actividad(self,nombreActual, nuevoNombre):
        try:
            actividad = self._controlador_actividad.get_actividad(nombreActual)
            if actividad != None and len(actividad.viajeros) == 0 and len (actividad.gastos) == 0 :
                resp = self._controlador_actividad.modificar_actividad(nombreActual,nuevoNombre)
                return logicResponse(True, "")
            else:
                return logicResponse(False, AppCodeErrors.error_edicion_actividad)
        except:
            return (False, AppCodeErrors.error_edicion_actividad)
    def eliminar_actividad(self, nombreActividad):
        try:
            actividad = self._controlador_actividad.get_actividad(nombreActividad)
            if actividad != None and len(actividad.viajeros) == 0 and len(actividad.gastos) == 0:
                resp = self._controlador_actividad.remove_actividad(nombreActividad)
                return logicResponse(True, "")
            else:
                return logicResponse(False, AppCodeErrors.error_eliminacion_actividad)
        except:
            return (False, AppCodeErrors.error_eliminacion_actividad)
    def add_gasto_actividad(self, nombreActividad,gasto):
        try:
            actividad = self._controlador_actividad.get_actividad(nombreActividad)
            if actividad != None:
                actividad.gastos.append(gasto)
                resp = self._controlador_actividad.editar_actividad_obj(actividad)
                return logicResponse(True, "")
            else:
                return logicResponse(False, AppCodeErrors.error_agregando_gasto)
        except:
            return logicResponse(False, AppCodeErrors.error_agregando_gasto)

    def editar_gasto(self, nombreActividad, gasto):
        try:
            rep = self._controlador_gasto.edit_gasto(gasto)
            return logicResponse(True, "")
        except:
            return logicResponse(False, "")
    def add_viajero(self, nombre, apellido):
        try:
            resp = self._controlador_viajero.agregar_viajero(nombre,apellido)
            if resp == True:
                return logicResponse(True, "")
            if resp == False:
                return logicResponse(False, AppCodeErrors.error_agregar_viajero.value)
        except:
            return logicResponse(False, "")
    def get_viajeros(self):
        try:
            resp = self._controlador_viajero.get_viajeros()
            return logicResponse(True, resp)
        except:
            return logicResponse(False, "")
    def remove_viajero(self,actividadnombre, identificadorViajero):
        try:
            resp = self._controlador_actividad.remove_viajero(actividadnombre,identificadorViajero)
            return logicResponse(resp, "")
        except:
            return logicResponse(False, "")
    def get_viajero(self, identificadorViajero):
        try:
            resp = self._controlador_viajero.get_viajero_id(identificadorViajero)
            if resp != None:
                return logicResponse(True, resp)
            else:
                return  logicResponse(False, "")
        except:
            return logicResponse(False, "")
