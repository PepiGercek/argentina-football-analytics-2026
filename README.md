# LPF 2026 | Radiografía del fútbol argentino

Proyecto personal de portfolio para analizar a los 30 equipos de la Liga Profesional Argentina 2026.

El informe especial sobre Boca Juniors incluirá una comparación de los ciclos de Claudio Úbeda y Rodolfo Arruabarrena, con fechas y resultados sujetos a verificación.

## Primera entrega

1. Documentar la procedencia, cobertura y permisos de uso de LPF_2026_partidos.csv.
2. Revisar y validar los resultados de Boca que correspondan a la tabla anual.
3. Ampliar la validación a las fases de zonas del Apertura y el Clausura, excluyendo los playoffs.

Referencias iniciales aportadas para contrastar con los datos:
- Boca: 32 partidos, 17 victorias, 12 empates y 3 derrotas.
- Balance esperado: 63 puntos, 46 goles a favor y 23 en contra.
- Cobertura total esperada: 480 partidos.

Los conteos por torneo y el balance anual de los 30 equipos ya fueron comprobados.

## Análisis previstos

- EDA, tabla anual y evolución por fecha.
- Comparación entre Apertura y Clausura.
- Rendimiento ofensivo y defensivo.
- xG, xGA y xPTS, sujetos a disponibilidad y metodología documentada.
- Formaciones, estilos de juego, mapas de remates y scouting.
- Estadística aplicada, machine learning y clustering.
- Dashboard en Power BI.

## Criterios de trabajo

- Usar exclusivamente datos públicos o autorizados.
- Mantener independencia de los recursos privados del trabajo.
- Documentar fuentes, cobertura, permisos y decisiones metodológicas.
- Conservar los archivos originales sin editar.
- Validar los cálculos mediante tests.
- Registrar avances con issues y commits.
- No inventar datos ni métricas.

## Herramientas

Python, SQL, Jupyter Notebooks, Git, GitHub y Power BI.
Entorno local: Windows, VS Code y PowerShell.

## Estado

La base local contiene 480 partidos de zonas, 240 por torneo. Los balances de los 30 equipos coinciden con la tabla anual de Cómo Salió.

Balance agregado de Boca comprobado desde los marcadores.

Pasaron 36 pruebas automatizadas, 25 unitarias y 11 sobre archivos reales.

Los 32 partidos de Boca coinciden con la referencia de AFA en rivales, localía y marcadores. El playoff contra Huracán está excluido.

Los 480 partidos coinciden con RSSSF en jornada, localía, fecha de juego y marcador.

El [notebook de Boca](notebooks/01_boca_ciclos_2026.ipynb) compara los 16 partidos de zonas de cada ciclo. Boca pasó de 30 a 33 puntos. Sumó 8 puntos más de local y 5 menos de visitante.

Los 30 puestos de la tabla anual coinciden con RSSSF. Para el empate entre Independiente y Defensa y Justicia, el cálculo incorpora el orden publicado por RSSSF según el criterio de Fair Play.

Ver [fuentes y trazabilidad](docs/fuentes.md).

## Evolución de puntos

![Puntos acumulados de Boca Juniors, Rosario Central y Argentinos Juniors por fecha de juego](reports/evolucion_puntos_top3_2026.png)

El gráfico sigue a los tres primeros de la tabla anual. Cada equipo suma sus puntos el día en que disputó el partido, incluso cuando se reprogramó la jornada. El [script de generación](reports/generar_evolucion_puntos_top3.py) permite repetir el cálculo y regenerar el PNG.

## Apertura vs. Clausura

El [notebook de comparación](notebooks/02_apertura_vs_clausura_2026.ipynb) reúne los puntos y goles de los 30 equipos en ambos torneos. El [gráfico de cambios en puntos](reports/apertura_vs_clausura_2026.png) muestra que Instituto registró la mayor suba (+13) y Estudiantes de La Plata la mayor caída (−15).

## Resultados en SQL

La base SQLite se genera a partir de los 480 partidos validados. La [consulta de balance anual](sql/02_balance_anual.sql) recalcula los resultados de los 30 clubes y una prueba confirma que coinciden con pandas. La [guía del entorno](docs/entorno.md#base-sqlite) explica cómo reconstruir la base y ejecutar el control.

## Power BI

El informe incluye **Rendimiento por equipo**, con filtros por club y torneo, indicadores y evolución de puntos, y **Tabla anual**, con la clasificación de los 30 clubes.

La [guía de Power BI](powerbi/README.md) explica cómo exportar los datos desde SQLite, relacionar las tablas y recrear las medidas DAX del informe.

![Informe de Power BI con Boca Juniors seleccionado. 32 partidos, 63 puntos, 46 goles a favor y 23 en contra.](reports/powerbi_rendimiento_boca_2026.png)
 
## Entorno de desarrollo

La [guía del entorno](docs/entorno.md) describe la configuración en Windows y los pasos para reproducirla.

Las versiones de las dependencias están registradas en [requirements.txt](requirements.txt).
