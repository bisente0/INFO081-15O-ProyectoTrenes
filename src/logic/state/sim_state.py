from datetime import time, datetime
from ...utils.funciones_relacionadas import JSON_Encoder
import queue, json


class estado:
    # Las personas serán accedidas a través de los trenes y estaciones.
    def __init__(self, 
                hora_actual: time,
                fecha: datetime,
                trenes_disp: tuple,
                estaciones_disp: tuple,
                rutas_disp: tuple,
                eventos_en_cola: queue.Queue,
                historial_eventos: dict):
        
        self.hora_actual = hora_actual
        self.fecha = fecha
        self.trenes_disp = trenes_disp
        self.estaciones_disp = estaciones_disp
        self.rutas_disp = rutas_disp
        self.eventos_en_cola = eventos_en_cola
        self.historial_eventos = historial_eventos
    
    # Analizar el atributo ingresado con un setter
    @property
    def hora_actual(self) -> None:
        return self._hora_actual

    @hora_actual.setter
    def hora_actual(self, tiempo: time) -> None:
        if tiempo < 0 or tiempo == None:
            raise ValueError("El tiempo no puede ser menor o igual a cero.")
        self._hora_actual = tiempo

    # Revisar la sintáxis del archivo, la coherencia en los datos, existencia...
    def verificar_integridad(self, path=".../data") -> bool:
        try:
            if (not self.estaciones_disp and self.trenes_disp) or (not self.rutas_disp and self.trenes_disp):
                print("Error en coherencia de datos")
                return False
            with open(path, mode="r", encoding="utf-8") as file:
                json.load(file)
            return True
        except FileNotFoundError as f:
            print(f"El archivo no se encontró en: {path}")
            return False
        except json.JSONDecodeError as j:
            print(f"Sintáxis JSON inválida en: {path} : {j}")
            return False

    def reset(self, path=".../data") -> None:
        pass

    # Actualizar el estado de la simulación dado un tickrate
    def update(self, dt: int) -> None:
        self.hora_actual += dt
        for tren in self.trenes_disp:
            tren.mover(dt)
        # Generar clientes

    # En caso de corrupción, guardado, etcétera...
    def reporte_estado(self, error, path=".../config/logs"):
        with open(path+f"/report_{self.fecha}.json", mode="w", encoding="utf-8" ) as report:
            json.load({
                "ERRROR" : f"{error}",
                "FECHA" : self.fecha,
                "HORA_ACTUAL" : self.hora_actual,
                "TRENES" : self.trenes_disp,
                "ESTACIONES" : self.estaciones_disp,
                "RUTAS" : self.rutas_disp,
                "EVENTOS_COLA" : self.eventos_en_cola,
                "HISTORIAL" : self.historial_eventos
                
            })


    # Para interacción con UI
    def pausar(self):
        pass
    
    def resumir(self):
        pass

    