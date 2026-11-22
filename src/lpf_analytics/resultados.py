import pandas as pd


def resumen_equipo(partidos: pd.DataFrame, equipo: str) -> dict[str, int]:
    """Calcula el balance de un equipo en los partidos recibidos.

    La temporada, el torneo y la fase deben filtrarse antes de llamar
    a esta función. El nombre del equipo se compara de forma exacta.
    """
    columnas = ["local", "visitante", "goles_local", "goles_visitante"]
    faltantes = sorted(set(columnas) - set(partidos.columns))

    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    local = partidos["local"].eq(equipo)
    visitante = partidos["visitante"].eq(equipo)

    if (local & visitante).any():
        raise ValueError("Un equipo no puede enfrentarse a sí mismo.")

    seleccion = partidos.loc[local | visitante]

    if seleccion.empty:
        raise ValueError(f"No se encontraron partidos para {equipo!r}.")

    goles = seleccion[["goles_local", "goles_visitante"]].apply(
        pd.to_numeric, errors="raise"
    )

    invalidos = (
        goles.isna().any().any()
        or goles.lt(0).any().any()
        or goles.mod(1).ne(0).any().any()
    )

    if invalidos:
        raise ValueError(
            "Los goles deben ser completos, enteros y no negativos."
        )

    es_local = seleccion["local"].eq(equipo)
    gf = goles["goles_local"].where(es_local, goles["goles_visitante"])
    gc = goles["goles_visitante"].where(es_local, goles["goles_local"])

    pg = int(gf.gt(gc).sum())
    pe = int(gf.eq(gc).sum())
    pp = int(gf.lt(gc).sum())

    return {
        "PJ": len(seleccion),
        "PG": pg,
        "PE": pe,
        "PP": pp,
        "PTS": 3 * pg + pe,
        "GF": int(gf.sum()),
        "GC": int(gc.sum()),
    }


def tabla_equipos(partidos: pd.DataFrame) -> pd.DataFrame:
    """Calcula una fila por equipo para el conjunto de partidos recibido.

    Filtrar temporada, torneo y fase antes de llamar esta funcion.
    La tabla se ordena por puntos y alfabeticamente en caso de empate.
    """
    faltantes = sorted({"local", "visitante"} - set(partidos.columns))
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")

    equipos = pd.concat(
        [partidos["local"], partidos["visitante"]],
        ignore_index=True,
    )

    if equipos.empty:
        raise ValueError("No hay partidos para calcular la tabla.")
    if equipos.isna().any() or equipos.astype("string").str.strip().eq("").any():
        raise ValueError("Hay partidos con un equipo sin nombre.")

    tabla = pd.DataFrame([
        {"Equipo": equipo, **resumen_equipo(partidos, equipo)}
        for equipo in equipos.unique()
    ])
    tabla["DG"] = tabla["GF"] - tabla["GC"]

    columnas = ["Equipo", "PTS", "PJ", "PG", "PE", "PP", "GF", "GC", "DG"]
    return tabla[columnas].sort_values(
        ["PTS", "Equipo"], ascending=[False, True], ignore_index=True
    )


def tabla_anual_2026(partidos: pd.DataFrame) -> pd.DataFrame:
    """Ordena la tabla anual a partir de los partidos de zonas de 2026."""
    if "temporada" not in partidos or not partidos["temporada"].eq(2026).fillna(False).all():
        raise ValueError("Se esperaban partidos de la temporada 2026.")

    tabla = tabla_equipos(partidos)
    if len(tabla) != 30 or not tabla["PJ"].eq(32).all():
        raise ValueError("Se esperaban 30 equipos con 32 partidos cada uno.")

    criterios = ["PTS", "DG", "GF"]
    empatados = tabla.loc[tabla.duplicated(subset=criterios, keep=False)]

    # Orden publicado por RSSSF para el desempate de Fair Play.
    puesto_rsssf = {"Independiente": 13, "Defensa y Justicia": 14}
    balance_empatado = set(empatados[criterios].itertuples(index=False, name=None))

    if set(empatados["Equipo"]) != set(puesto_rsssf) or balance_empatado != {(47, 3, 39)}:
        raise ValueError("El empate no coincide con el documentado para 2026.")

    ordenada = (
        tabla.assign(_puesto_rsssf=tabla["Equipo"].map(puesto_rsssf))
        .sort_values(
            [*criterios, "_puesto_rsssf"],
            ascending=[False, False, False, True],
            ignore_index=True,
        )
        .drop(columns="_puesto_rsssf")
    )
    ordenada.insert(0, "Pos", ordenada.index + 1)
    return ordenada
