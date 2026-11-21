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

Pasaron 30 pruebas automatizadas, 24 unitarias y 6 sobre archivos reales.

Los 32 partidos de Boca coinciden con la referencia de AFA en rivales, localía y marcadores. El playoff contra Huracán está excluido.

Los 480 partidos coinciden con RSSSF en jornada, localía, fecha de juego y marcador.

Quedan pendientes la revisión de las asignaciones de los DT y los criterios oficiales de desempate.

Ver [fuentes y trazabilidad](docs/fuentes.md).

## Entorno de desarrollo

La [guía del entorno](docs/entorno.md) describe la configuración en Windows y los pasos para reproducirla.

Las versiones de las dependencias están registradas en [requirements.txt](requirements.txt).
