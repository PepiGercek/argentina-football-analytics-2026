"""Pruebas del cotejo con datos ficticios, ajenos a la base real."""

import pandas as pd
import pytest

from lpf_analytics.validacion import cotejar_boca_2026


@pytest.fixture
def tablas_ficticias():
    partidos = pd.DataFrame(
        [
            (2026, "Apertura", 1, "Boca Juniors", "Rival ficticio", 2, 0),
            (2026, "Clausura", 1, "Rival ficticio", "Boca Juniors", 1, 3),
        ],
        columns=[
            "temporada", "torneo", "fecha", "local", "visitante",
            "goles_local", "goles_visitante",
        ],
    )
    referencia = pd.DataFrame(
        [
            ("Apertura", 1, "Rival ficticio", "Local", 2, 0),
            ("Clausura", 1, "Rival ficticio", "Visitante", 3, 1),
        ],
        columns=["torneo", "fecha", "rival", "condicion", "gf", "gc"],
    )
    return partidos, referencia


def test_coinciden_partidos_con_igual_fecha_en_distintos_torneos(tablas_ficticias):
    partidos, referencia = tablas_ficticias
    control = cotejar_boca_2026(partidos, referencia)

    assert len(control) == 2
    assert control["_merge"].eq("both").all()
    assert control["coincide_todo"].all()


@pytest.mark.parametrize(
    "campo, valor",
    [
        ("rival", "Otro rival ficticio"),
        ("condicion", "Visitante"),
        ("gf", 7),
        ("gc", 8),
    ],
)
def test_detecta_diferencias_por_campo(tablas_ficticias, campo, valor):
    partidos, referencia = tablas_ficticias
    referencia.loc[0, campo] = valor

    control = cotejar_boca_2026(partidos, referencia)
    fila = control.loc[control["torneo"].eq("Apertura")].iloc[0]

    assert not bool(fila["coincide_todo"])
    for otro in ("rival", "condicion", "gf", "gc"):
        assert bool(fila[f"coincide_{otro}"]) == (otro != campo)


@pytest.mark.parametrize("lado", ["csv", "afa"])
def test_conserva_partidos_sin_pareja(tablas_ficticias, lado):
    partidos, referencia = tablas_ficticias
    if lado == "csv":
        partidos = partidos.iloc[:1].copy()
    else:
        referencia = referencia.iloc[:1].copy()

    control = cotejar_boca_2026(partidos, referencia)
    sin_pareja = control.loc[control["_merge"].ne("both")]

    assert len(control) == 2
    assert len(sin_pareja) == 1
    esperado = "right_only" if lado == "csv" else "left_only"
    assert sin_pareja.iloc[0]["_merge"] == esperado
    assert not bool(sin_pareja.iloc[0]["coincide_todo"])


@pytest.mark.parametrize("lado", ["csv", "afa"])
def test_rechaza_claves_duplicadas(tablas_ficticias, lado):
    partidos, referencia = tablas_ficticias
    if lado == "csv":
        partidos = pd.concat([partidos, partidos.iloc[[0]]], ignore_index=True)
    else:
        referencia = pd.concat([referencia, referencia.iloc[[0]]], ignore_index=True)

    with pytest.raises(pd.errors.MergeError):
        cotejar_boca_2026(partidos, referencia)


@pytest.mark.parametrize("lado", ["csv", "afa", "ambos"])
def test_rechaza_claves_vacias(tablas_ficticias, lado):
    partidos, referencia = tablas_ficticias
    if lado in ("csv", "ambos"):
        partidos["fecha"] = partidos["fecha"].astype("Int64")
        partidos.loc[0, "fecha"] = pd.NA
    if lado in ("afa", "ambos"):
        referencia["fecha"] = referencia["fecha"].astype("Int64")
        referencia.loc[0, "fecha"] = pd.NA

    with pytest.raises(ValueError, match="claves"):
        cotejar_boca_2026(partidos, referencia)
