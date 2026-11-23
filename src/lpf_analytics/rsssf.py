"""Lectura de las fases de zonas de Argentina 2026, compiladas por RSSSF."""

import re
from datetime import date
from pathlib import Path

import pandas as pd
from lxml import html


TORNEOS = ("Apertura", "Clausura")
MESES = {
    mes: numero
    for numero, mes in enumerate(
        "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), start=1
    )
}
PATRON_JORNADA = re.compile(r"Round\s+(\d+):")
PATRON_DIA = re.compile(r"\[([A-Za-z]{3})\s+(\d{1,2}),\s*[A-Za-z]+\]")
PATRON_PARTIDO = re.compile(
    r"(.+?)\s{2,}(\d+)\s*-\s*(\d+)\s{2,}(.+?)(?:\s{2,}.*)?"
)

NOMBRES_RSSSF = {
    "AA Argentinos Juniors": "Argentinos Juniors",
    "AA Estudiantes": "Estudiantes (Río Cuarto)",
    "CA Aldosivi": "Aldosivi",
    "CA Banfield": "Banfield",
    "CA Barracas Central": "Barracas Central",
    "CA Belgrano": "Belgrano",
    "CA Boca Juniors": "Boca Juniors",
    "CA Central Córdoba": "Central Córdoba (SdE)",
    "CA Gimnasia y Esgrima": "Gimnasia (Mendoza)",
    "CA Huracán": "Huracán",
    "CA Independiente": "Independiente",
    "CA Lanús": "Lanús",
    "CA Newell's Old Boys": "Newell's Old Boys",
    "CA Platense": "Platense",
    "CA River Plate": "River Plate",
    "CA Rosario Central": "Rosario Central",
    "CA San Lorenzo de Almagro": "San Lorenzo",
    "CA Sarmiento": "Sarmiento (Junín)",
    "CA Talleres": "Talleres (Córdoba)",
    "CA Tigre": "Tigre",
    "CA Unión": "Unión",
    "CA Vélez Sarsfield": "Vélez Sarsfield",
    "CS Independiente Rivadavia": "Independiente Rivadavia",
    "CSD Defensa y Justicia": "Defensa y Justicia",
    "Club Atlético Tucumán": "Atlético Tucumán",
    "Club Estudiantes de La Plata": "Estudiantes (La Plata)",
    "Club de Gimnasia y Esgrima LP": "Gimnasia (La Plata)",
    "Deportivo Riestra AFBC": "Deportivo Riestra",
    "Instituto ACC": "Instituto",
    "Racing Club": "Racing Club",
}


def leer_partidos_rsssf_2026(ruta_html: str | Path) -> pd.DataFrame:
    """Extrae jornadas, fechas y marcadores de los dos torneos de zonas."""
    documento = html.fromstring(Path(ruta_html).read_bytes())
    if documento.xpath("string(//title)").strip() != "Argentina 2026":
        raise ValueError("El HTML no corresponde a Argentina 2026.")

    filas = []
    bloques = documento.xpath("//pre")[:2]
    if len(bloques) != 2:
        raise ValueError("Se esperaban los bloques de Apertura y Clausura.")

    for torneo, bloque in zip(TORNEOS, bloques):
        lineas = bloque.text_content().splitlines()
        inicio = next(
            (i for i, linea in enumerate(lineas) if "Phase of groups" in linea),
            None,
        )
        if inicio is None:
            raise ValueError(f"No se encontró el inicio de zonas en {torneo}.")

        fin = next(
            (i for i in range(inicio + 1, len(lineas)) if lineas[i].strip() == "Tie break:"),
            None,
        )
        if fin is None:
            raise ValueError(f"No se encontró el fin de zonas en {torneo}.")

        jornada = None
        fecha_jugada = None

        for numero, original in enumerate(lineas[inicio + 1:fin], start=inicio + 2):
            linea = original.strip()
            if not linea:
                continue

            ronda = PATRON_JORNADA.fullmatch(linea)
            if ronda:
                jornada = int(ronda.group(1))
                fecha_jugada = None
                continue

            dia = PATRON_DIA.fullmatch(linea)
            if dia:
                mes, numero_dia = dia.groups()
                fecha_jugada = date(2026, MESES[mes], int(numero_dia)).isoformat()
                continue

            partido = PATRON_PARTIDO.fullmatch(linea)
            if partido is None or jornada is None or fecha_jugada is None:
                raise ValueError(f"Línea sin interpretar en {torneo}, {numero}: {linea}")

            local, gl, gv, visitante = partido.groups()
            filas.append((torneo, jornada, fecha_jugada, local, visitante, int(gl), int(gv)))

    referencia = pd.DataFrame(filas, columns=[
        "torneo", "fecha", "fecha_jugada", "local_rsssf", "visitante_rsssf",
        "goles_local", "goles_visitante",
    ])

    esperados = {(torneo, jornada): 15 for torneo in TORNEOS for jornada in range(1, 17)}
    if referencia.groupby(["torneo", "fecha"]).size().to_dict() != esperados:
        raise ValueError("Se esperaban 15 partidos por jornada en ambos torneos.")

    for lado in ("local", "visitante"):
        nombres = referencia[f"{lado}_rsssf"]
        desconocidos = sorted(set(nombres) - NOMBRES_RSSSF.keys())
        if desconocidos:
            raise ValueError(f"Nombres de RSSSF sin equivalencia: {desconocidos}")
        referencia[lado] = nombres.map(NOMBRES_RSSSF)

    return referencia

