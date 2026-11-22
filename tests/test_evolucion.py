"""Pruebas del orden cronológico y de los acumulados de la LPF."""

from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.evolucion import evolucion_equipos
from lpf_analytics.resultados import tabla_anual_2026


def test_un_reprogramado_suma_el_dia_en_que_se_juega():
    partidos = pd.DataFrame(
        [
            ("Apertura", 1, "2026-02-10", "Equipo A", "Equipo B", 2, 0),
            ("Apertura", 2, "2026-02-01", "Equipo C", "Equipo A", 1, 1),
        ],
        columns=[
            "torneo", "fecha", "fecha_jugada", "local", "visitante",
            "goles_local", "goles_visitante",
        ],
    )

    evolucion = evolucion_equipos(partidos)
    equipo_a = evolucion.loc[evolucion["equipo"].eq("Equipo A")]

    assert equipo_a["fecha"].tolist() == [2, 1]
    assert equipo_a["puntos_acumulados"].tolist() == [1, 4]


def test_el_cierre_de_los_30_equipos_coincide_con_la_tabla_anual():
    raiz = Path(__file__).resolve().parents[1]
    ruta = raiz / "data/raw/LPF_2026_partidos.csv"
    if not ruta.is_file():
        pytest.skip(f"Falta el archivo local {ruta.name}.")

    partidos = pd.read_csv(ruta, encoding="utf-8-sig")
    evolucion = evolucion_equipos(partidos)

    assert len(evolucion) == 960

    cierre = (
        evolucion.groupby("equipo").tail(1)
        .set_index("equipo")[["partido_acumulado", "puntos_acumulados"]]
        .rename(columns={"partido_acumulado": "PJ", "puntos_acumulados": "PTS"})
        .rename_axis("Equipo")
    )
    anual = tabla_anual_2026(partidos).set_index("Equipo")[["PJ", "PTS"]]

    pd.testing.assert_frame_equal(
        cierre.sort_index(), anual.sort_index(), check_index_type=False
    )
