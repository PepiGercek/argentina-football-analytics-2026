"""Cálculo de xG y xGA registrados para los partidos de zonas de Boca."""

import json
from pathlib import Path

import pandas as pd


def _leer_json(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def _xg_por_partido(ruta: Path, equipo_esperado: pd.Series) -> pd.Series:
    remates = pd.DataFrame(_leer_json(ruta)["shots"])
    remates = remates.loc[remates["game_id"].isin(equipo_esperado.index)]

    if not remates["team"].eq(remates["game_id"].map(equipo_esperado)).all():
        raise ValueError(f"Hay remates asignados al equipo incorrecto en {ruta.name}.")

    xg = pd.to_numeric(remates["xg"])
    if not xg.between(0, 1).all():
        raise ValueError(f"Hay valores de xG faltantes o fuera de rango en {ruta.name}.")

    return xg.groupby(remates["game_id"]).sum()


def cargar_xg_boca(carpeta: Path) -> pd.DataFrame:
    """Cruza los remates registrados con el listado validado de partidos."""
    respuesta = _leer_json(carpeta / "strikerapi_boca_partidos_2026.json")
    partidos = pd.json_normalize(respuesta["games"])
    ids = partidos["game_id"]
    if ids.isna().any() or not ids.is_unique:
        raise ValueError("El listado contiene IDs faltantes o repetidos.")

    partidos = partidos.set_index("game_id")
    partidos["torneo"] = partidos["stage"].str.removeprefix("Torneo ")
    boca_local = partidos["home.abbrev"].eq("CABJ")
    rivales = partidos["away.abbrev"].where(boca_local, partidos["home.abbrev"])

    partidos["GF"] = partidos["home.score"].where(boca_local, partidos["away.score"])
    partidos["GC"] = partidos["away.score"].where(boca_local, partidos["home.score"])
    partidos["xG_registrado"] = _xg_por_partido(
        carpeta / "strikerapi_boca_remates_favor_2026.json",
        pd.Series("CABJ", index=partidos.index),
    )
    partidos["xGA_registrado"] = _xg_por_partido(
        carpeta / "strikerapi_boca_remates_contra_2026.json",
        rivales,
    )

    indicadores = ["xG_registrado", "xGA_registrado"]
    if partidos[indicadores].isna().any().any():
        raise ValueError("Hay partidos sin xG registrado en alguno de los dos sentidos.")

    return partidos[["torneo", "GF", "GC", *indicadores]]