COLUMNAS_CSV = [
    "temporada", "torneo", "fecha", "fecha_jugada", "local", "visitante",
    "goles_local", "goles_visitante", "puntos_local", "puntos_visitante",
    "dt_boca", "fuente_resultado", "credito_resultado", "fuente_dt_boca",
]

FUENTE_RSSSF = "https://www.rsssf.org/tablesa/arg2026.html"
CREDITO_RSSSF = "Osvaldo José Gorgazzi / RSSSF"

DT_BOCA = {
    "Apertura": "Claudio Úbeda",
    "Clausura": "Rodolfo Arruabarrena",
}
FUENTE_DT_BOCA = {
    "Apertura": "https://deportv.gob.ar/futbol/campana-boca-valio-titulo-liga-profesional-nid%3A18747",
    "Clausura": "https://www.bocajuniors.com.ar/noticias/comunicado-oficial-2",
}


def reconstruir_partidos_rsssf_2026(ruta_html: str | Path) -> pd.DataFrame:
    """Reconstruye el esquema de resultados a partir de una copia de RSSSF."""
    referencia = leer_partidos_rsssf_2026(ruta_html)
    goles_local = referencia["goles_local"]
    goles_visitante = referencia["goles_visitante"]
    puntos_empate = goles_local.eq(goles_visitante).astype(int)
    es_boca = referencia[["local", "visitante"]].eq("Boca Juniors").any(axis=1)
    torneos = referencia["torneo"]

    partidos = referencia.assign(
        temporada=2026,
        puntos_local=3 * goles_local.gt(goles_visitante).astype(int) + puntos_empate,
        puntos_visitante=3 * goles_local.lt(goles_visitante).astype(int) + puntos_empate,
        dt_boca=torneos.map(DT_BOCA).where(es_boca, ""),
        fuente_resultado=FUENTE_RSSSF,
        credito_resultado=CREDITO_RSSSF,
        fuente_dt_boca=torneos.map(FUENTE_DT_BOCA).where(es_boca, ""),
    )
    return partidos[COLUMNAS_CSV]


def main() -> None:
    from argparse import ArgumentParser
    from tempfile import TemporaryDirectory

    parser = ArgumentParser(description="Reconstruye el CSV de resultados de LPF 2026.")
    parser.add_argument("html", type=Path, help="Copia local de Argentina 2026 en RSSSF.")
    parser.add_argument("csv", type=Path, help="Ruta del CSV de salida.")
    args = parser.parse_args()

    if args.html.resolve() == args.csv.resolve():
        parser.error("Indicá una ruta de salida distinta a la del HTML.")

    partidos = reconstruir_partidos_rsssf_2026(args.html)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=args.csv.parent) as carpeta:
        temporal = Path(carpeta) / args.csv.name
        partidos.to_csv(temporal, index=False, encoding="utf-8")
        temporal.replace(args.csv)

    print(f"CSV generado en {args.csv} con {len(partidos)} partidos.")


if __name__ == "__main__":
    main()