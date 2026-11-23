"""Formaciones iniciales y minutos reglamentarios de Boca en StrikerAPI."""

import json
from collections import Counter
from pathlib import Path

import pandas as pd


def _leer_partidos_boca(carpeta: Path) -> pd.DataFrame:
    ruta = carpeta / "strikerapi_boca_partidos_2026.json"
    datos = json.loads(ruta.read_text(encoding="utf-8-sig"))
    return pd.json_normalize(datos["games"])


def _leer_alineacion_boca(carpeta: Path, game_id: str) -> dict | None:
    ruta = carpeta / f"strikerapi_boca_formaciones_{game_id}.json"
    if not ruta.is_file():
        return None

    ficha = json.loads(ruta.read_text(encoding="utf-8-sig"))
    if ficha["game"]["game_id"] != game_id:
        raise ValueError(f"El ID del partido no coincide en {ruta.name}.")

    alineaciones = [equipo for equipo in ficha["lineups"] if equipo["abbrev"] == "CABJ"]
    if len(alineaciones) != 1:
        raise ValueError(f"Se esperaba una alineación de Boca en {ruta.name}.")

    return alineaciones[0]


def cargar_formaciones_boca(carpeta: Path) -> pd.DataFrame:
    """Cruza los partidos de zonas con las fichas de formación guardadas."""
    partidos = _leer_partidos_boca(carpeta)
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
        alineacion = _leer_alineacion_boca(carpeta, game_id)
        if alineacion is None:
            continue

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


def cargar_minutos_boca(carpeta: Path) -> pd.DataFrame:
    """Reconstruye los minutos reglamentarios por jugador y partido de zonas."""
    partidos = _leer_partidos_boca(carpeta)
    filas = []

    for game_id in partidos["game_id"]:
        alineacion = _leer_alineacion_boca(carpeta, game_id)
        if alineacion is None:
            raise FileNotFoundError(f"Falta la ficha de formación del partido {game_id}.")

        titulares = alineacion["starting_xi"]
        suplentes = alineacion["substitutes_used"]
        if len(titulares) != 11 or any(jugador["minute_on"] != 0 for jugador in titulares):
            raise ValueError(f"Se esperaban 11 titulares desde el minuto 0 en {game_id}.")

        salidas = Counter()
        for jugador in titulares + suplentes:
            if not jugador["player_id"]:
                raise ValueError(f"Hay un jugador sin ID en el partido {game_id}.")
            if jugador.get("red_cards"):
                raise ValueError(f"Hay una expulsión que requiere revisar los minutos en {game_id}.")

            player_id = str(jugador["player_id"])
            entrada = jugador["minute_on"]
            salida = jugador["minute_off"]

            # Boca confirmó que Paredes jugó 16 minutos ante Instituto.
            # https://www.bocajuniors.com.ar/noticias/empate-en-cordoba
            if (game_id, player_id, entrada, salida) == ("401841607", "153115", 55, 55):
                salida = 71

            final = 90 if salida is None else salida
            if type(entrada) is not int or type(final) is not int or not 0 <= entrada <= final <= 90:
                raise ValueError(f"Intervalo inválido para el jugador {player_id} en {game_id}.")

            if salida is not None:
                salidas[salida] += 1
            filas.append((game_id, player_id, final - entrada))

        entradas = Counter(jugador["minute_on"] for jugador in suplentes)
        if entradas != salidas:
            raise ValueError(f"Las entradas y salidas no coinciden en el partido {game_id}.")

    tabla = pd.DataFrame(filas, columns=["game_id", "player_id", "minutos_reglamentarios"])
    if tabla.duplicated(["game_id", "player_id"]).any():
        raise ValueError("Hay jugadores repetidos en una ficha de partido.")
    return tabla