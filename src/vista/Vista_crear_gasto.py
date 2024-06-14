from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from functools import partial
from datetime import date, datetime

from src.logica.adaptador_actividad import AdaptadorActividad
from src.modelo.gasto import Gasto


class Dialogo_crear_gasto(QDialog):
    #Diálogo para crear o editar un gasto

    def __init__(self,viajeros, gasto, actividad):
        """
        Constructor del diálogo
        """   
        super().__init__()

        self.adaptadorActividad = AdaptadorActividad()
        self.setFixedSize(340, 250)
        self.setWindowIcon(QIcon("src/devcuentasclaras/recursos/smallLogo.png"))
        self.nombreActividad = actividad
        self.resultado = ""
        self.viajeros = viajeros
        self.isEdicion = False
        self.gasto = Gasto()
        self.widget_lista = QListWidget()
        

        distribuidor_dialogo = QGridLayout()
        self.setLayout(distribuidor_dialogo)
        numero_fila=0
        
        #Si el diálogo se usa para crear o editar, el título cambia.

        titulo=""
        if(gasto==None):
            titulo="Nuevo Gasto"
        else:
            titulo="Editar Gasto"
            self.isEdicion= True
            self.gasto = gasto
      

        self.setWindowTitle(titulo)

        #Creación de las etiquetas y campos de texto

        etiqueta_concepto=QLabel("Concepto")
        distribuidor_dialogo.addWidget(etiqueta_concepto,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_concepto=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_concepto,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_fecha=QLabel("Fecha")
        distribuidor_dialogo.addWidget(etiqueta_fecha,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        #Campo fecha es un elemento especial para modificar fechas
        self.campo_fecha=QDateEdit(self)
        distribuidor_dialogo.addWidget(self.campo_fecha,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_valor=QLabel("Valor")
        distribuidor_dialogo.addWidget(etiqueta_valor,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        self.texto_valor=QLineEdit(self)
        distribuidor_dialogo.addWidget(self.texto_valor,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        etiqueta_viajero=QLabel("Viajero")
        distribuidor_dialogo.addWidget(etiqueta_viajero,numero_fila,0,1,3)                
        numero_fila=numero_fila+1

        
        self.lista_viajeros = QComboBox(self)

        for viajero in viajeros:
            self.lista_viajeros.addItem(viajero.identificadorViajero)
        
             
        distribuidor_dialogo.addWidget(self.lista_viajeros,numero_fila,0,1,3)
        numero_fila=numero_fila+1

        #Creación de los botones para guardar o cancelar

        self.btn_guardar = QPushButton("Guardar")
        distribuidor_dialogo.addWidget(self.btn_guardar ,numero_fila,1)
        self.btn_guardar.clicked.connect(self.guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        distribuidor_dialogo.addWidget(self.btn_cancelar ,numero_fila,2)
        self.btn_cancelar.clicked.connect(self.cancelar)

        #Si el diálogo se usa para editar, se debe poblar con la información del gasto a editar
        if gasto != None:
            self.texto_concepto.setText(gasto.concepto)
            self.campo_fecha.setDate(QDate.fromString(str(gasto.fechaGasto),"dd-MM-yyyy"))
            self.texto_valor.setText(str(gasto.valorGasto))
            indice = self.lista_viajeros.findText(gasto.viajero[0].identificadorViajero)
            self.lista_viajeros.setCurrentIndex(indice)

    def validar_campos(self):
        reason = ""
        if self.campo_fecha.date() == "" or self.campo_fecha.date() > date.today() :
            reason = "Fecha erronea"
        if self.texto_concepto.text() == "" :
            reason = "concepto esta vacio"
        if self.texto_valor.text() == "" or float(self.texto_valor.text()) <= 0:
            reason = "Valor no puede ser vacio o cero"

        return reason




    
    def guardar(self):
        """
        Esta función envía la información de que se han guardado los cambios
        """
        viajero = self.adaptadorActividad.get_viajero(self.lista_viajeros.currentText()).result

        razon = self.validar_campos()
        if razon != "":
            msg = QMessageBox()
            msg.setWindowTitle("Error con Gasto")
            msg.setText(razon)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        else:
            self.gasto.fechaGasto = self.campo_fecha.date().toPyDate()
            self.gasto.concepto = self.texto_concepto.text()
            self.gasto.valorGasto= float(self.texto_valor.text())
            self.gasto.viajero = [viajero]

            if self.isEdicion == True:
                self.adaptadorActividad.editar_gasto(self.nombreActividad, self.gasto)
            else:
                self.adaptadorActividad.add_gasto_actividad(self.nombreActividad,self.gasto)

        self.resultado=1
        self.close()
        return self.resultado


    def cancelar(self):
        """
        Esta función envía la información de que se ha cancelado la operación
        """   
        self.resultado=0
        self.close()
        return self.resultado

