# INFO081-15O-ProyectoTrenes

## CONTEXTO

&ensp; La empresa de <mark>Ferrocarriles del Estado de Chile (EFE)</mark> presenta una necesidad que nace de una nueva posible inversión en la cuál se plantean nuevas rutas, incorpora nuevos trenes y estaciones con distintas capacidades.

&ensp; Para esto, la empresa requiere de <mark>una aplicación capaz de simular a tiempo real, el comportamiento de trenes</mark>, que pueden ser manipulados a discreción del operario (usuario), considerando diversos aspectos como puede ser la generación de personas, estaciones, trenes rutas, restricciones, etcétera...

## INTEGRANTES

- Gabriel Poblete
- Vicente Rojas
- Francisco Carmona
- Vicente Osorio

## INDICADORES

&ensp; Los indicadores son guías de carácter cualitativo o cuantitativo, que le permiten al operario tomar decisiones rápidas para mejorar el flujo de ferroviario.

### Sugerencia de próximo movimiento

&ensp; Con el fin de buscar un funcionamiento óptimo, sin romper el programa, se propone que durante el juego y tras un turno, exista un 'in-page' no invasivo que recomiende el <mark> próximo movimiento más eficiente. </mark>

### Énfasis en flujos altamente densos

&ensp; Dado un flujo concentrado, el cuál será calculado dependiendo de la población y la generación de personas, al momento de interactuar con la estación o tren, la cantidad de flujo acumulado se verá resaltado, de manera que el operario perciba la deficiencia y busque una solución dentro del simulador.

## PERSISTENCIA DE DATOS

&ensp; Cómo equipo, decidimos basar la lógica general en PYTHON, todo lo que tenga que ver con texto a interactuar en el programa principal (control de estados, config...) será manejado a través de JSON, además, los documentos de lectura se manejarán con MARKDOWN.

&ensp; Planteamos tener, al menos, 4 carpetas principales, compuestas de la siguiente manera:

![Alt text](/assets/FILE_ORG0.png)

&ensp; Los archivos como 'config.json' o 'R01.json', guardarán la información considerada para su existencia, por ejemplo, para un tren necesitamos datos como nombre, velocidad, vagones... Por lo tanto, el archivo considera:

```json
{
    "NOMBRE_TREN" : "R01",
    "VELOCIDAD" : 120,
    "RUTA" : "R01",
    "VAGONES" : [5, 25],
    "FLUJO_ACUM" : 75,
    "ACTIVO" : true,
    "PASAJEROS" : [
        {
            "_comment": "Se establecen los atributos del objeto específicamente con el propósito de su comprensión, en real uso, sería el nombre del objeto/persona.",
            "ID" : "A001",
            "ORIGEN" : "E0",
            "CREACION" : "22:14",
            "DESTINO" : "E1",
            "REGRESO" : "14:02"
        }
    ]
}
```

&ensp; Teniendo esto claro, lo mismo aplica para los archivos de carácter similar, cómo sería 'E01.json' o 'R01.json'. Y para archivos como 'config.json':

```json
{
    "simulacion_default" : {
        "MAX_TRENES" : 18,
        "INTERVALO_AUTOSAVE" : 60,
        "VELOCIDAD_TIEMPO" : 1,
        "VELOCIDAD_DEFAULT" : true
    },
    "ARCHIVOS" : {
        "RUTAS" : ".../DATA/RUTAS",
        "ESTACIONES" : ".../DATA/ESTACIONES",
        "ESTADO" : ".../DATA/STATE",
        "TRENES" : ".../DATA/TRENES"
    },
    "DISPLAY" : {
        "TAMAÑO_VENTANA" : [1280, 720],
        "USAR_GUI" : true,
        "INFO_DEBUG" : false
    }
}
```

&ensp; Cabe destacar que, a medida que el programa es desarrollado, serán observados los aspectos considerados en el archivo.

## REQUISITOS

- Python 3.10+
- Tkinter (Usualmente viene instalado)

```bash
sudo apt-get install python3-tk

sudo dnf install python3-tkinter
```

## INICIALIZACIÓN

1. Ingresar a carpeta src

```bash
cd src
```

2. Ejecutar el archivo principal (main.py)

```bash
python main.py
```

&ensp; Tras haber ejecutado, se espera que el menú inicial sea visible.
