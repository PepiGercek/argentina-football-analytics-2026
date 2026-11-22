"""Genera un mapa comparativo de los remates de Boca en las dos fases de zonas."""

import json
from math import asin, degrees
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Rectangle

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data/raw"
ANCHO = 68
DISTANCIA_PENAL = 11
MEDIA_CANCHA = DISTANCIA_PENAL / 0.23
AZUL = "#215CA3"
DORADO = "#A45B08"
LINEAS = "#A1ACB8"

CICLOS = {
    "Torneo Apertura": ("Apertura", "Claudio Úbeda"),
    "Torneo Clausura": ("Clausura", "Rodolfo Arruabarrena"),
}


def leer_respuesta(tipo):
    ruta = DATOS / f"strikerapi_boca_{tipo}_2026.json"
    return json.loads(ruta.read_text(encoding="utf-8-sig"))


def dibujar_cancha(eje):
    centro = ANCHO / 2
    eje.add_patch(Rectangle(
        (0, 0), ANCHO, MEDIA_CANCHA, facecolor="#F3F6F8", edgecolor=LINEAS
    ))
    for profundidad in (5.5, 16.5):
        ancho_area = 7.32 + 2 * profundidad
        eje.add_patch(Rectangle(
            (centro - ancho_area / 2, 0), ancho_area, profundidad,
            fill=False, edgecolor=LINEAS,
        ))

    eje.add_patch(Rectangle(
        (centro - 7.32 / 2, -2), 7.32, 2, fill=False, edgecolor=LINEAS
    ))
    eje.scatter(centro, DISTANCIA_PENAL, s=8, color=LINEAS)

    radio = 9.15
    angulo = degrees(asin((16.5 - DISTANCIA_PENAL) / radio))
    eje.add_patch(Arc(
        (centro, DISTANCIA_PENAL), 2 * radio, 2 * radio,
        theta1=angulo, theta2=180 - angulo, color=LINEAS,
    ))
    eje.add_patch(Arc(
        (centro, MEDIA_CANCHA), 2 * radio, 2 * radio,
        theta1=180, theta2=360, color=LINEAS,
    ))
    eje.set_xlim(-1, ANCHO + 1)
    eje.set_ylim(MEDIA_CANCHA + 1, -3)
    eje.set_aspect("equal")
    eje.axis("off")


def generar_mapa():
    partidos = pd.DataFrame(leer_respuesta("partidos")["games"])[["game_id", "stage"]]
    remates = pd.DataFrame(leer_respuesta("remates_favor")["shots"])
    zonas = remates.merge(partidos, on="game_id", validate="many_to_one")

    figura, ejes = plt.subplots(1, 2, figsize=(12, 6.8), facecolor="white")
    figura.subplots_adjust(left=0.05, right=0.95, bottom=0.16, top=0.76, wspace=0.10)
    figura.text(0.05, 0.94, "Dónde remató Boca en 2026", fontsize=26, weight="bold")
    figura.text(0.05, 0.88, "Comparación de los ciclos en las fases de zonas", fontsize=13)

    for eje, (torneo, (nombre, entrenador)) in zip(ejes, CICLOS.items(), strict=True):
        detalle = zonas.loc[zonas["stage"].eq(torneo)]
        goles = detalle["outcome"].eq("goal")
        dibujar_cancha(eje)

        otros = detalle.loc[~goles]
        eje.scatter(
            otros["y"] * ANCHO, otros["x"] * MEDIA_CANCHA,
            s=16 + 240 * otros["xg"], color=AZUL, alpha=0.35, linewidths=0,
        )
        convertidos = detalle.loc[goles]
        eje.scatter(
            convertidos["y"] * ANCHO, convertidos["x"] * MEDIA_CANCHA,
            s=16 + 240 * convertidos["xg"], facecolors="none",
            edgecolors=DORADO, linewidths=1.5,
        )

        eje.set_title(
            f"{nombre} · {entrenador}",
            loc="left",
            fontsize=15,
            weight="bold",
            pad=24,
        )
        eje.text(
            0, 1.0, f"{len(detalle)} remates · {goles.sum()} goles",
            transform=eje.transAxes,
            fontsize=10,
            color="#475467",
            va="bottom",
        )

    leyenda = [
        Line2D([], [], marker="o", linestyle="none", color=AZUL, label="Remate sin gol"),
        Line2D([], [], marker="o", linestyle="none", markerfacecolor="none",
               markeredgecolor=DORADO, label="Gol"),
    ]
    figura.legend(handles=leyenda, loc="lower left", bbox_to_anchor=(0.05, 0.085),
                  ncol=2, frameon=False)
    figura.text(0.05, 0.065, "El tamaño del punto aumenta con el xG.", fontsize=10)
    figura.text(
        0.05, 0.035, "StrikerAPI · Remates con coordenadas y xG · Cancha esquemática",
        fontsize=9, color="#475467",
    )

    destino = RAIZ / "reports/mapa_remates_boca_2026.png"
    figura.savefig(destino, dpi=180)
    plt.close(figura)
    print(f"Mapa guardado en {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    generar_mapa()