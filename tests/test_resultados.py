"""Pruebas unitarias con partidos ficticios, ajenos al dataset real."""

import pandas as pd
import pytest

from lpf_analytics.resultados import resumen_equipo


def test_calcula_balance_desde_goles_y_localia():
    partidos = pd.DataFrame(
        [
            ("Equipo A", "Equipo B", 2, 0),
            ("Equipo C", "Equipo A", 0, 1),
            ("Equipo A", "Equipo D", 1, 1),
            ("Equipo E", "Equipo A", 2, 2),
            ("Equipo A", "Equipo F", 0, 3),
            ("Equipo G", "Equipo A", 4, 1),
            ("Equipo H", "Equipo I", 9, 9),
        ],
        columns=["local", "visitante", "goles_local", "goles_visitante"],
    )

    # Valores incorrectos deliberados: el calculo debe usar los goles.
    partidos["puntos_local"] = 999
    partidos["puntos_visitante"] = 999

    esperado = {
        "PJ": 6,
        "PG": 2,
        "PE": 2,
        "PP": 2,
        "PTS": 8,
        "GF": 7,
        "GC": 10,
    }

    assert resumen_equipo(partidos, "Equipo A") == esperado


@pytest.mark.parametrize("columna", ["goles_local", "goles_visitante"])
@pytest.mark.parametrize("valor", [None, -1, 0.5, "sin dato"])
def test_rechaza_goles_invalidos(columna, valor):
    fila = {
        "local": "Equipo A",
        "visitante": "Equipo B",
        "goles_local": 1,
        "goles_visitante": 0,
    }
    fila[columna] = valor

    with pytest.raises(ValueError):
        resumen_equipo(pd.DataFrame([fila]), "Equipo A")


def test_rechaza_columnas_faltantes():
    partidos = pd.DataFrame(
        [{"local": "Equipo A", "visitante": "Equipo B", "goles_local": 1}]
    )

    with pytest.raises(ValueError, match="Faltan columnas"):
        resumen_equipo(partidos, "Equipo A")


def test_rechaza_equipo_sin_partidos():
    partidos = pd.DataFrame(
        [("Equipo A", "Equipo B", 1, 0)],
        columns=["local", "visitante", "goles_local", "goles_visitante"],
    )

    with pytest.raises(ValueError, match="No se encontraron partidos"):
        resumen_equipo(partidos, "Equipo Z")


def test_rechaza_partido_contra_si_mismo():
    partidos = pd.DataFrame(
        [("Equipo A", "Equipo A", 1, 0)],
        columns=["local", "visitante", "goles_local", "goles_visitante"],
    )

    with pytest.raises(ValueError, match="sí mismo"):
        resumen_equipo(partidos, "Equipo A")
