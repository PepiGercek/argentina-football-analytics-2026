"""Controles de los balances de Apertura y Clausura 2026."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.resultados import comparar_torneos_2026, tabla_anual_2026


def test_los_balances_por_torneo_coinciden_con_el_total_anual():
    raiz = Path(__file__).resolve().parents[1]
    ruta = raiz / "data/raw/LPF_2026_partidos.csv"
    if not ruta.is_file():
        pytest.skip(f"Falta el archivo local {ruta.name}.")

    partidos = pd.read_csv(ruta, encoding="utf-8-sig")
    comparacion = comparar_torneos_2026(partidos).set_index("Equipo")

    indicadores = ["PJ", "PTS", "GF", "GC"]
    suma_torneos = pd.DataFrame({
        campo: comparacion[f"{campo}_Apertura"] + comparacion[f"{campo}_Clausura"]
        for campo in indicadores
    })
    anual = tabla_anual_2026(partidos).set_index("Equipo")[indicadores]

    pd.testing.assert_frame_equal(
        suma_torneos.sort_index(), anual.sort_index(), check_index_type=False
    )

    columnas_boca = [
        "PTS_Apertura", "PTS_Clausura", "Cambio_PTS", "Cambio_GF", "Cambio_GC",
    ]
    assert comparacion.loc["Boca Juniors", columnas_boca].tolist() == [30, 33, 3, 2, 5]
