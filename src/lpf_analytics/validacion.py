import pandas as pd


def cotejar_boca_2026(
    partidos: pd.DataFrame, referencia_afa: pd.DataFrame
) -> pd.DataFrame:
    """Compara los partidos recibidos de Boca 2026 contra AFA.

    Identifica cada partido por torneo y jornada.
    Conserva las filas sin correspondencia y rechaza claves duplicadas.
    Devuelve los valores de ambas fuentes y las coincidencias por campo.
    """
    requeridas_csv = [
        "temporada", "torneo", "fecha", "local", "visitante",
        "goles_local", "goles_visitante",
    ]
    requeridas_afa = ["torneo", "fecha", "rival", "condicion", "gf", "gc"]

    for nombre, tabla, requeridas in (
        ("CSV", partidos, requeridas_csv),
        ("AFA", referencia_afa, requeridas_afa),
    ):
        faltantes = sorted(set(requeridas) - set(tabla.columns))
        if faltantes:
            raise ValueError(f"Faltan columnas en {nombre}: {faltantes}")

    boca = partidos.loc[
        partidos["local"].eq("Boca Juniors")
        | partidos["visitante"].eq("Boca Juniors")
    ].copy()

    if boca.empty or not boca["temporada"].eq(2026).fillna(False).all():
        raise ValueError("Se esperaban partidos de Boca de la temporada 2026.")

    es_local = boca["local"].eq("Boca Juniors")
    goles = boca[["goles_local", "goles_visitante"]].apply(
        pd.to_numeric, errors="raise"
    )

    vista_csv = pd.DataFrame(
        {
            "torneo": boca["torneo"],
            "fecha": boca["fecha"],
            "rival": boca["visitante"].where(es_local, boca["local"]),
            "condicion": es_local.map({True: "Local", False: "Visitante"}),
            "gf": goles["goles_local"].where(es_local, goles["goles_visitante"]),
            "gc": goles["goles_visitante"].where(es_local, goles["goles_local"]),
        }
    )

    claves = ["torneo", "fecha"]
    if (
        vista_csv[claves].isna().any().any()
        or referencia_afa[claves].isna().any().any()
    ):
        raise ValueError("Hay torneos o jornadas vacíos en las claves.")

    control = vista_csv.merge(
        referencia_afa,
        on=claves,
        how="outer",
        suffixes=("_csv", "_afa"),
        validate="one_to_one",
        indicator=True,
    )

    banderas = []
    for campo in ("rival", "condicion", "gf", "gc"):
        bandera = f"coincide_{campo}"
        control[bandera] = control[f"{campo}_csv"].eq(
            control[f"{campo}_afa"]
        ).fillna(False)
        banderas.append(bandera)

    control["coincide_todo"] = (
        control["_merge"].eq("both") & control[banderas].all(axis=1)
    )

    return control.sort_values(claves).reset_index(drop=True)
