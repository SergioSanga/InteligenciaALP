"""
Lógica del Índice de Potencial de Recolección de Firmas (IPRF)
para el módulo de Inteligencia Territorial.
"""

import pandas as pd

PESOS = {
    "afinidad_politica": 0.30,
    "participacion": 0.20,
    "densidad_poblacional": 0.15,
    "concentracion_urbana": 0.15,
    "accesibilidad": 0.10,
    "movilizacion": 0.10,
}

PARTIDOS_ALIADOS = [
    "LIBRE", "MAS-IPSP", "BC", "FD", "PAN-BOL", "SUMA", "MNR",
    "alianza", "izquierda", "progresista"
]

PARTIDOS_OPOSICION = [
    "CREEMOS", "BB", "JHE", "vamos", "unidad",
    "dc", "pdc", "vertebrado", "adversario"
]


def calcular_pct_voto(df: pd.DataFrame, partido: str) -> float:
    """Calcula el porcentaje de votos para un partido específico."""
    if df.empty:
        return 0.0
    total = df["votos"].sum()
    if total == 0:
        return 0.0
    voto_partido = df[df["partido"].str.upper().str.contains(partido.upper(), na=False)]["votos"].sum()
    return (voto_partido / total) * 100


def afinidad_politica(pres_v1: pd.DataFrame, pres_v2: pd.DataFrame, partido_target: str = "MAS") -> float:
    """
    Calcula la afinidad política de una zona.
    Retorna score 0-100 basado en votación del partido objetivo.
    """
    v1_pct = calcular_pct_voto(pres_v1, partido_target)
    v2_pct = calcular_pct_voto(pres_v2, partido_target)

    if pres_v1.empty and pres_v2.empty:
        return 50.0

    if pres_v1.empty:
        return v2_pct
    if pres_v2.empty:
        return v1_pct

    return (v1_pct + v2_pct) / 2


def calcular_participacion(df: pd.DataFrame) -> float:
    """Calcula el porcentaje de participación electoral."""
    if df.empty:
        return 50.0
    if "participacion" in df.columns:
        return float(df["participacion"].iloc[0])
    return 75.0


def impacto_participacion(participacion: float) -> float:
    """
    Convierte participación en score (mayor participación = mayor potencial).
    Fórmula: participación superior al 75% es óptimo.
    """
    if participacion >= 85:
        return 100.0
    elif participacion >= 75:
        return 75.0 + (participacion - 75) * 2.5
    elif participacion >= 60:
        return 50.0 + (participacion - 60) * 1.67
    elif participacion >= 40:
        return 25.0 + (participacion - 40) * 1.25
    else:
        return participacion * 0.625


def indice_densidad(densidad: float) -> float:
    """
    Convierte densidad poblacional en score.
    Zonas con densidad media-alta (500-2000 hab/km²) son óptimas.
    """
    if densidad >= 2000:
        return 100.0
    elif densidad >= 1000:
        return 80.0 + (densidad - 1000) * 0.02
    elif densidad >= 500:
        return 60.0 + (densidad - 500) * 0.04
    elif densidad >= 100:
        return 30.0 + (densidad - 100) * 0.375
    elif densidad >= 10:
        return 10.0 + (densidad - 10) * 0.22
    else:
        return max(5.0, densidad * 0.5)


def indice_urbano(urbano: str) -> float:
    """Score basado en clasificación urbana."""
    urbano_lower = urbano.lower() if isinstance(urbano, str) else ""
    if "capital" in urbano_lower or "metropoli" in urbano_lower:
        return 100.0
    elif "ciudad" in urbano_lower or "urbano" in urbano_lower:
        return 75.0
    elif "peri" in urbano_lower:
        return 50.0
    elif "rural" in urbano_lower:
        return 30.0
    else:
        return 40.0


def indice_movilizacion(voters: int, recintos: int) -> float:
    """
    Score basado en concentración de voters y recintos.
    Más voters y recintos = mayor potencial de collecte.
    """
    if recintos == 0:
        return 20.0

    avg_votantes_recinto = voters / recintos if recintos > 0 else 0

    if voters >= 50000:
        base = 100.0
    elif voters >= 20000:
        base = 75.0 + (voters - 20000) / 2000
    elif voters >= 5000:
        base = 50.0 + (voters - 5000) / 500
    elif voters >= 1000:
        base = 25.0 + (voters - 1000) / 160
    else:
        base = 10.0 + voters / 100

    if avg_votantes_recinto >= 500:
        return min(100, base * 1.1)
    elif avg_votantes_recinto >= 200:
        return base
    else:
        return max(10, base * 0.8)


