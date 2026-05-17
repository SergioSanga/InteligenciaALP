"""
Carga y caché de todos los datasets de la aplicación.

Este módulo es el único punto de contacto con el sistema de archivos para datos.
Los datos se cargan una vez al inicio y se almacenan en memoria.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path

from config import DATA_FILES

log = logging.getLogger(__name__)


def _load_json(path: Path) -> dict:
    """Carga un archivo JSON desde disco. Lanza FileNotFoundError si no existe."""
    if not path.exists():
        raise FileNotFoundError(f"Archivo de datos no encontrado: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def get_municipios_v1() -> dict:
    """343 municipios con resultados de alcalde (1ª vuelta)."""
    return _load_json(DATA_FILES["municipios_v1"])


@lru_cache(maxsize=None)
def get_municipios_v2() -> dict:
    """151 municipios con resultados de gobernador (2ª vuelta)."""
    return _load_json(DATA_FILES["municipios_v2"])


@lru_cache(maxsize=None)
def get_departamentos() -> dict:
    """9 departamentos con resultado agregado de gobernación (1ª vuelta)."""
    return _load_json(DATA_FILES["departamentos"])


@lru_cache(maxsize=None)
def get_gobernaciones_v1() -> dict:
    """Resultados de gobernación por partido para los 9 departamentos (1ª vuelta)."""
    return _load_json(DATA_FILES["gobernaciones_v1"])


@lru_cache(maxsize=None)
def get_gobernaciones_v2() -> dict:
    """Resultados de ballottage para los 5 departamentos con 2ª vuelta."""
    return _load_json(DATA_FILES["gobernaciones_v2"])


@lru_cache(maxsize=None)
def get_recintos_resultados(eleccion: str = "gobernador") -> dict:
    """Resultados por recinto de la primera vuelta para gobernador o alcalde."""
    key = "recintos_alcalde" if eleccion == "alcalde" else "recintos_gobernador"
    return _load_json(DATA_FILES[key])


@lru_cache(maxsize=None)
def get_recintos_municipios() -> dict:
    """Municipios usados por los artefactos de recintos."""
    return _load_json(DATA_FILES["recintos_municipios"])


@lru_cache(maxsize=None)
def get_recintos_departamentos() -> dict:
    """Departamentos usados por los artefactos de recintos."""
    return _load_json(DATA_FILES["recintos_deptos"])


@lru_cache(maxsize=None)
def get_recintos_timestamp() -> str:
    """Fecha/hora de actualización del artefacto de recintos."""
    path = DATA_FILES["recintos_timestamp"]
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def get_depts_con_segunda_vuelta() -> set[str]:
    """Retorna el conjunto de IDs de departamento que tuvieron 2ª vuelta."""
    return set(get_gobernaciones_v2().keys())


@lru_cache(maxsize=None)
def get_geojson() -> dict:
    """GeoJSON con geometrías de los 343 municipios de Bolivia."""
    from config import GEOJSON_FILE
    return _load_json(GEOJSON_FILE)
