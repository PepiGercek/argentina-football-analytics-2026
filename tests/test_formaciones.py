import json

import pandas as pd

from lpf_analytics.formaciones import cargar_formaciones_boca, cargar_minutos_boca


def test_formaciones_conserva_partidos_sin_ficha_y_usa_fecha_local(tmp_path):
    partidos = {
        "games": [
            {
                "game_id": "1",
                "stage": "Torneo Apertura",
                "starts_at": "2026-01-29T00:30:00Z",
                "home": {"abbrev": "CABJ", "name": "Boca Juniors"},
                "away": {"abbrev": "RIE", "name": "Deportivo Riestra"},
            },
            {
                "game_id": "2",
                "stage": "Torneo Clausura",
                "starts_at": "2026-07-26T22:30:00Z",
                "home": {"abbrev": "RIE", "name": "Deportivo Riestra"},
                "away": {"abbrev": "CABJ", "name": "Boca Juniors"},
            },
        ],
    }
    ficha = {
        "game": {"game_id": "1"},
        "lineups": [
            {
                "abbrev": "CABJ",
                "formation": "4-3-3",
                "starting_xi": [{"player_id": str(i)} for i in range(1, 12)],
            },
        ],
    }
    respuestas = {
        "strikerapi_boca_partidos_2026.json": partidos,
        "strikerapi_boca_formaciones_1.json": ficha,
    }
    for nombre, contenido in respuestas.items():
        (tmp_path / nombre).write_text(json.dumps(contenido), encoding="utf-8")

    tabla = cargar_formaciones_boca(tmp_path).set_index("game_id")

    assert tabla.index.tolist() == ["1", "2"]
    assert tabla["rival"].tolist() == ["Deportivo Riestra", "Deportivo Riestra"]
    assert tabla.loc["1", "fecha_jugada"] == "2026-01-28"
    assert tabla.loc["1", "formacion"] == "4-3-3"
    assert tabla.loc["1", "titulares"] == 11
    assert pd.isna(tabla.loc["2", "formacion"])
    assert pd.isna(tabla.loc["2", "titulares"])

def test_minutos_corrigen_la_salida_de_paredes_ante_instituto(tmp_path):
    game_id = "401841607"
    partidos = {"games": [{"game_id": game_id}]}
    ruta_partidos = tmp_path / "strikerapi_boca_partidos_2026.json"
    ruta_partidos.write_text(json.dumps(partidos), encoding="utf-8")

    titulares = [
        {"player_id": str(i), "minute_on": 0, "minute_off": None}
        for i in range(1, 12)
    ]
    titulares[0]["minute_off"] = 55
    suplentes = [
        {"player_id": "153115", "minute_on": 55, "minute_off": 55},
        {"player_id": "12", "minute_on": 71, "minute_off": None},
    ]
    ficha = {
        "game": {"game_id": game_id},
        "lineups": [
            {
                "abbrev": "CABJ",
                "starting_xi": titulares,
                "substitutes_used": suplentes,
            }
        ],
    }
    ruta_ficha = tmp_path / f"strikerapi_boca_formaciones_{game_id}.json"
    ruta_ficha.write_text(json.dumps(ficha), encoding="utf-8")

    minutos = cargar_minutos_boca(tmp_path).set_index("player_id")

    assert minutos.loc["153115", "minutos_reglamentarios"] == 16
    assert minutos["minutos_reglamentarios"].sum() == 990