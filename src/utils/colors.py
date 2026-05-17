"""
Utilidades de color para partidos políticos.
"""

from config import FALLBACK_COLOR, PARTY_COLORS


def party_color(party: str) -> str:
    """Retorna el color hex asignado a un partido, o el color por defecto."""
    return PARTY_COLORS.get(party, FALLBACK_COLOR)


def party_colors_list(parties: list[str]) -> list[str]:
    """Retorna una lista de colores para una lista de partidos."""
    return [party_color(p) for p in parties]


def badge_style(party: str) -> dict:
    """Retorna el estilo inline para un badge de partido."""
    c = party_color(party)
    return {
        "background": c + "22",
        "color": c,
        "border": f"1px solid {c}44",
    }