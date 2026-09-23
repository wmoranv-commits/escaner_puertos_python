# Scanner de Puertos TCP en Python

Aplicación de escritorio desarrollada en **Python** para realizar un escaneo de puertos TCP sobre una dirección IP determinada. El programa permite ingresar una dirección IP y un rango de puertos, ejecutar el análisis y visualizar los puertos abiertos junto con el progreso y un resumen del escaneo.

## Objetivo

Desarrollar una herramienta sencilla para apoyar el aprendizaje de conceptos básicos de redes, sockets TCP, validación de datos y programación con interfaces gráficas en Python.

## Funcionalidades

- Validación de la dirección IP ingresada.
- Validación del rango de puertos entre **1 y 65535**.
- Escaneo de puertos mediante conexiones TCP.
- Identificación y listado de puertos abiertos.
- Barra de progreso durante el escaneo.
- Resumen final con:
  - dirección IP analizada;
  - rango de puertos;
  - cantidad de puertos escaneados;
  - cantidad de puertos abiertos;
  - lista de puertos encontrados;
  - tiempo total del escaneo.
- Botones para iniciar, limpiar y salir de la aplicación.
- Ejecución del escaneo en un hilo separado para mantener la interfaz disponible.

## Requisitos

- Python 3.x
- Tkinter (normalmente incluido con Python)
- No requiere librerías externas adicionales.

## Ejecución

Desde la carpeta del proyecto:

```bash
python scanner_puertos.py
```

En algunos sistemas puede ser necesario utilizar:

```bash
python3 scanner_puertos.py
```

## Uso

1. Ingrese la dirección IP que desea analizar.
2. Especifique el puerto inicial.
3. Especifique el puerto final.
4. Presione **INICIAR ESCANEO**.
5. Observe el progreso y los puertos abiertos encontrados.
6. Al finalizar, revise el resumen del análisis.

Para pruebas locales se puede utilizar la dirección `127.0.0.1`.

## Estructura del repositorio

```text
scanner-puertos-python/
├── scanner_puertos.py
├── README.md
└── .gitignore
```

## Consideraciones de uso

Esta herramienta debe utilizarse únicamente sobre equipos, direcciones IP y redes para las que se tenga autorización. El escaneo de puertos sobre sistemas de terceros sin permiso puede estar restringido por políticas institucionales o por la legislación aplicable.

## Autoría

Proyecto académico desarrollado como parte de una actividad de programación y redes.
