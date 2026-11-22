WITH base AS (
    SELECT
        printf('%d|%s|%02d|%s|%s', temporada, torneo, fecha, local, visitante)
            AS partido_id,
        temporada,
        torneo,
        fecha AS jornada,
        fecha_jugada,
        local,
        visitante,
        goles_local,
        goles_visitante,
        dt_boca
    FROM partidos
),
participaciones AS (
    SELECT
        partido_id, temporada, torneo, jornada, fecha_jugada,
        local AS equipo, visitante AS rival, 'Local' AS condicion,
        goles_local AS goles_favor, goles_visitante AS goles_contra,
        CASE WHEN local = 'Boca Juniors' THEN dt_boca END AS dt_equipo
    FROM base

    UNION ALL

    SELECT
        partido_id, temporada, torneo, jornada, fecha_jugada,
        visitante AS equipo, local AS rival, 'Visitante' AS condicion,
        goles_visitante AS goles_favor, goles_local AS goles_contra,
        CASE WHEN visitante = 'Boca Juniors' THEN dt_boca END AS dt_equipo
    FROM base
)
SELECT
    *,
    CASE
        WHEN goles_favor > goles_contra THEN 'G'
        WHEN goles_favor = goles_contra THEN 'E'
        ELSE 'P'
    END AS resultado,
    CASE
        WHEN goles_favor > goles_contra THEN 3
        WHEN goles_favor = goles_contra THEN 1
        ELSE 0
    END AS puntos
FROM participaciones
ORDER BY equipo, fecha_jugada, torneo, jornada;
