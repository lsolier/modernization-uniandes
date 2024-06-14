from src.modelo.declarative_base import Base, engine, session
from src.modelo.viajero import Viajero

class ControladorViajero:

    def __init__(self):
        super().__init__()
        Base.metadata.create_all(engine)

    def agregar_viajero(self, nombre, apellido):
        identificadorViajero = nombre+apellido
        viajero = session.query(Viajero).filter(Viajero.identificadorViajero == identificadorViajero).first()
        if viajero is None:
            viajero = Viajero(nombre=nombre,
                              apellido=apellido,
                              identificadorViajero=identificadorViajero)
            session.add(viajero)
            session.commit()
            return True
        else:
            return False

    def agregar_viajero_obj(self, viajeroObj):
        session.add(viajeroObj)
        session.commit()
        return True

    def editar_viajero(self, nombre, apellido, nuevoNombre, nuevoApellido):
        identificadorViajero = nombre + apellido
        nuevoIdentificadorViajero = nuevoNombre + nuevoApellido
        viajero = session.query(Viajero).filter(Viajero.identificadorViajero == identificadorViajero).first()
        if viajero is not None:
            viajero.nombre = nuevoNombre
            viajero.apellido = nuevoApellido
            viajero.identificadorViajero = nuevoIdentificadorViajero
            session.commit()
            return True
        else:
            return False

    def eliminar_viajero(self, nombre, apellido):
        identificadorViajero = nombre + apellido
        viajero = session.query(Viajero).filter(Viajero.identificadorViajero == identificadorViajero).first()
        if viajero is not None:
            session.delete(viajero)
            session.commit()
            return True
        else:
            return False

    def get_viajeros(self):
        viajeros = session.query(Viajero).all()
        if viajeros != None:
            return viajeros
        else:
            return []

    def get_viajero(self, nombre, apellido):
        identificadorViajero = nombre + apellido
        return session.query(Viajero).filter(Viajero.identificadorViajero == identificadorViajero).first()
    def get_viajero_id(self, identificadorViajero):
        return session.query(Viajero).filter(Viajero.identificadorViajero == identificadorViajero).first()
