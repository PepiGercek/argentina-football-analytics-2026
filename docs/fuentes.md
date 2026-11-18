# Fuentes y trazabilidad

## Archivo de entrada

- Archivo: data/raw/LPF_2026_partidos.csv.
- Procedencia declarada: generado por ChatGPT a partir de la compilación de RSSSF.
- Transformaciones declaradas: normalización de nombres y fechas, cálculo de puntos e incorporación del DT de Boca con su fuente.
- Consulta de las fuentes: 2026-11-17.
- SHA256 del original y de la copia:
  A8EC02ED7D8750727A7A7D2ECB2BD480D6E6A3B2EADC8AFC920C6F33DDF72A0B

El CSV es un archivo derivado. Su extracción y sus transformaciones deben auditarse.

## Fuente de los marcadores

[Argentina 2026 — RSSSF](https://www.rsssf.org/tablesa/arg2026.html).

- Compilador y autor: Osvaldo José Gorgazzi.
- Última actualización indicada en la página consultada: 2026-11-12.
- Nota de uso: permite copiar el documento completo o parcialmente dando el reconocimiento correspondiente al autor.
- La página conserva el aviso de copyright de Osvaldo José Gorgazzi y RSSSF.
- Crédito que debe conservarse: Osvaldo José Gorgazzi / RSSSF, acompañado del enlace original.

## Fuentes de contraste

### Tabla anual

[Cómo Salió — tabla anual](https://comosalio.com/t/arg.1/anual).

Referencia para contrastar los balances de los 30 equipos.
La página identifica la cobertura como Apertura más Clausura, sin playoffs.

### Partidos de Boca

[AFA — Boca se coronó campeón de la Liga 2026](https://www.afa.com.ar/es/posts/boca-se-corono-campeon-de-la-liga-2026).

Referencia para contrastar rivales, marcadores y localía de Boca.
El listado incluye también el partido de octavos del Apertura contra Huracán, que queda fuera del alcance de la tabla anual.

Los permisos de redistribución de contenidos de AFA y Cómo Salió quedan pendientes de revisión. En esta etapa se consultan para cotejar resultados.

## Controles realizados sobre el CSV

- La copia del proyecto tiene el mismo SHA256 que el archivo de Descargas.
- Se leyeron 480 registros y 14 columnas.
- Temporada 2026: 240 registros del Apertura y 240 del Clausura.
- Se identificaron 32 partidos de Boca Juniors.
- Se verificó que los goles de esos partidos fueran numéricos, completos, enteros y no negativos.
- Se recalculó el balance desde los marcadores: 17 victorias, 12 empates, 3 derrotas, 63 puntos, 46 GF y 23 GC.
- Balance de Boca verificado con la función resumen_equipo, en src/lpf_analytics/resultados.py.
- Ejecución del 2026-11-18: 14 tests aprobados (12 unitarios y 2 sobre el CSV real), sin omisiones.

## Controles pendientes


- Cotejar los 32 partidos de Boca con AFA y dejar una comprobación reproducible.
- Verificar las fechas jugadas y documentar su relación con las jornadas del torneo.
- Revisar las fuentes y las asignaciones de los DT.
- Revisar duplicados, cobertura y créditos de todos los registros.
- Recalcular los balances de los 30 equipos y contrastarlos con la tabla anual.
