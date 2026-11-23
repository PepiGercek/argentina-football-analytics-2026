"""Cotejo del CSV reconstruido con la base original de partidos."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.rsssf import reconstruir_partidos_rsssf_2026


def test_csv_reconstruido_coincide_con_el_original():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    ruta_html = raiz / "data/raw/rsssf_argentina_2026.html"

    faltantes = [ruta.name for ruta in (ruta_csv, ruta_html) if not ruta.is_file()]
    if faltantes:
        pytest.skip(f"Faltan archivos locales: {', '.join(faltantes)}")

    original = pd.read_csv(ruta_csv, encoding="utf-8-sig", keep_default_na=False)
    reconstruido = reconstruir_partidos_rsssf_2026(ruta_html)

    assert len(original) == len(reconstruido) == 480
    assert original.columns.tolist() == reconstruido.columns.tolist()

    claves = ["temporada", "torneo", "fecha", "local", "visitante"]
    original = original.set_index(claves).sort_index()
    reconstruido = reconstruido.set_index(claves).sort_index()

    assert original.index.is_unique, "Hay partidos duplicados en el CSV original."
    assert reconstruido.index.is_unique, "Hay partidos duplicados en el CSV reconstruido."

    pd.testing.assert_frame_equal(
        original,
        reconstruido,
        check_dtype=False,
        check_index_type=False,
        check_exact=True,
    )