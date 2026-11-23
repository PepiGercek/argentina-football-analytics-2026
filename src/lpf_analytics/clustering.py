"""Agrupamiento exploratorio del rendimiento de los equipos."""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

from .resultados import tabla_equipos


def indicadores_rendimiento(partidos: pd.DataFrame) -> pd.DataFrame:
    """Calcula las tres variables de agrupamiento a partir de los resultados."""
    equipos = tabla_equipos(partidos).set_index("Equipo")
    jugados = equipos["PJ"]

    return pd.DataFrame({
        "GF_por_partido": equipos["GF"] / jugados,
        "GC_por_partido": equipos["GC"] / jugados,
        "Proporcion_empates": equipos["PE"] / jugados,
    })


def _crear_modelo(k: int) -> Pipeline:
    return make_pipeline(
        StandardScaler(),
        KMeans(n_clusters=k, n_init=30, random_state=42),
    )


def evaluar_grupos(indicadores: pd.DataFrame) -> pd.DataFrame:
    """Compara de dos a seis grupos para los 30 clubes de la LPF."""
    escalados = StandardScaler().fit_transform(indicadores)
    rng = np.random.default_rng(42)
    muestras = [
        np.sort(rng.choice(len(indicadores), size=24, replace=False))
        for _ in range(40)
    ]

    filas = []
    for k in range(2, 7):
        referencia = _crear_modelo(k).fit_predict(indicadores)
        tamanos = pd.Series(referencia).value_counts().sort_values(ascending=False)

        coincidencias = []
        for indices in muestras:
            modelo = _crear_modelo(k).fit(indicadores.iloc[indices])
            asignacion = modelo.predict(indicadores)
            coincidencias.append(adjusted_rand_score(referencia, asignacion))

        filas.append({
            "Grupos": k,
            "Silueta": silhouette_score(escalados, referencia),
            "Equipos_por_grupo": ", ".join(map(str, tamanos)),
            "ARI_mediana": np.median(coincidencias),
            "ARI_percentil_10": np.quantile(coincidencias, 0.10),
        })

    return pd.DataFrame(filas).set_index("Grupos")


def agrupar_equipos(indicadores: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    """Asigna un grupo a cada equipo y conserva las variables originales."""
    grupos = _crear_modelo(k).fit_predict(indicadores)
    return indicadores.assign(Grupo=grupos + 1)