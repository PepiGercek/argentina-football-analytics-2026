import pandas as pd


def resumen_equipo(partidos: pd.DataFrame, equipo: str) -> dict[str, int]:
    """Calcula el balance de un equipo en los partidos recibidos.

    La temporada, el torneo y la fase deben filtrarse antes de llamar
    a esta función. El nombre del equipo se compara de forma exacta.
    """
    columnas = ["local", "visitante", "goles_local", "goles_visitante"]
    faltantes = sorted(set(columnas) - set(partidos.columns))

    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    local = partidos["local"].eq(equipo)
    visitante = partidos["visitante"].eq(equipo)

    if (local & visitante).any():
        raise ValueError("Un equipo no puede enfrentarse a sí mismo.")

    seleccion = partidos.loc[local | visitante]

    if seleccion.empty:
        raise ValueError(f"No se encontraron partidos para {equipo!r}.")

    goles = seleccion[["goles_local", "goles_visitante"]].apply(
        pd.to_numeric, errors="raise"
    )

    invalidos = (
        goles.isna().any().any()
        or goles.lt(0).any().any()
        or goles.mod(1).ne(0).any().any()
    )

    if invalidos:
        raise ValueError(
            "Los goles deben ser completos, enteros y no negativos."
        )

    es_local = seleccion["local"].eq(equipo)
    gf = goles["goles_local"].where(es_local, goles["goles_visitante"])
    gc = goles["goles_visitante"].where(es_local, goles["goles_local"])

    pg = int(gf.gt(gc).sum())
    pe = int(gf.eq(gc).sum())
    pp = int(gf.lt(gc).sum())

    return {
        "PJ": len(seleccion),
        "PG": pg,
        "PE": pe,
        "PP": pp,
        "PTS": 3 * pg + pe,
        "GF": int(gf.sum()),
        "GC": int(gc.sum()),
    }
