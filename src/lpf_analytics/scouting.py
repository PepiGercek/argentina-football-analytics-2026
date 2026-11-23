"""Indicadores de remate por jugador."""

import pandas as pd


def resumir_remates_jugadores(remates: pd.DataFrame) -> pd.DataFrame:
    """Resume los remates registrados, incluidos los indicadores sin penal."""
    if remates[["player_id", "player"]].isna().any().any():
        raise ValueError("Hay remates sin jugador identificado.")

    if not remates["penalty"].isin([True, False]).all():
        raise ValueError("Hay remates sin una marca de penal válida.")

    sin_penal = remates["penalty"].eq(False)
    gol = remates["outcome"].eq("goal")
    detalle = remates.assign(
        gol=gol,
        sin_penal=sin_penal,
        gol_sin_penal=gol & sin_penal,
        xg_sin_penal=remates["xg"].where(sin_penal, 0.0),
    )

    tabla = detalle.groupby("player_id").agg(
        Jugador=("player", "first"),
        Remates=("xg", "size"),
        Goles=("gol", "sum"),
        xG_registrado=("xg", "sum"),
        Remates_sin_penal=("sin_penal", "sum"),
        Goles_sin_penal=("gol_sin_penal", "sum"),
        npxG_registrado=("xg_sin_penal", "sum"),
    )
    tabla["Penales"] = tabla["Remates"] - tabla["Remates_sin_penal"]
    tabla["xG_por_remate"] = tabla["xG_registrado"] / tabla["Remates"]

    intentos = tabla["Remates_sin_penal"]
    tabla["npxG_por_remate"] = tabla["npxG_registrado"] / intentos.where(intentos.gt(0))

    return tabla.sort_values(
        ["npxG_registrado", "Remates_sin_penal", "Jugador"],
        ascending=[False, False, True],
    )