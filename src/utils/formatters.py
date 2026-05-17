"""
Funciones de formateo para números, porcentajes y texto.
"""


def fmt_number(n: int | float) -> str:
    """Formatea un número con separadores de miles. Ej: 1234567 → '1,234,567'"""
    return f"{int(n):,}"


def fmt_pct(ratio: float, decimals: int = 1) -> str:
    """Convierte un ratio (0–1) a porcentaje formateado. Ej: 0.456 → '45.6%'"""
    return f"{ratio * 100:.{decimals}f}%"


def fmt_pct_raw(value: float, decimals: int = 1) -> str:
    """Formatea un valor ya en porcentaje. Ej: 45.6 → '45.6%'"""
    return f"{value:.{decimals}f}%"


def title_case(text: str) -> str:
    """Capitaliza correctamente texto en español."""
    return text.strip().title()