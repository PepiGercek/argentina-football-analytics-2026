"""Controles de las consultas SQL y de los datos para Power BI."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.evolucion import evolucion_equipos
from lpf_analytics.resultados import tabla_equipos


@pytest.fixture(scope="module")
def base_sql_lpf():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    if not ruta_csv.is_file():
        pytest.skip(f"Falta el archivo local {ruta_csv.name}.")

    partidos = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    filas_sql = partidos.drop(columns=["puntos_local", "puntos_visitante"])
    carpeta_sql = raiz / "sql"
    esquema = (carpeta_sql / "01_esquema.sql").read_text(encoding="utf-8-sig")

    with closing(sqlite3.connect(":memory:")) as conexion:
        conexion.executescript(esquema)
        filas_sql.to_sql("partidos", conexion, if_exists="append", index=False)
        yield conexion, partidos, carpeta_sql


def test_balance_anual_sql_coincide_con_pandas(base_sql_lpf):
    conexion, partidos, carpeta_sql = base_sql_lpf
    consulta = (carpeta_sql / "02_balance_anual.sql").read_text(encoding="utf-8-sig")
    tabla_sql = pd.read_sql_query(consulta, conexion)

    assert len(tabla_sql) == 30

    indicadores = ["PJ", "PG", "PE", "PP", "PTS", "GF", "GC", "DG"]
    calculada = tabla_sql.set_index("Equipo")[indicadores].sort_index()
    esperada = tabla_equipos(partidos).set_index("Equipo")[indicadores].sort_index()

    pd.testing.assert_frame_equal(
        calculada, esperada, check_dtype=False,
        check_index_type=False, check_exact=True,
    )


def test_participaciones_para_powerbi_coinciden_con_pandas(base_sql_lpf):
    conexion, partidos, carpeta_sql = base_sql_lpf
    consulta = (carpeta_sql / "03_partidos_por_equipo.sql").read_text(
        encoding="utf-8-sig"
    )
    tabla_sql = pd.read_sql_query(consulta, conexion)

    por_partido = tabla_sql.groupby("partido_id")["condicion"].agg(["size", "nunique"])
    assert len(tabla_sql) == 960
    assert len(por_partido) == 480
    assert por_partido.eq(2).all().all()

    tabla_pandas = evolucion_equipos(partidos).rename(columns={
        "fecha": "jornada",
        "GF": "goles_favor",
        "GC": "goles_contra",
    })
    tabla_pandas["fecha_jugada"] = tabla_pandas["fecha_jugada"].dt.strftime("%Y-%m-%d")

    campos = [
        "equipo", "rival", "torneo", "jornada", "fecha_jugada",
        "condicion", "goles_favor", "goles_contra", "puntos",
    ]
    orden = ["equipo", "fecha_jugada"]
    calculada = tabla_sql[campos].sort_values(orden, ignore_index=True)
    esperada = tabla_pandas[campos].sort_values(orden, ignore_index=True)
    pd.testing.assert_frame_equal(
        calculada, esperada, check_dtype=False, check_exact=True,
    )

    boca = tabla_sql.loc[tabla_sql["equipo"].eq("Boca Juniors")]
    assert boca["resultado"].value_counts().to_dict() == {"G": 17, "E": 12, "P": 3}
