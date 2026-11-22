CREATE TABLE partidos (
    temporada INTEGER NOT NULL CHECK (temporada = 2026),
    torneo TEXT NOT NULL CHECK (torneo IN ('Apertura', 'Clausura')),
    fecha INTEGER NOT NULL CHECK (fecha BETWEEN 1 AND 16),
    fecha_jugada TEXT NOT NULL,
    local TEXT NOT NULL,
    visitante TEXT NOT NULL,
    goles_local INTEGER NOT NULL CHECK (goles_local >= 0),
    goles_visitante INTEGER NOT NULL CHECK (goles_visitante >= 0),
    dt_boca TEXT,
    fuente_dt_boca TEXT,
    fuente_resultado TEXT NOT NULL,
    credito_resultado TEXT NOT NULL,
    PRIMARY KEY (temporada, torneo, fecha, local, visitante),
    CHECK (local <> visitante)
);
