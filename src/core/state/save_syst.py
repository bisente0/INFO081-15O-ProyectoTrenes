from sim_state import state
from ..utils.funciones_relacionadas import JSON_Encoder, datos_corruptos
import json

class file_syst:
    def __init__(self, state: estado):
        self.estado = state

    # Antes de establecer el estado como atributo, verificar...
    @property
    def estado(self):
        return self.state
    
    @estado.setter
    def estado(self, state: estado):
        # Verificar si es estado DEFAULT antes de settear
        # Implica comparar con config_default y decidir dependiendo de los cambios realizados
        pass

    def guardar_sim(self, state: estado ,path="..../data/estado") -> None:
        #Función que usando el ENCODER en utils, escribe/reescribe el estado en data.
        with open(f"..../data/estado/{state.fecha}.json", mode="w", encoding="utf-8") as w_file:
            json.dump(JSON_Encoder.default(state), w_file)

    def cargar_sim(self, state: estado, path=".../data/estado") -> None:
        # Función que verifica integridad, en caso de que el archivo no esté corrupto,
        # recorre los atributos del estado y escribe/reescribe usando el ENCODER.
        if self.estado.verificar_integridad():
            with open("..../data/estaciones/estaciones.json", mode="a", encoding="utf-8") as w_file:
                for estacion in state.estaciones_disp:
                    json.dump(JSON_Encoder.default(estacion), w_file)
            with open("..../data/rutas/rutas.json", mode="a", encoding="utf-8") as w_file:
                for ruta in state.rutas_disp:
                    json.dump(JSON_Encoder.default(ruta), w_file)
            with open("..../data/personas/personas.json", mode="a", encoding="utf-8") as w_file:
                # Las personas están en un tren, o en una estación.
                for estacion in state.estaciones_disp:
                    json.dump(JSON_Encoder.default(estacion.personas), w_file)
                for tren in state.trenes_disp:
                    json.dump(JSON_Encoder.default(tren.personas), w_file)
            with open("..../data/trenes/trenes.json", mode="a", encoding="utf-8") as w_file:
                for tren in state.trenes_disp:
                    json.dump(JSON_Encoder.default(tren), w_file)
        else:
            raise datos_corruptos(state)