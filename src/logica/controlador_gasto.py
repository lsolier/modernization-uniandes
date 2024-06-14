
from src.modelo.declarative_base import engine, Base, session
from src.modelo.gasto import Gasto


class ControladorGasto:

    def __init__(self):
        Base.metadata.create_all(engine)

    def add_gasto_obj(self,gasto):
        try:
            session.add(gasto)
            session.commit()
            return True
        except:
            return False

    def get_gasto(self, gastoId):
            gasto = session.query(Gasto).filter(Gasto.id == gastoId).first()
            return gasto

    def edit_gasto(self,gasto):
        try:
            dbGasto= session.query(Gasto).filter(Gasto.id == gasto.id).first()
            if dbGasto != None:
                dbGasto.fechaGasto = gasto.fechaGasto
                dbGasto.valorGasto = gasto.valorGasto
                dbGasto.viajero = gasto.viajero
                dbGasto.concepto = gasto.concepto
                session.commit()
                return True
            else:
                self.add_gasto_obj(gasto)
        except:
            return False
    def delete_gasto(self,gastoId):
        try:
            dbGasto = session.query(Gasto).filter(Gasto.id == gastoId).first()
            session.delete(dbGasto)
            session.commit()
            return True
        except:
            return False
    def delete_all_gastos(self):
        try:
            gastos= session.query(Gasto).all()
            if gastos != None :
                for gasto in gastos:
                    session.delete(gasto)
                session.commit()
            return True
        except:
            return False