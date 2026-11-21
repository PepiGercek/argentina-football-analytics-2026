from io import StringIO
from pathlib import Path

import pandas as pd


ALIAS_RIVALES_AFA_BOCA_2026 = {
    "Estudiantes de La Plata": "Estudiantes (La Plata)",
    "Gimnasia y Esgrima": "Gimnasia (Mendoza)",
    "Talleres (C)": "Talleres (Córdoba)",
}


def leer_boca_afa_2026(
    ruta_html: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lee la referencia de AFA para los partidos de Boca 2026.

    La fuente consultada presenta Apertura y Clausura en ese orden.
    Devuelve los partidos de zonas y las filas excluidas.
    GF y GC corresponden siempre a Boca, también cuando es visitante.
    """
    texto = Path(ruta_html).read_text(encoding="utf-8-sig")
    tablas = pd.read_html(StringIO(texto), flavor="lxml", header=0)

    if len(tablas) != 2:
        raise ValueError("Se esperaban dos tablas: Apertura y Clausura.")

    columnas = ["Fecha", "Rival", "Condición", "Resultado"]
    referencias = []
    exclusiones = []

    for torneo, tabla in zip(("Apertura", "Clausura"), tablas):
        faltantes = sorted(set(columnas) - set(tabla.columns))
        if faltantes:
            raise ValueError(f"Faltan columnas en {torneo}: {faltantes}")

        etiquetas = tabla["Fecha"].astype("string").str.strip()
        es_fecha = etiquetas.str.fullmatch(r"Fecha\s+\d+", na=False)

        fuera = tabla.loc[~es_fecha].copy()
        if not fuera.empty:
            fuera.insert(0, "torneo", torneo)
            exclusiones.append(fuera)

        datos = tabla.loc[es_fecha].copy()
        fechas = etiquetas.loc[es_fecha].str.extract(
            r"(\d+)$", expand=False
        ).astype(int)

        if sorted(fechas.tolist()) != list(range(1, 17)):
            raise ValueError(f"Cobertura de jornadas incorrecta en {torneo}.")

        rivales = datos["Rival"].astype("string").str.strip()
        if rivales.isna().any() or rivales.eq("").any():
            raise ValueError(f"Hay rivales vacíos en {torneo}.")

        condicion = datos["Condición"].astype("string").str.strip()
        if not condicion.isin(["Local", "Visitante"]).all():
            raise ValueError(f"Hay condiciones desconocidas en {torneo}.")

        goles = datos["Resultado"].astype("string").str.extract(
            r"^\s*(\d+)\s*-\s*(\d+)(?:\s*\([^)]*\))?\s*$"
        )
        if goles.isna().any().any():
            raise ValueError(f"Hay marcadores no reconocidos en {torneo}.")

        referencia = pd.DataFrame(
            {
                "torneo": torneo,
                "fecha": fechas,
                "rival_afa_original": rivales,
                "rival": rivales.replace(ALIAS_RIVALES_AFA_BOCA_2026),
                "condicion": condicion,
                "gf": goles[0].astype(int),
                "gc": goles[1].astype(int),
            }
        )
        referencias.append(referencia)

    zonas = pd.concat(referencias, ignore_index=True)
    excluidos = (
        pd.concat(exclusiones, ignore_index=True)
        if exclusiones
        else pd.DataFrame(columns=["torneo", *columnas])
    )

    return zonas, excluidos


ALIAS_EQUIPOS_COMOSALIO_2026 = {
    "Boca": "Boca Juniors",
    "Argentinos": "Argentinos Juniors",
    "Ind. Rivadavia": "Independiente Rivadavia",
    "Gimnasia LP": "Gimnasia (La Plata)",
    "Vélez": "Vélez Sarsfield",
    "Estudiantes": "Estudiantes (La Plata)",
    "Barracas": "Barracas Central",
    "Def. y Jus.": "Defensa y Justicia",
    "Unión (SF)": "Unión",
    "Gimnasia (M)": "Gimnasia (Mendoza)",
    "Sarmiento (J)": "Sarmiento (Junín)",
    "Talleres": "Talleres (Córdoba)",
    "Newell's": "Newell's Old Boys",
    "Racing": "Racing Club",
    "Atl Tucumán": "Atlético Tucumán",
    "C. Córdoba (SE)": "Central Córdoba (SdE)",
    "Riestra": "Deportivo Riestra",
    "Estudiantes RC": "Estudiantes (Río Cuarto)",
}


def leer_tabla_anual_comosalio_2026(ruta_html: str | Path) -> pd.DataFrame:
    """Lee los balances de Cómo Salió y conserva los nombres originales."""
    texto = Path(ruta_html).read_text(encoding="utf-8-sig")
    tablas = pd.read_html(StringIO(texto), flavor="lxml")

    columnas = ["Equipo", "Pts", "PJ", "PG", "PE", "PP", "GF", "GC", "Dif"]
    candidatas = [
        tabla for tabla in tablas if set(columnas).issubset(tabla.columns)
    ]
    if len(candidatas) != 1:
        raise ValueError("Se esperaba una única tabla con los balances anuales.")

    referencia = candidatas[0][columnas].rename(
        columns={"Pts": "PTS", "Dif": "DG"}
    )
    nombres = referencia["Equipo"].astype("string").str.strip()
    if nombres.isna().any() or nombres.eq("").any():
        raise ValueError("La referencia contiene equipos sin nombre.")

    referencia.insert(1, "Equipo_original", nombres)
    referencia["Equipo"] = nombres.replace(ALIAS_EQUIPOS_COMOSALIO_2026)
    return referencia
