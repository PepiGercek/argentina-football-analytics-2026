"""Cálculo de xG, xGA y xPTS para los partidos de zonas de Boca."""

import json
from math import fsum
from pathlib import Path

import pandas as pd

from .xpts import calcular_xpts


def _leer_json(ruta: Path) -> dict:
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def _xg_por_remate(ruta: Path, equipo_esperado: pd.Series) -> pd.Series:
    remates = pd.DataFrame(_leer_json(ruta)["shots"])
    remates = remates.loc[remates["game_id"].isin(equipo_esperado.index)]

    if not remates["team"].eq(remates["game_id"].map(equipo_esperado)).all():
        raise ValueError(f"Hay remates asignados al equipo incorrecto en {ruta.name}.")

    xg = pd.to_numeric(remates["xg"])
    if not xg.between(0, 1).all():
        raise ValueError(f"Hay valores de xG faltantes o fuera de rango en {ruta.name}.")

    return xg.groupby(remates["game_id"]).agg(list).reindex(equipo_esperado.index)


def _cargar_partidos_y_remates(
    carpeta: Path,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
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
    favor = _xg_por_remate(
        carpeta / "strikerapi_boca_remates_favor_2026.json",
        pd.Series("CABJ", index=partidos.index),
    )
    contra = _xg_por_remate(
        carpeta / "strikerapi_boca_remates_contra_2026.json",
        rivales,
    )
    if favor.isna().any() or contra.isna().any():
        raise ValueError("Hay partidos sin xG registrado en alguno de los dos sentidos.")

    return partidos[["torneo", "GF", "GC"]], favor, contra


def cargar_xg_boca(carpeta: Path) -> pd.DataFrame:
    """Suma el xG de los remates registrados para cada partido."""
    partidos, favor, contra = _cargar_partidos_y_remates(carpeta)
    return partidos.assign(
        xG_registrado=favor.map(fsum),
        xGA_registrado=contra.map(fsum),
    )


def cargar_xpts_boca(carpeta: Path) -> pd.DataFrame:
    """Devuelve puntos reales y esperados para cada partido."""
    partidos, favor, contra = _cargar_partidos_y_remates(carpeta)
    estimaciones = pd.DataFrame(
        [
            calcular_xpts(remates_favor, remates_contra)
            for remates_favor, remates_contra in zip(favor, contra, strict=True)
        ],
        index=partidos.index,
    )
    victorias = partidos["GF"].gt(partidos["GC"]).astype(int)
    empates = partidos["GF"].eq(partidos["GC"]).astype(int)
    return partidos.assign(PTS=3 * victorias + empates).join(estimaciones)