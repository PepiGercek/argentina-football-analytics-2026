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

### Ciclos técnicos de Boca en la tabla anual

- **Claudio Úbeda.** El CSV le asigna los 16 partidos de zonas del Apertura, del 25 de enero al 2 de mayo. Boca lo identifica como DT en el [debut ante Riestra](https://www.bocajuniors.com.ar/noticias/cabeza-y-corazon) y en el [cierre de zonas ante Central Córdoba](https://www.bocajuniors.com.ar/noticias/cierre-con-victoria). [DeporTV reproduce el anuncio de su salida del 2 de junio](https://deportv.gob.ar/futbol/boca-oficial-ubeda-entrenador-no-va-mas-nid:13887).
- **Rodolfo Arruabarrena.** El CSV le asigna los 16 partidos de zonas del Clausura, del 26 de julio al 7 de noviembre. Boca anunció su [nombramiento el 18 de junio](https://www.bocajuniors.com.ar/noticias/comunicado-oficial-2) y lo identifica como DT en el [debut ante Riestra](https://www.bocajuniors.com.ar/noticias/trabajare-para-pensar-en-chile) y en el [cierre ante Defensa y Justicia](https://www.bocajuniors.com.ar/noticias/campeones).

La asignación de las jornadas intermedias se infiere por continuidad del ciclo. La comparación describe el rendimiento de Boca durante cada período. Como cada ciclo coincide con un torneo distinto, las diferencias observadas también reflejan cambios entre Apertura y Clausura.

El [resumen de campaña de DeporTV](https://deportv.gob.ar/futbol/campana-boca-valio-titulo-liga-profesional-nid:18747) respalda el cambio de DT entre semestres. Para los marcadores se mantienen RSSSF y AFA como referencias. Por ejemplo, DeporTV da 2–0 ante Talleres en la jornada 13 del Clausura, mientras que AFA, RSSSF y Boca registran 2–1. [Crónica de Boca sobre el cierre del Clausura](https://www.bocajuniors.com.ar/noticias/campeones).

### Orden de la tabla anual y criterio de desempate

El [artículo 24 del reglamento de AFA](https://assets1.afa.com.ar/2026/BOLETINES/Boletin-Resoluciones-6818---Complementario-01---Reglamento-Torneos-LPF-Primera-2026.pdf#page=29) define el orden por puntos, diferencia de gol, goles a favor y Fair Play. Si persiste el empate, se recurre a un sorteo. Si la igualdad en puntos define un descenso, corresponde un desempate en cancha.

Independiente y Defensa y Justicia fueron los únicos clubes igualados en los tres criterios que se calculan desde los marcadores. Ambos terminaron con 47 puntos, +3 de diferencia y 39 goles a favor. El [Boletín 6974 de AFA, expediente 100253](https://assets1.afa.com.ar/2026/BOLETINES/Boletin-6974.-12.11.docx-%281%29.pdf#page=2), documenta cuatro sanciones al cuerpo técnico de Defensa tras el partido con Boca.

La [edición de RSSSF actualizada el 19 de noviembre](https://www.rsssf.org/tablesa/arg2026.html) ubica a Independiente 13.º y a Defensa y Justicia 14.º. La copia de Cómo Salió los mostraba en orden inverso y se utilizó para contrastar sus balances por equipo. La consulta a RSSSF del 2026-11-22 devolvió el mismo SHA256 que la copia local `data/raw/rsssf_argentina_2026.html`.

La función `tabla_anual_2026` calcula los balances desde los marcadores y usa el orden publicado por RSSSF para ese empate. El cálculo de los puntajes de Fair Play requeriría los datos disciplinarios. El orden de los 30 equipos coincidió con RSSSF en `tests/test_clasificacion_anual.py`. El 2026-11-22 pasaron las 31 pruebas de la suite, sin omisiones.

## Controles pendientes




- Consultar las planillas individuales para verificar quién ocupó el banco en cada encuentro, si el análisis requiere ese nivel de detalle.



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

## Fuentes candidatas para datos avanzados

Consulta del 22 de noviembre de 2026. Seguimiento en el issue #1.

- **StrikerAPI.** Declara cobertura de remates geolocalizados con xG propio, formaciones y estadísticas de jugadores para la liga argentina. Sus términos permiten el análisis y la visualización en dashboards, y restringen la redistribución como archivo o dataset. Cobertura por partido pendiente de verificar. [Cobertura para Argentina](https://strikerapi.com/argentina-liga-profesional) · [Términos de uso](https://strikerapi.com/terms)
- **LPF Data.** El informe de cierre de Apertura incluye frecuencias de formaciones y el de Clausura publica xG promedio por equipo. Sirven como referencia agregada. Permisos de reutilización pendientes de confirmar. [Informe de Apertura](https://www.ligaprofesional.ar/wp-content/uploads/2026/05/LPF-Data-Fecha-16-Torneo-Apertura-Mercado-Libre-2026.pdf) · [Informe de Clausura](https://www.ligaprofesional.ar/wp-content/uploads/2026/11/LPF-Data-Prensa-Fecha-16.pdf)
- **Hudl StatsBomb Open Data.** El catálogo abierto lista las temporadas 1981 y 1997/98 para la liga argentina. [Catálogo de temporadas](https://github.com/hudl/open-data/blob/master/data/competitions.json)

### Cobertura de StrikerAPI para Boca

Se cotejaron los 32 partidos de zonas con el CSV de resultados por torneo, fecha de juego en Argentina, localía y marcador. La fecha local se obtuvo convirtiendo `starts_at` a `America/Argentina/Buenos_Aires`. Los 32 encuentros coincidieron.

Las dos consultas de remates por temporada se cruzaron con el listado de zonas mediante `game_id`. En los 32 partidos hubo remates con coordenadas y xG en ambos sentidos. El detalle incluye 434 remates de Boca y 323 de sus rivales. El listado de partidos y las dos consultas de temporada consumieron 22 créditos.

El xG registrado suma los valores de los remates disponibles de Boca. El xGA registrado aplica el mismo cálculo a los remates de sus rivales. La cobertura de 32/32 indica presencia de datos por partido. En el piloto del Apertura ante Deportivo Riestra, la API registró coordenadas y xG para 22 de los 25 remates informados.

En ese mismo piloto se comprobaron las formaciones iniciales y la presencia de estadísticas de jugadores. La cobertura de esos campos en el resto de la temporada queda pendiente.

### Mapa de remates de Boca

El mapa muestra los remates con coordenadas y xG de los 32 partidos de zonas. Ambos paneles usan la misma orientación y escala. La media cancha es esquemática, con 68 m de ancho de referencia y el punto penal alineado con `x = 0.23` en las coordenadas de StrikerAPI. [Coordenadas de StrikerAPI](https://strikerapi.com/docs/get-shot-map) · [Dimensiones del terreno de juego](https://www.theifab.com/es/laws/latest/the-field-of-play/)

El [generador del mapa](../reports/generar_mapa_remates_boca.py) usa los JSON locales de partidos y remates a favor.