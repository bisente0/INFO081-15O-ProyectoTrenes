import json
from datetime import datetime, timedelta


class EstadoSimulacion:
    def avanzar_tiempo(self, minutos):
        formato = "%Y-%m-%d %H:%M"
        dt = datetime.strptime(self.hora_actual, formato)
        dt += timedelta(minutes=minutos)
        self.hora_actual = dt.strftime(formato)

    def registrar_evento(self, descripcion):
        evento = {
            "hora": self.hora_actual,
            "descripcion": descripcion
        }
        self.eventos.append(evento)

    def __init__(self):
        self.hora_actual = "2015-03-01 07:00"
        self.estaciones = []
        self.rutas = []
        self.trenes = []
        self.eventos = []

    def guardar(self, archivo):
        estado = {
            "hora_actual": self.hora_actual,
            "estaciones": [vars(e) for e in self.estaciones],
            "rutas": [vars(r) for r in self.rutas],
            "trenes": [vars(t) for t in self.trenes],
            "eventos": self.eventos
        }
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(estado, f, ensure_ascii=False, indent=4)
