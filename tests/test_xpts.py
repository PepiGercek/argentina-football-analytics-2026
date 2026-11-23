import pytest

from lpf_analytics.xpts import calcular_xpts


def test_xpts_con_un_remate_por_equipo():
    resultado = calcular_xpts([0.4], [0.2])

    assert resultado == pytest.approx({
        "prob_victoria": 0.32,
        "prob_empate": 0.56,
        "prob_derrota": 0.12,
        "xPTS": 1.52,
    })


def test_xpts_con_distinta_cantidad_de_remates():
    resultado = calcular_xpts([0.5, 0.5], [0.5])

    assert resultado == pytest.approx({
        "prob_victoria": 0.5,
        "prob_empate": 0.375,
        "prob_derrota": 0.125,
        "xPTS": 1.875,
    })


@pytest.mark.parametrize(
    ("favor", "contra", "esperado"),
    [([], [], 1.0), ([1.0], [], 3.0), ([], [1.0], 0.0)],
)
def test_xpts_con_resultado_cierto(favor, contra, esperado):
    assert calcular_xpts(favor, contra)["xPTS"] == esperado