import pandas as pd
import pytest

from lpf_analytics.clustering import agrupar_equipos, indicadores_rendimiento


def test_indicadores_rendimiento_desde_marcadores():
    partidos = pd.DataFrame(
        [("A", "B", 2, 0), ("B", "A", 1, 1), ("A", "C", 0, 3)],
        columns=["local", "visitante", "goles_local", "goles_visitante"],
    )

    indicadores = indicadores_rendimiento(partidos)

    assert indicadores.loc["A"].to_dict() == pytest.approx({
        "GF_por_partido": 1.0,
        "GC_por_partido": 4 / 3,
        "Proporcion_empates": 1 / 3,
    })


def test_agrupar_equipos_conserva_variables_y_reune_pares_cercanos():
    indicadores = pd.DataFrame(
        [
            (1.40, 0.65, 0.20),
            (1.42, 0.67, 0.21),
            (0.65, 1.40, 0.21),
            (0.67, 1.42, 0.20),
            (1.02, 1.02, 0.43),
            (1.04, 1.04, 0.44),
        ],
        index=["A", "B", "C", "D", "E", "F"],
        columns=["GF_por_partido", "GC_por_partido", "Proporcion_empates"],
    )

    resultado = agrupar_equipos(indicadores, k=3)
    grupos = resultado["Grupo"]

    pd.testing.assert_frame_equal(resultado.drop(columns="Grupo"), indicadores)
    assert grupos.nunique() == 3
    assert grupos.loc["A"] == grupos.loc["B"]
    assert grupos.loc["C"] == grupos.loc["D"]
    assert grupos.loc["E"] == grupos.loc["F"]