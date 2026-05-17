"""
Data loader para el módulo de Inteligencia Territorial.
Carga datos de elecciones 2025 y Atlas Urbano.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from data.elecciones2025 import (
    PRESIDENCIALES_V1,
    PRESIDENCIALES_V2,
    MUNICIPIOS_PRESIDENCIALES,
    RECINTOS_PRESIDENCIALES,
)


def get_presidencial_v1_data() -> dict:
    """Retorna datos de primera vuelta presidencial 2025."""
    return PRESIDENCIALES_V1


def get_presidencial_v2_data() -> dict:
    """Retorna datos de segunda vuelta presidencial 2025."""
    return PRESIDENCIALES_V2


def get_municipios_presidenciales() -> list:
    """Retorna lista de municipios con datos de elecciones 2025."""
    return MUNICIPIOS_PRESIDENCIALES


def get_recintos_presidenciales() -> list:
    """Retorna lista de recintos con datos de elecciones 2025."""
    return RECINTOS_PRESIDENCIALES


def get_departamentos_presidenciales() -> dict:
    """Retorna diccionario de departamentos con datos combinadas."""
    deptos = {}
    
    for key, data in PRESIDENCIALES_V1.items():
        deptos[key] = {
            "nombre": data["nombre"],
            "presidencial_v1": data["resultados"],
            "participacion_v1": data["participacion"],
            "votantes_v1": data["votantes_habilitados"],
        }
    
    for key, data in PRESIDENCIALES_V2.items():
        if key in deptos:
            deptos[key]["presidencial_v2"] = data["resultados"]
            deptos[key]["participacion_v2"] = data["participacion"]
            deptos[key]["votantes_v2"] = data["votantes_habilitados"]
        else:
            deptos[key] = {
                "nombre": data["nombre"],
                "presidencial_v2": data["resultados"],
                "participacion_v2": data["participacion"],
                "votantes_v2": data["votantes_habilitados"],
            }
    
    for mun in MUNICIPIOS_PRESIDENCIALES:
        dept_key = mun["departamento"].lower().replace(" ", "_")
        if dept_key not in deptos:
            deptos[dept_key] = {"nombre": mun["departamento"]}
        
        if "municipios" not in deptos[dept_key]:
            deptos[dept_key]["municipios"] = []
        deptos[dept_key]["municipios"].append(mun)
        
        if "atlas" not in deptos[dept_key]:
            deptos[dept_key]["atlas"] = {
                "votantes_presidenciales": mun["votantes"],
                "recintos": mun["recintos"],
                "densidad_poblacional": mun["densidad"],
                "clasificacion": mun["clasificacion"],
            }
    
    return deptos


ATLAS_URBANO = {
    "la_paz": {
        "nombre": "La Paz",
        "poblacion": 812000,
        "densidad": 2800,
        "superficie_km2": 290,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 95,
        "municipios": 20,
        "recintos": 1800,
        "acceso_vial": "Alto",
        "nivel_socioeconomico": "Medio-Alto",
        "movilidad": "Alta",
        "potencial_movilizacion": 85,
    },
    "el_alto": {
        "nombre": "El Alto",
        "poblacion": 1100000,
        "densidad": 3200,
        "superficie_km2": 350,
        "clasificacion": "Ciudad Principal",
        "indice_urbano": 88,
        "municipios": 1,
        "recintos": 2200,
        "acceso_vial": "Alto",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Alta",
        "potencial_movilizacion": 92,
    },
    "santa_cruz": {
        "nombre": "Santa Cruz de la Sierra",
        "poblacion": 1650000,
        "densidad": 4200,
        "superficie_km2": 395,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 98,
        "municipios": 1,
        "recintos": 3200,
        "acceso_vial": "Alto",
        "nivel_socioeconomico": "Medio-Alto",
        "movilidad": "Muy Alta",
        "potencial_movilizacion": 95,
    },
    "cochabamba": {
        "nombre": "Cochabamba",
        "poblacion": 630000,
        "densidad": 3100,
        "superficie_km2": 200,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 92,
        "municipios": 1,
        "recintos": 1450,
        "acceso_vial": "Alto",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Alta",
        "potencial_movilizacion": 88,
    },
    "sucre": {
        "nombre": "Sucre",
        "poblacion": 290000,
        "densidad": 2200,
        "superficie_km2": 130,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 78,
        "municipios": 1,
        "recintos": 580,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Media",
        "potencial_movilizacion": 72,
    },
    "tarija": {
        "nombre": "Tarija",
        "poblacion": 350000,
        "densidad": 2500,
        "superficie_km2": 140,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 82,
        "municipios": 1,
        "recintos": 720,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio-Alto",
        "movilidad": "Alta",
        "potencial_movilizacion": 78,
    },
    "potosi": {
        "nombre": "Potosí",
        "poblacion": 245000,
        "densidad": 1800,
        "superficie_km2": 135,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 75,
        "municipios": 1,
        "recintos": 520,
        "acceso_vial": "Bajo",
        "nivel_socioeconomico": "Medio-Bajo",
        "movilidad": "Media",
        "potencial_movilizacion": 68,
    },
    "oruro": {
        "nombre": "Oruro",
        "poblacion": 285000,
        "densidad": 2400,
        "superficie_km2": 118,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 76,
        "municipios": 1,
        "recintos": 580,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Media",
        "potencial_movilizacion": 70,
    },
    "trinidad": {
        "nombre": "Trinidad",
        "poblacion": 145000,
        "densidad": 1500,
        "superficie_km2": 95,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 68,
        "municipios": 1,
        "recintos": 320,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Media",
        "potencial_movilizacion": 62,
    },
    "cobija": {
        "nombre": "Cobija",
        "poblacion": 65000,
        "densidad": 1250,
        "superficie_km2": 52,
        "clasificacion": "Capital Metrópoli",
        "indice_urbano": 62,
        "municipios": 1,
        "recintos": 140,
        "acceso_vial": "Bajo",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Baja",
        "potencial_movilizacion": 55,
    },
    "ciudad_intermedia_1": {
        "nombre": "Ciudades Intermedias",
        "poblacion": 850000,
        "densidad": 1200,
        "superficie_km2": 850,
        "clasificacion": "Ciudad Intermedia",
        "indice_urbano": 65,
        "municipios": 45,
        "recintos": 1800,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio",
        "movilidad": "Media",
        "potencial_movilizacion": 60,
    },
    "area_periurbana": {
        "nombre": "Áreas Periurbanas",
        "poblacion": 1200000,
        "densidad": 800,
        "superficie_km2": 1800,
        "clasificacion": "Área Periurbana",
        "indice_urbano": 55,
        "municipios": 85,
        "recintos": 2500,
        "acceso_vial": "Medio",
        "nivel_socioeconomico": "Medio-Bajo",
        "movilidad": "Media",
        "potencial_movilizacion": 52,
    },
    "area_rural": {
        "nombre": "Áreas Rurales",
        "poblacion": 2100000,
        "densidad": 45,
        "superficie_km2": 65000,
        "clasificacion": "Área Rural",
        "indice_urbano": 25,
        "municipios": 280,
        "recintos": 4200,
        "acceso_vial": "Bajo",
        "nivel_socioeconomico": "Bajo",
        "movilidad": "Baja",
        "potencial_movilizacion": 35,
    },
}


def get_atlas_data() -> dict:
    """Retorna datos del Atlas Urbano de Bolivia."""
    return ATLAS_URBANO


def get_atlas_por_departamento(dept_key: str) -> dict:
    """Retorna datos del atlas para un departamento específico."""
    return ATLAS_URBANO.get(dept_key.lower(), ATLAS_URBANO["area_periurbana"])