def calcular_iprf(
    afi: float,
    part: float,
    dens: float,
    urb: float,
    mov: float,
) -> float:
    """
    Calcula el Índice de Potencial de Recolección de Firmas (IPRF).
    Ponderación configurable.
    """
    iprf = (
        afi * PESOS["afinidad_politica"] +
        part * PESOS["participacion"] +
        dens * PESOS["densidad_poblacional"] +
        urb * PESOS["concentracion_urbana"] +
        mov * PESOS["movilizacion"]
    )
    return round(iprf, 1)


def clasificar_prioridad(iprf: float) -> str:
    """Clasifica el IPRF en niveles de prioridad."""
    if iprf >= 75:
        return "Alta"
    elif iprf >= 50:
        return "Media"
    else:
        return "Baja"


def ranking_deptos() -> pd.DataFrame:
    """Genera ranking de departamentos por IPRF."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root))
    from data.elecciones2025.presidenciales import PRESIDENCIALES_V1, PRESIDENCIALES_V2, MUNICIPIOS_PRESIDENCIALES

    deptos_nombres = {
        "la_paz": "La Paz", "santa_cruz": "Santa Cruz", "cochabamba": "Cochabamba",
        "chuquisaca": "Chuquisaca", "tarija": "Tarija", "potosi": "Potosí",
        "oruro": "Oruro", "beni": "Beni", "pando": "Pando"
    }

    resultados = []

    for key, data in PRESIDENCIALES_V1.items():
        v1_data = pd.DataFrame(data["resultados"])

        v2_data = pd.DataFrame()
        if key in PRESIDENCIALES_V2:
            v2_data = pd.DataFrame(PRESIDENCIALES_V2[key]["resultados"])

        afi = afinidad_politica(v1_data, v2_data, "MAS")
        part = data["participacion"]
        part_score = impacto_participacion(part)

        muns = [m for m in MUNICIPIOS_PRESIDENCIALES if m["departamento"].lower().replace(" ", "_") == key]
        dens = sum(m["densidad"] for m in muns) / len(muns) if muns else 50
        dens_score = indice_densidad(dens)

        voters = data["votantes_habilitados"]
        recintos = sum(m["recintos"] for m in muns) if muns else 20
        urb_score = indice_urbano(muns[0]["clasificacion"]) if muns else 40
        mov_score = indice_movilizacion(voters, recintos)

        iprf = calcular_iprf(afi, part_score, dens_score, urb_score, mov_score)
        prioridad = clasificar_prioridad(iprf)

        resultados.append({
            "id": key,
            "nombre": deptos_nombres.get(key, key),
            "iprf": iprf,
            "prioridad": prioridad,
            "votantes": voters,
            "recintos": recintos,
            "participacion": round(part, 1),
            "afinidad": round(afi, 1),
            "densidad": round(dens, 0),
        })

    df = pd.DataFrame(resultados)
    return df.sort_values("iprf", ascending=False)


def ranking_municipios() -> pd.DataFrame:
    """Genera ranking de municipios por IPRF."""
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root))
    from data.elecciones2025.presidenciales import PRESIDENCIALES_V1, MUNICIPIOS_PRESIDENCIALES

    resultados = []

    for mun in MUNICIPIOS_PRESIDENCIALES:
        voters = mun["votantes"]
        recintos = mun["recintos"]
        dens = mun["densidad"]
        urb = mun["clasificacion"]

        dens_score = indice_densidad(dens)
        urb_score = indice_urbano(urb)
        mov_score = indice_movilizacion(voters, recintos)

        afi = 50.0 + (dens / 100)
        part_score = 70.0 + (recintos / 5)

        iprf = calcular_iprf(afi, part_score, dens_score, urb_score, mov_score)
        prioridad = clasificar_prioridad(iprf)

        resultados.append({
            "id": mun["id"],
            "nombre": mun["nombre"],
            "departamento": mun["departamento"],
            "provincia": mun["provincia"],
            "iprf": iprf,
            "prioridad": prioridad,
            "votantes": voters,
            "recintos": recintos,
            "participacion": round(70 + recintos / 2, 1),
            "afinidad": round(afi, 1),
            "densidad": dens,
            "clasificacion": urb,
        })

    df = pd.DataFrame(resultados)
    return df.sort_values("iprf", ascending=False)