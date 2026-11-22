"""Exporta las tablas del modelo de Power BI desde SQLite."""

import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from lpf_analytics.resultados import tabla_anual_2026


raiz = Path(__file__).resolve().parents[1]
ruta_base = raiz / "data/processed/lpf_2026.sqlite3"
destino = raiz / "data/processed/powerbi"
consulta = (raiz / "sql/03_partidos_por_equipo.sql").read_text(encoding="utf-8-sig")

with closing(sqlite3.connect(ruta_base.as_uri() + "?mode=ro", uri=True)) as conexion:
    participaciones = pd.read_sql_query(consulta, conexion)
    partidos = pd.read_sql_query(
        "SELECT temporada, local, visitante, goles_local, goles_visitante FROM partidos",
        conexion,
    )

conteos = participaciones["partido_id"].value_counts()
if len(participaciones) != 960 or len(conteos) != 480 or not conteos.eq(2).all():
    raise ValueError("Se esperaban 480 partidos con dos participaciones cada uno.")

clasificacion = tabla_anual_2026(partidos)
equipos = clasificacion[["Equipo", "Pos"]].rename(columns={
    "Equipo": "equipo",
    "Pos": "posicion_anual",
})
if set(participaciones["equipo"]) != set(equipos["equipo"]):
    raise ValueError("Los equipos de las dos tablas no coinciden.")

calendario = pd.DataFrame({
    "fecha": pd.date_range("2026-01-01", "2026-12-31", freq="D"),
})

tablas = {
    "partidos_equipo.csv": participaciones,
    "equipos.csv": equipos,
    "calendario.csv": calendario,
}

destino.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=destino) as temporal:
    for nombre, tabla in tablas.items():
        tabla.to_csv(
            Path(temporal) / nombre,
            index=False,
            encoding="utf-8-sig",
            date_format="%Y-%m-%d",
        )
    for nombre in tablas:
        (Path(temporal) / nombre).replace(destino / nombre)

print("Archivos generados en:", destino.relative_to(raiz))
for nombre, tabla in tablas.items():
    print(f"{nombre}: {len(tabla)} filas")
