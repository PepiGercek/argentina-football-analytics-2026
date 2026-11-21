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
- Cotejo individual con la copia de AFA: 32 coincidencias en rival, condición, GF y GC; cero partidos faltantes.
- Playoff de octavos contra Huracán excluido de la referencia anual.
- Ejecución del 2026-11-19: 28 tests aprobados (24 unitarios y 4 sobre archivos reales), sin omisiones.

### Validación de los 480 partidos y la tabla anual

- Los mismos 30 equipos tienen 16 partidos en cada torneo. Las 960 combinaciones de torneo, jornada y equipo aparecen exactamente una vez.
- Los 480 marcadores tienen goles enteros, completos y no negativos. Los puntos guardados coinciden con los recalculados desde los goles en todos los partidos.
- Las 480 filas conservan el enlace de RSSSF y el crédito «Osvaldo José Gorgazzi / RSSSF».
- Los 30 balances calculados coinciden con Cómo Salió en PTS, PJ, PG, PE, PP, GF, GC y diferencia de gol.
- El cotejo por equipo se puede repetir con la prueba de `tests/test_tabla_anual.py`. El 2026-11-21 pasaron las 29 pruebas de la suite, sin omisiones.

La copia de Cómo Salió utilizada se guardó en `data/raw/comosalio_tabla_anual_2026.html`. Pesa 39659 bytes y su SHA256 es `df426d200ccfa248986300e3c2303dcf059f8ccc42abdeb134710af7e094ec7c`.

Las equivalencias de nombres están en `src/lpf_analytics/fuentes.py`. El lector conserva el nombre publicado junto al nombre utilizado en el CSV.

### Fechas de juego y marcadores según RSSSF

La copia utilizada está en `data/raw/rsssf_argentina_2026.html`. Tiene 111939 bytes y su SHA256 es `96fbac67f0a2e8eb573ff8418629e1ef447f6545c03c16d5a0edab915cdb7383`.

El lector `src/lpf_analytics/rsssf.py` extrae las fases de zonas desde el encabezado `Phase of groups` hasta la línea anterior a `Tie break:`. Conserva los nombres de RSSSF y sus equivalencias en el CSV.

El cruce por torneo, jornada, local y visitante emparejó los 480 partidos. En todos coincidieron la fecha jugada y los goles de ambos equipos. La prueba `tests/test_rsssf.py` permite repetir el cotejo. La suite pasó las 30 pruebas, sin omisiones.

`fecha` indica la jornada del torneo y `fecha_jugada` indica el día del partido. Por ejemplo, Boca jugó la jornada 9 del Apertura el 2 de mayo, después de la jornada 16 del 23 de abril. Para una evolución cronológica de puntos se usa `fecha_jugada`.

## Controles pendientes




- Revisar las fuentes y las asignaciones de los DT.
- Verificar el criterio oficial de desempate antes de reproducir el orden de clasificación.


## Referencia y equivalencias para el cotejo con AFA

### Copia consultada

- Archivo: data/raw/afa_boca_2026.html.
- Descarga: 2026-11-18.
- Tamaño: 65618 bytes.
- SHA256: cd727a81a68d3c4a1e7b261d57a621de6bc3daf3e1afc80c97d465f2231f9f62.

Se conservaron 16 jornadas de cada torneo: 32 partidos en total.
La fila de octavos de final contra Huracán quedó excluida.

### Equivalencias de nombres

Estas reglas corresponden a los rivales de los partidos de zonas de Boca 2026 publicados por AFA.

| Nombre en AFA | Nombre utilizado en el CSV |
| --- | --- |
| Estudiantes de La Plata | Estudiantes (La Plata) |
| Gimnasia y Esgrima | Gimnasia (Mendoza) |
| Talleres (C) | Talleres (Córdoba) |

La equivalencia de Gimnasia se contrastó con RSSSF el 2026-11-18: la fecha 8 del Apertura registra Boca 1-1 CA Gimnasia y Esgrima, el 2026-02-28. La compilación identifica a ese club con sede en Mendoza y distingue al club de La Plata.

RSSSF también identifica al Club Atlético Talleres con sede en Córdoba.

Referencia: https://www.rsssf.org/tablesa/arg2026.html

El cotejo conservará el nombre original de AFA junto al nombre normalizado, para mantener la trazabilidad.
