# Entorno de desarrollo

## Configuración utilizada

- Sistema operativo: Windows.
- Editor: VS Code.
- Terminal: PowerShell.
- Python: 3.14.8.
- Git: 2.55.0.windows.5.
- pip del entorno virtual: 26.2.1.

## Dependencias iniciales

- pandas 3.1.1: lectura y análisis de tablas.
- ipykernel 7.4.0: ejecución de Python en notebooks.
- pytest 9.2.0: pruebas de validación.

requirements.txt registra las versiones exactas de los paquetes instalados, incluidas sus dependencias.

## Decisión sobre el entorno virtual

Las dependencias se instalan dentro de .venv, carpeta excluida de Git.

PowerShell bloqueó el script Activate.ps1 por su política de ejecución.
Los comandos del proyecto invocan directamente .\.venv\Scripts\python.exe.

## Reproducir el entorno en Windows

Ejecutar desde la raíz del proyecto, con Python 3.14 instalado.

1. Crear el entorno virtual:

       py -3.14 -m venv .venv

2. Instalar las versiones registradas desde el índice público PyPI:

       .\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple -r requirements.txt

3. Comprobar los requisitos de los paquetes:

       .\.venv\Scripts\python.exe -m pip check

## Comprobaciones realizadas

- pip check devolvió: No broken requirements found.
- pandas, ipykernel y pytest se importaron correctamente desde el entorno virtual.

En VS Code se seleccionó .venv como intérprete del proyecto y como kernel del notebook. Una celda con sys.executable confirmó el uso del Python del entorno virtual.

## Paquete del proyecto y pruebas

requirements.txt fija las versiones de las dependencias externas.

Después de instalar esas dependencias, instalar el paquete local desde la raíz del proyecto:

    .\.venv\Scripts\python.exe -m pip install --index-url https://pypi.org/simple --no-deps -e .

El modo editable permite importar lpf_analytics desde los tests y notebooks, utilizando el código de src.

Ejecutar todas las pruebas:

    .\.venv\Scripts\python.exe -m pytest -v -ra

Las pruebas unitarias usan partidos ficticios, identificados como tales.

Los controles sobre datos reales requieren data/raw/LPF_2026_partidos.csv. Si falta ese archivo, esas pruebas se indican como omitidas y se informa el motivo.
