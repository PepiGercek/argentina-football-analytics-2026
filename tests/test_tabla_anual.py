"""Cotejo de la tabla anual 2026 contra la copia local de Cómo Salió."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.fuentes import leer_tabla_anual_comosalio_2026
from lpf_analytics.resultados import tabla_equipos


def test_tabla_anual_coincide_con_comosalio():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    ruta_html = raiz / "data/raw/comosalio_tabla_anual_2026.html"

    faltantes = [
        ruta.name for ruta in (ruta_csv, ruta_html) if not ruta.is_file()
    ]
    if faltantes:
        pytest.skip(f"Faltan archivos de referencia: {', '.join(faltantes)}")

    partidos = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    calculada = tabla_equipos(partidos).set_index("Equipo")
    referencia = leer_tabla_anual_comosalio_2026(ruta_html).set_index("Equipo")

    assert len(calculada) == len(referencia) == 30
    assert calculada.index.is_unique
    assert referencia.index.is_unique

    indicadores = ["PTS", "PJ", "PG", "PE", "PP", "GF", "GC", "DG"]
    pd.testing.assert_frame_equal(
        calculada[indicadores].sort_index(),
        referencia[indicadores].sort_index(),
        check_dtype=False,
        check_index_type=False,
        check_exact=True,
    )
