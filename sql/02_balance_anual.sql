WITH participaciones AS (
    SELECT local AS equipo, goles_local AS gf, goles_visitante AS gc
    FROM partidos

    UNION ALL

    SELECT visitante AS equipo, goles_visitante AS gf, goles_local AS gc
    FROM partidos
)
SELECT
    equipo AS Equipo,
    COUNT(*) AS PJ,
    SUM(CASE WHEN gf > gc THEN 1 ELSE 0 END) AS PG,
    SUM(CASE WHEN gf = gc THEN 1 ELSE 0 END) AS PE,
    SUM(CASE WHEN gf < gc THEN 1 ELSE 0 END) AS PP,
    SUM(CASE WHEN gf > gc THEN 3 WHEN gf = gc THEN 1 ELSE 0 END) AS PTS,
    SUM(gf) AS GF,
    SUM(gc) AS GC,
    SUM(gf) - SUM(gc) AS DG
FROM participaciones
GROUP BY equipo
ORDER BY equipo;
