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

def resumir_remates_por_90(
    remates: pd.DataFrame, minutos: pd.DataFrame
) -> pd.DataFrame:
    """Añade minutos reglamentarios y npxG por 90 al perfil de remates."""
    claves = ["game_id", "player_id"]
    tipos_id = {"game_id": "string", "player_id": "string"}
    remates = remates.astype(tipos_id)
    minutos = minutos[[*claves, "minutos_reglamentarios"]].astype(tipos_id)

    control = remates[claves].merge(
        minutos, on=claves, how="left", validate="many_to_one"
    )
    if control["minutos_reglamentarios"].fillna(0).le(0).any():
        raise ValueError("Hay remates sin minutos positivos para ese jugador y partido.")

    minutos_por_jugador = (
        minutos.groupby("player_id")["minutos_reglamentarios"].sum().rename("Minutos")
    )
    perfil = resumir_remates_jugadores(remates)
    tabla = perfil.join(minutos_por_jugador, validate="one_to_one")
    tabla["npxG_por_90"] = 90 * tabla["npxG_registrado"] / tabla["Minutos"]
    return tabla