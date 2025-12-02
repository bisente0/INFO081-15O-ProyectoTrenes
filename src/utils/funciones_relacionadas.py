import json, datetime
from ..logic.state.sim_state import estado
from ...data.estaciones.ent_estacion import *
from ...data.trenes.ent_trenes import *
from ...data.rutas.ent_rutas import *
from ...data.personas.personas import *



class JSON_Encoder(json.JSONEncoder):
    '''
    Encoder que será llamado al momento de interacción PYTHON a JSON
    Evitamos un TypeError al manipular instancias dentro de instancias
    '''

    def default(self, obj) -> dict:
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
    
def json_decoder(d: dict) -> object:
    '''
    Decodificador para pasar de JSON a PYTHON
    '''

    if "__type__" not in d:
        return d

    t = d["__type__"]

    if t == "tren":
        return Tren(**{k: atributo for k, atributo in Tren.items() if k != "__type__"})
    elif t == "estacion":
        return Estacion(**{k: atributo for k, atributo in Estacion.items() if k!= "__type__"})
    elif t == "ruta":
        return Ruta(**{k: atributo for k, atributo in Ruta.items() if k != "__type__"})
    elif t == "persona":
        return Persona(**{k: atributo for k, atributo in Persona.items() if k != "__type__"})
    elif t == "estado":
        return estado(**{k: atributo for k, atributo in estado.items() if k != "__type__"})

def diff_jsonfiles(f1: object, f2: object) -> bool:
    '''
    Función que analiza la diferencia entre dos archivos
    JSON. Retorna True si son iguales, False si son distintos.
    '''
    from deepdiff import DeepDiff

    diff = DeepDiff(JSON_Encoder(f1), 
                    JSON_Encoder(f2), 
                    ignore_order=True,
                    view=dict
                    )
    if diff:
        return True
    return False



    
class datos_corruptos(Exception):
    ''''
    Excepción que exclama la corrupción de datos por los siguientes motivos:
    sintáxis inválida, archivo incompleto, coherencia de datos y/o existencia.
    '''

    def __init__(self,
                  state: estado,
                  message="El estado se encuentra corrupto"):
        self.estado = state
        self.message = message
        super().__init__(self.message)