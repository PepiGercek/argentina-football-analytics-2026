"""Control del balance anual calculado con SQLite."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd
import pytest

from lpf_analytics.resultados import tabla_equipos


def test_balance_anual_sql_coincide_con_pandas():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    if not ruta_csv.is_file():
        pytest.skip(f"Falta el archivo local {ruta_csv.name}.")

    esquema = (raiz / "sql/01_esquema.sql").read_text(encoding="utf-8-sig")
    consulta = (raiz / "sql/02_balance_anual.sql").read_text(encoding="utf-8-sig")
    partidos = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    filas_sql = partidos.drop(columns=["puntos_local", "puntos_visitante"])

    with closing(sqlite3.connect(":memory:")) as conexion:
        conexion.executescript(esquema)
        filas_sql.to_sql("partidos", conexion, if_exists="append", index=False)
        tabla_sql = pd.read_sql_query(consulta, conexion)

    assert len(tabla_sql) == 30

    indicadores = ["PJ", "PG", "PE", "PP", "PTS", "GF", "GC", "DG"]
    calculada = tabla_sql.set_index("Equipo")[indicadores].sort_index()
    esperada = tabla_equipos(partidos).set_index("Equipo")[indicadores].sort_index()

    pd.testing.assert_frame_equal(
        calculada,
        esperada,
        check_dtype=False,
        check_index_type=False,
        check_exact=True,
    )
