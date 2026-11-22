"""Genera el gráfico de puntos acumulados de los tres primeros de la LPF 2026."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from lpf_analytics.evolucion import evolucion_equipos
from lpf_analytics.resultados import tabla_anual_2026


raiz = Path(__file__).resolve().parents[1]
partidos = pd.read_csv(
    raiz / "data/raw/LPF_2026_partidos.csv", encoding="utf-8-sig"
)
evolucion = evolucion_equipos(partidos)
top3 = tabla_anual_2026(partidos).head(3)

inicio = evolucion["fecha_jugada"].min() - pd.Timedelta(days=1)
fin = evolucion["fecha_jugada"].max()
fin_apertura = evolucion.loc[evolucion["torneo"].eq("Apertura"), "fecha_jugada"].max()
inicio_clausura = evolucion.loc[evolucion["torneo"].eq("Clausura"), "fecha_jugada"].min()

fig, ax = plt.subplots(figsize=(11.5, 6.5))
fig.subplots_adjust(left=0.09, right=0.96, top=0.80, bottom=0.18)
fig.text(0.09, 0.92, "La carrera por la tabla anual", fontsize=22, weight="bold")
fig.text(0.09, 0.865, "LPF 2026 | Los tres primeros al cierre del año", fontsize=12)

ax.axvspan(fin_apertura, inicio_clausura, color="#e9edf3")
ax.text(
    fin_apertura + (inicio_clausura - fin_apertura) / 2,
    5, "Receso entre torneos", ha="center", color="#515b68", fontsize=9,
)

estilos = [("#17469e", "-"), ("#a85c00", "--"), ("#ad3655", ":")]
for fila, (color, estilo) in zip(top3.itertuples(index=False), estilos):
    serie = evolucion.loc[evolucion["equipo"].eq(fila.Equipo)]
    dias = [inicio, *serie["fecha_jugada"], fin]
    puntos = [0, *serie["puntos_acumulados"], fila.PTS]
    ax.step(
        dias, puntos, where="post", color=color, linestyle=estilo,
        linewidth=2.5, label=f"{fila.Equipo} ({fila.PTS} pts)",
    )

ax.set_xlim(inicio, fin + pd.Timedelta(days=5))
ax.set_ylim(0, 68)
ax.set_ylabel("Puntos acumulados")
ax.set_xlabel("Fecha de juego")
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.set_axisbelow(True)
ax.grid(axis="y", color="#d8dde5", linewidth=0.7)
ax.legend(loc="upper left", frameon=False)
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)

fig.text(
    0.09, 0.05,
    "Resultados: Osvaldo José Gorgazzi / RSSSF, Argentina 2026. "
    "Fases de zonas del Apertura y Clausura.",
    fontsize=9, color="#515b68",
)

ruta = raiz / "reports/evolucion_puntos_top3_2026.png"
fig.savefig(ruta, dpi=180)
plt.close(fig)
print("Gráfico guardado:", ruta.relative_to(raiz))
