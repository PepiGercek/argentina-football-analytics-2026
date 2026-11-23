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
- lxml 6.1.3: lectura de las tablas HTML de las fuentes.
- Matplotlib 3.11.2: gráficos de evolución.

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

## Regenerar el gráfico de evolución

Con el entorno configurado y `data/raw/LPF_2026_partidos.csv` disponible, ejecutar este comando desde la raíz del proyecto.

    .\.venv\Scripts\python.exe .\reports\generar_evolucion_puntos_top3.py

El script genera `reports/evolucion_puntos_top3_2026.png`.

## Base SQLite

El cargador usa el módulo `sqlite3` de Python. Desde la raíz del proyecto, con el CSV disponible en `data/raw/LPF_2026_partidos.csv`, ejecutar el siguiente comando.

    .\.venv\Scripts\python.exe .\sql\cargar_partidos.py

El cargador aplica el esquema de `sql/01_esquema.sql` y genera `data/processed/lpf_2026.sqlite3` después de comprobar que hay 240 partidos por torneo. La base generada queda excluida de Git.

La consulta `sql/02_balance_anual.sql` calcula partidos jugados, victorias, empates, derrotas, puntos y goles por equipo. Para cotejar los 30 balances con pandas, ejecutar esta prueba.

    .\.venv\Scripts\python.exe -m pytest tests/test_sql.py -q -ra

La prueba crea su propia base en memoria a partir del CSV y del mismo esquema.

## Reconstruir el CSV de resultados

Desde un clon nuevo, con el entorno virtual configurado, ejecutá estos pasos en PowerShell desde la raíz del proyecto.

1. Descargá una copia del HTML de RSSSF.

       Invoke-WebRequest -Uri "https://www.rsssf.org/tablesa/arg2026.html" -OutFile ".\data\raw\rsssf_argentina_2026.html" -UseBasicParsing

2. Generá el CSV en la ruta que usan los notebooks.

       .\.venv\Scripts\python.exe -m lpf_analytics.rsssf ".\data\raw\rsssf_argentina_2026.html" ".\data\raw\LPF_2026_partidos.csv"

El generador extrae los 480 partidos de zonas, normaliza los nombres y calcula los puntos a partir de los marcadores. El DT de Boca se asigna por torneo según el criterio documentado en [fuentes](fuentes.md). La reconstrucción se cotejó con el CSV original y coincidió en los 480 partidos y las 14 columnas.

Si ya tenés el CSV original, usá `data/processed/LPF_2026_partidos_reconstruido.csv` como ruta de salida para conservar ambas copias y poder cotejarlas. [Argentina 2026, Osvaldo José Gorgazzi / RSSSF](https://www.rsssf.org/tablesa/arg2026.html)