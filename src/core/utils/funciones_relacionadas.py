import json, datetime
from ..state.sim_state import estado
from ....data.estaciones.ent_estacion import *
from ....data.trenes.ent_trenes import *
from ....data.rutas.ent_rutas import *
from ....data.personas.personas import *



class JSON_Encoder(json.JSONEncoder):
    # Encoder que será llamado al momento de interactuar con clases en nuestros archivos JSON
    # Evitamos un TypeError al manipular instancias dentro de instancias
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Tren):
            return {
                    "__type__" : "tren", 
                    "ID" : obj.id,
                    "VELOCIDAD" : obj.velocidad,
                    "VAGONES" : obj.vagones,
                    "FLUJO_ACUM" : obj.flujo_acum,
                    "ACTIVO" : obj.activo,
                    "PASAJEROS" : obj.pasajeros
                    }
        elif isinstance(obj, Estacion):
            return {
                    "__type__" : "estacion",
                    "NOMBRE" : obj.nombre,
                    "ID" : obj.id,
                    "POBLACION_TOTAL" : obj.poblacion,
                    "VIAS" : obj.vias,
                    "FLUJO_ACUM" : obj.flujo_acum
                    }
        elif isinstance(obj, Ruta):
            return {
                    "__type__" : "ruta",
                    "NOMBRE" : obj.nombre,
                    "ID" : obj.id,
                    "ORIGEN" : obj.origen,
                    "DESTINO" : obj.destino,
                    "LONGITUD" : obj.longitud
                    }
        elif isinstance(obj, estado):
            return {
                    "__type__" : "estado",
                    "HORA_ACTUAL" : obj.hora_actual,
                    "FECHA" : obj.fecha,
                    "TRENES_DISP" : obj.trenes_disp,
                    "ESTACIONES_DISP" : obj.estaciones_disp,
                    "RUTAS_DISP" : obj.rutas_disp,
                    "EVENTOS_EN_COLA" : obj.eventos_en_cola,
                    "PAUSA" : obj.pause
                    }
        elif isinstance(obj, Persona):
            return {
                    "__type__" : "persona",
                    "ID" : obj.id,
                    "ORIGEN" : obj.origen,
                    "FECHA_CREACION" : obj.creacion,
                    "DESTINO" : obj.destino,
                    "REGRESO" : obj.regreso
                    }
        # En caso de no saber cómo serializar la información levanta un TypeError (built-in)
        return super().default(obj)

class datos_corruptos(Exception):
    def __init__(self,
                  state: estado,
                  message="El estado se encuentra corrupto"):
        self.estado = state
        self.message = message
        super().__init__(self.message)