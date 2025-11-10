from ..estaciones.ent_estacion import Estacion
import datetime

class Persona:
    def __init__(self, id: int,
                origen: Estacion,
                creacion: datetime,
                destino: Estacion, 
                regreso: datetime):
        self.id = id
        self.origen = origen
        self.creacion = creacion
        self.destino = destino
        self.regreso = regreso

    def GenerarPersona(self):
        pass

    def id_random(self):
        pass

    ...