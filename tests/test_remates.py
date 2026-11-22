import json

import pandas as pd

from lpf_analytics.remates import cargar_xg_boca


def test_xg_por_partido_respeta_localia_y_excluye_playoffs(tmp_path):
    partidos = [
        {
            "game_id": "zonas-1",
            "stage": "Torneo Apertura",
            "home": {"abbrev": "CABJ", "score": 2},
            "away": {"abbrev": "RIV", "score": 1},
        },
        {
            "game_id": "zonas-2",
            "stage": "Torneo Clausura",
            "home": {"abbrev": "RIV", "score": 1},
            "away": {"abbrev": "CABJ", "score": 0},
        },
    ]
    respuestas = {
        "partidos": {"games": partidos},
        "remates_favor": {
            "shots": [
                {"game_id": "zonas-1", "team": "CABJ", "xg": 0.375},
                {"game_id": "zonas-1", "team": "CABJ", "xg": 0.125},
                {"game_id": "zonas-2", "team": "CABJ", "xg": 0.125},
                {"game_id": "playoff", "team": "CABJ", "xg": 0.875},
            ],
        },
        "remates_contra": {
            "shots": [
                {"game_id": "zonas-1", "team": "RIV", "xg": 0.25},
                {"game_id": "zonas-2", "team": "RIV", "xg": 0.75},
                {"game_id": "playoff", "team": "RIV", "xg": 0.5},
            ],
        },
    }
    for tipo, respuesta in respuestas.items():
        ruta = tmp_path / f"strikerapi_boca_{tipo}_2026.json"
        ruta.write_text(json.dumps(respuesta), encoding="utf-8")

    resultado = cargar_xg_boca(tmp_path)
    esperado = pd.DataFrame(
        [
            ["Apertura", 2, 1, 0.5, 0.25],
            ["Clausura", 0, 1, 0.125, 0.75],
        ],
        columns=["torneo", "GF", "GC", "xG_registrado", "xGA_registrado"],
        index=pd.Index(["zonas-1", "zonas-2"], name="game_id"),
    )

    pd.testing.assert_frame_equal(resultado, esperado)