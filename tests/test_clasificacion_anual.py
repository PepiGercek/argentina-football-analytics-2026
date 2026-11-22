"""Cotejo del orden de la tabla anual con la copia local de RSSSF."""

import re
from pathlib import Path

import pandas as pd
import pytest
from lxml import html

from lpf_analytics.resultados import tabla_anual_2026
from lpf_analytics.rsssf import NOMBRES_RSSSF


def test_clasificacion_anual_coincide_con_rsssf():
    raiz = Path(__file__).resolve().parents[1]
    ruta_csv = raiz / "data/raw/LPF_2026_partidos.csv"
    ruta_html = raiz / "data/raw/rsssf_argentina_2026.html"

    faltantes = [
        ruta.name for ruta in (ruta_csv, ruta_html) if not ruta.is_file()
    ]
    if faltantes:
        pytest.skip(f"Faltan archivos locales: {', '.join(faltantes)}")

    documento = html.fromstring(ruta_html.read_bytes())
    bloques = [nodo.text_content() for nodo in documento.xpath("//pre")]
    bloque, = [texto for texto in bloques if "Rules to define the champion:" in texto]

    patron = re.compile(r"^(\d{1,2})\.\s*(\S.*?)\s{2,}\d+\s")
    puestos_publicados = []
    for linea in bloque.splitlines():
        marca = patron.match(linea.strip())
        if marca:
            puesto, nombre = marca.groups()
            puestos_publicados.append((int(puesto), NOMBRES_RSSSF[nombre]))

    assert sorted(puesto for puesto, _ in puestos_publicados) == list(range(1, 31))

    partidos = pd.read_csv(ruta_csv, encoding="utf-8-sig")
    calculada = tabla_anual_2026(partidos)
    puestos_calculados = list(
        calculada[["Pos", "Equipo"]].itertuples(index=False, name=None)
    )

    assert puestos_calculados == sorted(puestos_publicados)
