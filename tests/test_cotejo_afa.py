"""Controles reales contra la copia local de AFA. Ver docs/fuentes.md."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.fuentes import leer_boca_afa_2026
from lpf_analytics.validacion import cotejar_boca_2026


RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def partidos_reales():
    ruta = RAIZ / "data" / "raw" / "LPF_2026_partidos.csv"
    if not ruta.is_file():
        pytest.skip("Falta data/raw/LPF_2026_partidos.csv.")

    return pd.read_csv(ruta, encoding="utf-8-sig")


@pytest.fixture(scope="module")
def referencia_afa():
    ruta = RAIZ / "data" / "raw" / "afa_boca_2026.html"
    if not ruta.is_file():
        pytest.skip("Falta data/raw/afa_boca_2026.html.")

    return leer_boca_afa_2026(ruta)


def test_los_32_partidos_coinciden_con_afa(partidos_reales, referencia_afa):
    zonas, _ = referencia_afa
    control = cotejar_boca_2026(partidos_reales, zonas)

    assert len(zonas) == 32
    assert len(control) == 32
    assert control["_merge"].eq("both").all()

    banderas = [
        "coincide_rival",
        "coincide_condicion",
        "coincide_gf",
        "coincide_gc",
        "coincide_todo",
    ]
    assert control[banderas].eq(True).fillna(False).all().all()


def test_huracan_de_octavos_esta_excluido(referencia_afa):
    zonas, excluidos = referencia_afa

    assert not zonas["rival"].eq("Huracán").any()

    huracan = excluidos.loc[
        excluidos["torneo"].eq("Apertura")
        & excluidos["Fecha"].eq("Octavos de final")
        & excluidos["Rival"].eq("Huracán")
    ]
    assert len(huracan) == 1
