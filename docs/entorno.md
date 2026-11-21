# Entorno de desarrollo

## Configuración utilizada

- Sistema operativo: Windows.
- Editor: VS Code.
- Terminal: PowerShell.
- Python: 3.14.8.
- Git: 2.55.0.windows.5.
- pip del entorno virtual: 26.2.1.

## Dependencias utilizadas

- pandas 3.1.1: lectura y análisis de tablas.
- ipykernel 7.4.0: ejecución de Python en notebooks.
- pytest 9.2.0: ejecución de pruebas automatizadas.
- lxml 6.1.3: lectura de las tablas HTML de AFA.

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

## Archivos de referencia para los controles reales

Las pruebas utilizan estos archivos locales:

- data/raw/LPF_2026_partidos.csv: base de resultados.
- data/raw/afa_boca_2026.html: copia de la página de AFA.
- data/raw/comosalio_tabla_anual_2026.html: copia de la tabla anual de Cómo Salió.
- data/raw/rsssf_argentina_2026.html: copia de la compilación Argentina 2026 de RSSSF.

Desde la raíz del proyecto se pueden descargar las referencias de AFA, Cómo Salió y RSSSF.

    Invoke-WebRequest -Uri "https://www.afa.com.ar/es/posts/boca-se-corono-campeon-de-la-liga-2026" -OutFile ".\data\raw\afa_boca_2026.html" -UseBasicParsing

    Invoke-WebRequest -Uri "https://comosalio.com/t/arg.1/anual" -OutFile ".\data\raw\comosalio_tabla_anual_2026.html" -UseBasicParsing

    Invoke-WebRequest -Uri "https://www.rsssf.org/tablesa/arg2026.html" -OutFile ".\data\raw\rsssf_argentina_2026.html" -UseBasicParsing

La trazabilidad de las copias utilizadas está documentada en [fuentes.md](fuentes.md).

Cuando falta un archivo requerido, la prueba correspondiente se indica como omitida y muestra el motivo. Las pruebas unitarias utilizan sus propios datos ficticios.
