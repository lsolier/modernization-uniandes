from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox

from .Vista_lista_actividades import Vista_lista_actividades
from .Vista_lista_viajeros import Vista_lista_viajeros
from .Vista_actividad import Vista_actividad
from .Vista_reporte_compensacion import Vista_reporte_compensacion
from .Vista_reporte_gastos import Vista_reporte_gastos_viajero
from ..logica.adaptador_actividad import AdaptadorActividad



class App_CuentasClaras(QApplication):
    """
    Clase principal de la interfaz que coordina las diferentes vistas/ventanas de la aplicación
    """

    def __init__(self, sys_argv, logica):
        """
        Constructor de la interfaz. Debe recibir la lógica e iniciar la aplicación en la ventana principal.
        """
        super(App_CuentasClaras, self).__init__(sys_argv)
        self.adaptadorActividad= AdaptadorActividad()
        self.logica = logica
        self.mostrar_vista_lista_actividades()
        self.actividades = self.adaptadorActividad.listar_actividades().result
        
        
    def mostrar_vista_lista_actividades(self):
        """
        Esta función inicializa la ventana de la lista de actividades
        """
        self.vista_lista_actividades = Vista_lista_actividades(self) 
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)


    def insertar_actividad(self, nombre):
        """
        Esta función inserta una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        if nombre == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error Agregar Actividad")
            msg.setText("El nombre de la actividad no puede ser vacío")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        else:
            resp = self.adaptadorActividad.agregar_actividad(nombre)

        self.actividades = self.adaptadorActividad.listar_actividades().result
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)

    def editar_actividad(self, nombreActividad, nombre):
        """
        Esta función editar una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        resp = self.adaptadorActividad.editar_actividad(nombreActividad, nombre)
        if resp.status == False:
            msg = QMessageBox()
            msg.setWindowTitle("Error Edición Actividad")
            msg.setText(resp.result.value)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

        self.vista_lista_actividades.mostrar_actividades(self.adaptadorActividad.listar_actividades())

    def eliminar_actividad(self, nombreActividad):
        """
        Esta función elimina una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        resp = self.adaptadorActividad.eliminar_actividad(nombreActividad)
        if resp.status == False:
            msg = QMessageBox()
            msg.setWindowTitle("Error Eliminar Actividad")
            msg.setText(resp.result.value)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        self.vista_lista_actividades.mostrar_actividades(self.logica.actividades)


    def mostrar_viajeros(self):
        """
        Esta función muestra la ventana de la lista de viajeros
        """
        self.vista_lista_viajeros=Vista_lista_viajeros(self)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def insertar_viajero(self, nombre, apellido):
        """
        Esta función inserta un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        if nombre == "" or apellido == "":
            msg = QMessageBox()
            msg.setWindowTitle("Error Agregar Viajero")
            msg.setText("los campos de nombre y apellido no pueden ser vacios")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

        else:
            resp = self.adaptadorActividad.add_viajero(nombre, apellido)
            if resp.status == False:
                msg = QMessageBox()
                msg.setWindowTitle("Error Agregar Viajero")
                msg.setText(resp.result)
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def editar_viajero(self, indice_viajero, nombre, apellido):
        """
        Esta función edita un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """        
        self.logica.viajeros[indice_viajero] = {"Nombre":nombre, "Apellido":apellido}
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)

    def eliminar_viajero(self, indice_viajero):
        """
        Esta función elimina un viajero en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros.pop(indice_viajero)
        self.vista_lista_viajeros.mostrar_viajeros(self.logica.viajeros)
    
    def mostrar_actividad(self, indice_actividad=-1):
        """
        Esta función muestra la ventana detallada de una actividad
        """
        if indice_actividad != -1:
            self.actividad_actual = indice_actividad
        actividadActual = self.actividades[self.actividad_actual]
        resp= self.adaptadorActividad.ver_gastos_actividad(actividadActual.nombreActividad)
        if resp.status == True:
            gastos = resp.result
        else:
            gastos = []
        self.vista_actividad = Vista_actividad(self)
        self.vista_actividad.mostrar_gastos_por_actividad(actividadActual, gastos)

    def insertar_gasto(self, nombreActividad):
        """
        Esta función inserta un gasto a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        gastos = self.adaptadorActividad.ver_gastos_actividad(nombreActividad).result
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividades[self.actividad_actual], gastos)

    def editar_gasto(self, nombreActividad):
        """
        Esta función edita un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        gastos = self.adaptadorActividad.ver_gastos_actividad(nombreActividad).result
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividades[self.actividad_actual], gastos)

    def eliminar_gasto(self, indice):
        """
        Esta función elimina un gasto de una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.gastos.pop(indice)
        self.vista_actividad.mostrar_gastos_por_actividad(self.actividades[self.actividad_actual], self.logica.gastos)

    def mostrar_reporte_compensacion(self, nombreActividad):
        """
        Esta función muestra la ventana del reporte de compensación
        """
        self.vista_reporte_comensacion = Vista_reporte_compensacion(self)
        self.vista_reporte_comensacion.mostrar_reporte_compensacion(self.logica.get_matriz_gastos_totales(nombreActividad))

    def mostrar_reporte_gastos_viajero(self, nombreActividad):
        """
        Esta función muestra el reporte de gastos consolidados
        """
        self.vista_reporte_gastos = Vista_reporte_gastos_viajero(self)
        self.vista_reporte_gastos.mostar_reporte_gastos(self.logica.get_gastos_consolidados(nombreActividad))

    def actualizar_viajeros(self, n_viajeros_en_actividad):
        """
        Esta función añade un viajero a una actividad en la lógica (debe modificarse cuando se construya la lógica)
        """
        self.logica.viajeros_en_actividad = n_viajeros_en_actividad

    def dar_viajeros(self):
        """
        Esta función pasa la lista de viajeros (debe implementarse como una lista de diccionarios o str)
        """
        viajeros = self.adaptadorActividad.get_viajeros().result
        return viajeros

    def dar_viajeros_en_actividad(self,actividad):
        """
        Esta función pasa los viajeros de una actividad (debe implementarse como una lista de diccionarios o str)
        """
        return actividad.viajeros

    def terminar_actividad(self, indice):
        """
        Esta función permite terminar una actividad (debe implementarse)
        """
        pass