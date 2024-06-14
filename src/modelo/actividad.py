
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .declarative_base import Base


class Actividad(Base):

    __tablename__ = "actividad"

    nombreActividad = Column(String(250), primary_key= True)
    estadoActividad = Column(Boolean)
    viajeros = relationship('Viajero', secondary='actividades_viajero')
    gastos = relationship('Gasto', secondary='actividades_gasto')
