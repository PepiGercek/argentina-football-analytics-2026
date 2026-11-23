import pandas as pd

from lpf_analytics.scouting import resumir_remates_jugadores


def test_resumen_separa_penales_y_remates_sin_penal():
    remates = pd.DataFrame(
        [
            ("a", "Jugador A", False, 0.25, "saved"),
            ("a", "Jugador A", True, 0.75, "goal"),
            ("b", "Jugador B", True, 0.75, "goal"),
        ],
        columns=["player_id", "player", "penalty", "xg", "outcome"],
    )

    tabla = resumir_remates_jugadores(remates)

    assert tabla.loc["a", "xG_registrado"] == 1.0
    assert tabla.loc["a", "Goles"] == 1
    assert tabla.loc["a", "Penales"] == 1
    assert tabla.loc["a", "Goles_sin_penal"] == 0
    assert tabla.loc["a", "npxG_registrado"] == 0.25
    assert tabla.loc["a", "npxG_por_remate"] == 0.25

    assert tabla.loc["b", "Remates_sin_penal"] == 0
    assert tabla.loc["b", "npxG_registrado"] == 0.0
    assert pd.isna(tabla.loc["b", "npxG_por_remate"])