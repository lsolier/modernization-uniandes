
from enum import Enum

class AppCodeErrors(Enum):
    actividad_repetida = "La actividad ya fue agregada al sistema"
    actividad_no_existe = "La actividad no existe"
    error_edicion_actividad= "No se pudo realizar la edición a una actividad, tiene asociada gastos y viajeros"
    error_eliminacion_actividad= "No se pudo eliminar la actividad"
    error_agregar_viajero_actividad = "No se puede agregar viajero a la actividad"
    error_agregar_viajero_actividad_existente= "Existe un viajero registrado con ese nombre  en la actividad"
    error_agregando_gasto=  "No se puede asociar gasto a la actividad"
    error_agregar_viajero=  "El viajero ya existe en el sistema"
