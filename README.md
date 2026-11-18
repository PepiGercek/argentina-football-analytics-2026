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

El balance agregado de Boca y los conteos por torneo ya fueron comprobados. La validación completa continúa en curso.

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

Base local incorporada: 480 registros, repartidos en 240 por torneo.

Balance agregado de Boca comprobado desde los marcadores.

Pruebas automatizadas: 14 aprobadas, incluidas 2 sobre el CSV real.

Continúan pendientes el cotejo individual con AFA, las fechas jugadas, los DT y la validación del resto de los equipos.

Ver [fuentes y trazabilidad](docs/fuentes.md).

## Entorno de desarrollo

La [guía del entorno](docs/entorno.md) describe la configuración en Windows y los pasos para reproducirla.

Las versiones de las dependencias están registradas en [requirements.txt](requirements.txt).
