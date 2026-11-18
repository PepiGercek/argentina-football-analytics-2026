"""Controles del CSV real. Fuentes y trazabilidad: docs/fuentes.md."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.resultados import resumen_equipo


@pytest.fixture(scope="module")
def partidos_2026():
    raiz = Path(__file__).resolve().parents[1]
    ruta = raiz / "data" / "raw" / "LPF_2026_partidos.csv"

    if not ruta.is_file():
        pytest.skip(
            "Falta data/raw/LPF_2026_partidos.csv para los controles reales."
        )

    return pd.read_csv(ruta, encoding="utf-8-sig")


def test_boca_2026_cubre_16_fechas_por_torneo(partidos_2026):
    boca = partidos_2026.loc[
        partidos_2026["local"].eq("Boca Juniors")
        | partidos_2026["visitante"].eq("Boca Juniors")
    ]

    assert boca["temporada"].eq(2026).all()
    assert set(boca["torneo"]) == {"Apertura", "Clausura"}

    for torneo in ("Apertura", "Clausura"):
        fechas = boca.loc[boca["torneo"].eq(torneo), "fecha"].tolist()
        assert sorted(fechas) == list(range(1, 17)), (
            f"Cobertura incorrecta en {torneo}: {fechas}"
        )


def test_balance_anual_boca_2026(partidos_2026):
    esperado = {
        "PJ": 32,
        "PG": 17,
        "PE": 12,
        "PP": 3,
        "PTS": 63,
        "GF": 46,
        "GC": 23,
    }

    assert resumen_equipo(partidos_2026, "Boca Juniors") == esperado
