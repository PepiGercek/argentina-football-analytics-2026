"""Descarga las fichas de formación pendientes de Boca."""

import json
from argparse import ArgumentParser
from getpass import getpass
from os import getenv
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .formaciones import cargar_formaciones_boca

ENDPOINT = "https://mcp.strikerapi.com/v1/get_lineups"
CREDITOS_POR_FICHA = 5


def consultar_ficha(game_id: str, clave_api: str) -> dict:
    cuerpo = json.dumps({"game_id": game_id, "league": "argentina"}).encode("utf-8")
    solicitud = Request(
        ENDPOINT,
        data=cuerpo,
        headers={
            "Content-Type": "application/json",
            "x-idempotency-key": f"lpf-2026-formacion-{game_id}",
        },
        method="POST",
    )
    solicitud.add_unredirected_header("x-api-key", clave_api)

    try:
        with urlopen(solicitud, timeout=30) as respuesta:
            ficha = json.load(respuesta)["data"]
    except HTTPError as error:
        raise SystemExit(f"Error HTTP {error.code} al consultar {game_id}.") from None
    except (URLError, TimeoutError):
        raise SystemExit(f"Falló la conexión al consultar {game_id}.") from None

    if ficha["game"]["game_id"] != game_id:
        raise ValueError(f"La API devolvió un ID distinto de {game_id}.")

    boca = [equipo for equipo in ficha["lineups"] if equipo["abbrev"] == "CABJ"]
    if len(boca) != 1:
        raise ValueError(f"Se esperaba una alineación de Boca para {game_id}.")

    return ficha


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--descargar", action="store_true", help="Ejecuta las consultas pendientes."
    )
    args = parser.parse_args()

    carpeta = Path("data/raw")
    tabla = cargar_formaciones_boca(carpeta)
    if len(tabla) != 32:
        raise SystemExit("Se esperaban los 32 partidos de zonas de Boca.")

    pendientes = tabla.loc[tabla["titulares"].isna(), "game_id"].tolist()
    print(f"Fichas pendientes: {len(pendientes)}")
    print(f"Créditos estimados: {len(pendientes) * CREDITOS_POR_FICHA}")

    if not args.descargar or not pendientes:
        return

    clave_api = getenv("LPF_STRIKERAPI_API_KEY", "").strip()
    if not clave_api:
        clave_api = getpass("Pegá tu clave de StrikerAPI y presioná Enter: ").strip()
    if not clave_api:
        raise SystemExit("Ingresá una clave para ejecutar las consultas.")

    with TemporaryDirectory(dir=carpeta) as temporal:
        for posicion, game_id in enumerate(pendientes, start=1):
            ficha = consultar_ficha(game_id, clave_api)
            nombre = f"strikerapi_boca_formaciones_{game_id}.json"
            archivo_temporal = Path(temporal) / nombre
            archivo_temporal.write_text(
                json.dumps(ficha, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            archivo_temporal.replace(carpeta / nombre)
            print(f"{posicion}/{len(pendientes)} · Ficha {game_id} guardada", flush=True)

            if posicion < len(pendientes):
                sleep(1.1)


if __name__ == "__main__":
    main()