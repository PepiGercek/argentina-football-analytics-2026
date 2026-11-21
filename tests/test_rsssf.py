"""Cotejo de los partidos de zonas con la copia local de RSSSF."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.rsssf import leer_partidos_rsssf_2026


def test_fechas_y_marcadores_coinciden_con_rsssf():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    ruta_html = raiz / "data/raw/rsssf_argentina_2026.html"

    faltantes = [
        ruta.name for ruta in (ruta_csv, ruta_html) if not ruta.is_file()
    ]
    if faltantes:
        pytest.skip(f"Faltan archivos locales: {', '.join(faltantes)}")

    partidos = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    referencia = leer_partidos_rsssf_2026(ruta_html)

    claves = ["torneo", "fecha", "local", "visitante"]
    campos = ["fecha_jugada", "goles_local", "goles_visitante"]

    csv = partidos.set_index(claves)[campos].sort_index()
    rsssf = referencia.set_index(claves)[campos].sort_index()

    assert len(csv) == len(rsssf) == 480
    assert csv.index.is_unique, "Hay partidos duplicados en el CSV."
    assert rsssf.index.is_unique, "Hay partidos duplicados en RSSSF."

    pd.testing.assert_frame_equal(
        csv,
        rsssf,
        check_dtype=False,
        check_index_type=False,
        check_exact=True,
    )
