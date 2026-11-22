"""Evolución cronológica de puntos desde la perspectiva de cada equipo."""

import pandas as pd


def evolucion_equipos(partidos: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por equipo y partido, con sus puntos acumulados.

    Recibe los resultados validados del período que se quiere analizar.
    """
    columnas = [
        "torneo", "fecha", "fecha_jugada", "local", "visitante",
        "goles_local", "goles_visitante",
    ]
    faltantes = sorted(set(columnas) - set(partidos.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    base = partidos[columnas]
    locales = base.rename(columns={
        "local": "equipo", "visitante": "rival",
        "goles_local": "GF", "goles_visitante": "GC",
    }).assign(condicion="Local")
    visitantes = base.rename(columns={
        "visitante": "equipo", "local": "rival",
        "goles_visitante": "GF", "goles_local": "GC",
    }).assign(condicion="Visitante")

    evolucion = pd.concat([locales, visitantes], ignore_index=True)
    evolucion["fecha_jugada"] = pd.to_datetime(
        evolucion["fecha_jugada"], format="%Y-%m-%d"
    )
    if evolucion["fecha_jugada"].isna().any():
        raise ValueError("Hay partidos sin fecha de juego.")
    if evolucion.duplicated(["equipo", "fecha_jugada"]).any():
        raise ValueError("Un equipo aparece más de una vez el mismo día.")

    evolucion["puntos"] = (
        3 * evolucion["GF"].gt(evolucion["GC"]).astype(int)
        + evolucion["GF"].eq(evolucion["GC"]).astype(int)
    )
    evolucion = evolucion.sort_values(
        ["equipo", "fecha_jugada"], ignore_index=True
    )
    por_equipo = evolucion.groupby("equipo", sort=False)
    evolucion["partido_acumulado"] = por_equipo.cumcount() + 1
    evolucion["puntos_acumulados"] = por_equipo["puntos"].cumsum()
    return evolucion
