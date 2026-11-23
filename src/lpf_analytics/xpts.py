"""Puntos esperados a partir del xG de cada remate registrado."""

from collections.abc import Iterable
from math import fsum


def _distribucion_goles(xg: Iterable[float]) -> list[float]:
    """Calcula la probabilidad de marcar cada cantidad posible de goles."""
    distribucion = [1.0]

    for probabilidad_gol in xg:
        if not 0 <= probabilidad_gol <= 1:
            raise ValueError("Cada valor de xG debe estar entre 0 y 1.")

        actualizada = [0.0] * (len(distribucion) + 1)
        for goles, probabilidad_previa in enumerate(distribucion):
            actualizada[goles] += probabilidad_previa * (1 - probabilidad_gol)
            actualizada[goles + 1] += probabilidad_previa * probabilidad_gol
        distribucion = actualizada

    return distribucion


def calcular_xpts(
    xg_favor: Iterable[float], xg_contra: Iterable[float]
) -> dict[str, float]:
    """Estima las probabilidades del resultado y los puntos de un equipo."""
    goles_favor = _distribucion_goles(xg_favor)
    goles_contra = _distribucion_goles(xg_contra)

    victoria = fsum(
        probabilidad * fsum(goles_contra[:goles])
        for goles, probabilidad in enumerate(goles_favor)
    )
    empate = fsum(
        favor * contra for favor, contra in zip(goles_favor, goles_contra)
    )
    derrota = fsum(
        probabilidad * fsum(goles_favor[:goles])
        for goles, probabilidad in enumerate(goles_contra)
    )

    return {
        "prob_victoria": victoria,
        "prob_empate": empate,
        "prob_derrota": derrota,
        "xPTS": 3 * victoria + empate,
    }