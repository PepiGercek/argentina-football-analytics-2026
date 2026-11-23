"""Cobertura de las formaciones iniciales de Boca en StrikerAPI."""

import json
from pathlib import Path

import pandas as pd


def cargar_formaciones_boca(carpeta: Path) -> pd.DataFrame:
    """Cruza los partidos de zonas con las fichas de formación guardadas."""
    ruta_partidos = carpeta / "strikerapi_boca_partidos_2026.json"
    datos = json.loads(ruta_partidos.read_text(encoding="utf-8-sig"))
    partidos = pd.json_normalize(datos["games"])

    boca_local = partidos["home.abbrev"].eq("CABJ")
    partidos["rival"] = partidos["away.name"].where(boca_local, partidos["home.name"])
    partidos["torneo"] = partidos["stage"].str.removeprefix("Torneo ")
    partidos["fecha_jugada"] = (
        pd.to_datetime(partidos["starts_at"], utc=True)
        .dt.tz_convert("America/Argentina/Buenos_Aires")
        .dt.strftime("%Y-%m-%d")
    )

    filas = []
    for game_id in partidos["game_id"]:
        ruta = carpeta / f"strikerapi_boca_formaciones_{game_id}.json"
        if not ruta.is_file():
            continue

        ficha = json.loads(ruta.read_text(encoding="utf-8-sig"))
        if ficha["game"]["game_id"] != game_id:
            raise ValueError(f"El ID del partido no coincide en {ruta.name}.")

        alineaciones = [equipo for equipo in ficha["lineups"] if equipo["abbrev"] == "CABJ"]
        if len(alineaciones) != 1:
            raise ValueError(f"Se esperaba una alineación de Boca en {ruta.name}.")

        alineacion = alineaciones[0]
        filas.append({
            "game_id": game_id,
            "formacion": alineacion.get("formation"),
            "titulares": len(alineacion.get("starting_xi") or []),
        })

    fichas = pd.DataFrame(filas, columns=["game_id", "formacion", "titulares"])
    columnas = ["game_id", "torneo", "fecha_jugada", "rival"]
    tabla = partidos[columnas].merge(fichas, on="game_id", how="left", validate="one_to_one")
    tabla["titulares"] = tabla["titulares"].astype("Int64")
    return tabla.sort_values("fecha_jugada", ignore_index=True)