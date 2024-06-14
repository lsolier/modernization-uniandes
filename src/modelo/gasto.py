

from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from .declarative_base import Base


class Gasto(Base):

    __tablename__ = "gasto"

    id = Column(Integer, primary_key= True)
    fechaGasto = Column(Date)
    concepto = Column(String)
    valorGasto= Column(Float)
    viajero= relationship('Viajero', secondary='gasto_viajero')

class ActividadGasto(Base):

    __tablename__ = "actividades_gasto"

    gasto_id = Column(
        String,
        ForeignKey('gasto.id'),
        primary_key=True)
    actividad_id = Column(
        String,
        ForeignKey('actividad.nombreActividad'),
        primary_key=True)