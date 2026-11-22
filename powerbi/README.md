# LPF 2026 en Power BI

El informe tiene dos páginas. **Rendimiento por equipo** muestra partidos, puntos, goles y su evolución por fecha de juego. **Tabla anual** muestra la clasificación validada de los 30 clubes.

## Preparar los datos

Desde la raíz del proyecto, con el [entorno configurado](../docs/entorno.md) y el CSV de resultados disponible, ejecutar estos comandos en orden.

    .\.venv\Scripts\python.exe .\sql\cargar_partidos.py
    .\.venv\Scripts\python.exe .\powerbi\exportar_modelo.py

En Power BI Desktop, importar como Texto o CSV los tres archivos de `data/processed/powerbi`.

| Tabla | Filas | Qué contiene |
| --- | ---: | --- |
| `partidos_equipo` | 960 | Dos participaciones por encuentro, con un `partido_id` compartido |
| `equipos` | 30 | Una fila por club y su posición final en la tabla anual |
| `calendario` | 365 | Una fila por día de 2026 |

## Configurar el modelo

Cargar `calendario[fecha]` y `partidos_equipo[fecha_jugada]` con tipo **Fecha**. Usar números enteros para los puntos, los goles y la posición anual.

Crear o verificar dos relaciones activas de uno a varios, con filtro único desde `equipos` y `calendario` hacia `partidos_equipo`.

- `equipos[equipo]` → `partidos_equipo[equipo]`
- `calendario[fecha]` → `partidos_equipo[fecha_jugada]`

Crear las medidas de [medidas.dax](medidas.dax) una por una en `partidos_equipo`. La medida `Partidos` cuenta identificadores distintos. Para la línea de puntos acumulados, usar `calendario[fecha]` como eje diario. La posición anual se toma de `equipos[posicion_anual]` y conserva el orden validado de cierre.

## Comprobar el informe

- La tarjeta de partidos muestra **480** con los filtros limpios.
- Al seleccionar Boca Juniors, muestra **32 partidos, 63 puntos, 46 goles a favor y 23 en contra**.
- Con Boca filtrado por torneo, muestra **30 puntos** en Apertura y **33** en Clausura.
- La tabla anual tiene 30 clubes y comienza con Boca en el puesto 1.

La copia local del informe se guarda en `data/processed/powerbi/LPF_2026.pbix`.

Resultados de [Osvaldo José Gorgazzi / RSSSF, Argentina 2026](https://www.rsssf.org/tablesa/arg2026.html). Ver [fuentes y trazabilidad](../docs/fuentes.md).
