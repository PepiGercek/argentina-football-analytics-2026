import json

import pandas as pd

from lpf_analytics.formaciones import cargar_formaciones_boca


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