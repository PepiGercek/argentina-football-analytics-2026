"""Carga los resultados validados en una base SQLite local."""

import csv
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory


raiz = Path(__file__).resolve().parents[1]
ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
ruta_esquema = raiz / "sql/01_esquema.sql"
ruta_base = raiz / "data/processed/lpf_2026.sqlite3"

columnas = (
    "temporada", "torneo", "fecha", "fecha_jugada", "local", "visitante",
    "goles_local", "goles_visitante", "dt_boca", "fuente_dt_boca",
    "fuente_resultado", "credito_resultado",
)
enteras = {"temporada", "fecha", "goles_local", "goles_visitante"}

with ruta_csv.open(encoding="utf-8-sig", newline="") as archivo:
    lector = csv.DictReader(archivo)
    faltantes = sorted(set(columnas) - set(lector.fieldnames or []))
    if faltantes:
        raise ValueError(f"Faltan columnas en el CSV: {faltantes}")

    filas = [
        tuple(
            int(fila[columna]) if columna in enteras else fila[columna] or None
            for columna in columnas
        )
        for fila in lector
    ]

esquema = ruta_esquema.read_text(encoding="utf-8-sig")
campos = ", ".join(columnas)
parametros = ", ".join("?" for _ in columnas)
insertar = f"INSERT INTO partidos ({campos}) VALUES ({parametros})"

with TemporaryDirectory(dir=ruta_base.parent) as carpeta_temporal:
    base_temporal = Path(carpeta_temporal) / ruta_base.name

    with closing(sqlite3.connect(base_temporal)) as conexion:
        conexion.executescript(esquema)
        with conexion:
            conexion.executemany(insertar, filas)
            conteos = dict(conexion.execute(
                "SELECT torneo, COUNT(*) FROM partidos GROUP BY torneo"
            ))
            if conteos != {"Apertura": 240, "Clausura": 240}:
                raise ValueError(f"Cobertura inesperada: {conteos}")

    base_temporal.replace(ruta_base)

print("Base creada:", ruta_base.relative_to(raiz))
for torneo, cantidad in conteos.items():
    print(f"{torneo}: {cantidad} partidos")
