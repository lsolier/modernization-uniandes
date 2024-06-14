
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Viajero(Base):
    __tablename__= 'viajero'

    id = Column(Integer, primary_key= True)
    nombre= Column(String(250))
    apellido= Column(String(250))
    identificadorViajero = Column(String(250))
    actividades = relationship('Actividad', secondary='actividades_viajero')
    gastos = relationship('Gasto', secondary='gasto_viajero')

class ActividadViajero(Base):
    __tablename__ = 'actividades_viajero'

    viajero_id = Column(
        String,
        ForeignKey('viajero.id'),
        primary_key=True)

    actividad_id = Column(
        String,
        ForeignKey('actividad.nombreActividad'),
        primary_key=True)

class GastoViajero(Base):
    __tablename__ = 'gasto_viajero'

    viajero_id = Column(
        String,
        ForeignKey('viajero.id'),
        primary_key=True)

    gasto_id = Column(
        String,
        ForeignKey('gasto.id'),
        primary_key=True)
