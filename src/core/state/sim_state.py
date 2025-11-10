from datetime import time, datetime
import queue

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
        pass

    def reset(self, path=".../data") -> None:
        pass

    # Actualizar el estado de la simulación dado un tickrate
    def update(self, dt: int) -> None:
        self.hora_actual += dt
        for tren in self.trenes_disp:
            tren.mover(dt)
        # Generar clientes

    # En caso de corrupción, guardado, etcétera...
    def reporte_estado(self, path=".../config/logs"):
        pass

    # Para interacción con UI
    def pausar(self):
        pass
    
    def resumir(self):
        pass

    