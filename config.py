"""
Configuración central de la aplicación.
Constantes, rutas y paleta de colores.
"""

from pathlib import Path

# ── Rutas ────────────────────────────────────────────────────────────────────
# ROOT_DIR siempre apunta al directorio que contiene app.py,
# independientemente de desde dónde se importe config.py.

def _find_root() -> Path:
    """
    Sube desde este archivo hasta encontrar el directorio que contiene app.py.
    Garantiza que DATA_DIR funcione sin importar la estructura de importación
    o el working directory actual.
    """
    candidate = Path(__file__).resolve().parent
    for _ in range(4):
        if (candidate / "app.py").exists():
            return candidate
        candidate = candidate.parent
    return Path(__file__).resolve().parent


ROOT_DIR   = _find_root()
DATA_DIR   = ROOT_DIR / "data"
ASSETS_DIR = ROOT_DIR / "src" / "assets"

DATA_FILES = {
    "municipios_v1":    DATA_DIR / "municipios_primera_vuelta.json",
    "municipios_v2":    DATA_DIR / "municipios_segunda_vuelta.json",
    "departamentos":    DATA_DIR / "departamentos.json",
    "gobernaciones_v1": DATA_DIR / "gobernaciones_primera_vuelta.json",
    "gobernaciones_v2": DATA_DIR / "gobernaciones_segunda_vuelta.json",
    "recintos_gobernador": DATA_DIR / "recintos" / "primera_vuelta" / "resultados_gobernador.json",
    "recintos_alcalde":    DATA_DIR / "recintos" / "primera_vuelta" / "resultados_alcalde.json",
    "recintos_municipios": DATA_DIR / "recintos" / "primera_vuelta" / "municipios.json",
    "recintos_deptos":     DATA_DIR / "recintos" / "primera_vuelta" / "departamentos.json",
    "recintos_timestamp":  DATA_DIR / "recintos" / "primera_vuelta" / "timestamp",
}

# ── App ───────────────────────────────────────────────────────────────────────

APP_TITLE = "Bolivia · Elecciones Subnacionales 2026"
APP_HOST  = "0.0.0.0"
APP_PORT  = 8050
APP_DEBUG = False

# ── Paleta de partidos ────────────────────────────────────────────────────────

PARTY_COLORS: dict[str, str] = {
    "AGN":                   "#4F86C6",
    "PATRIA-UNIDOS":         "#E07B39",
    "PATRIA-SOL":            "#E07B39",
    "PATRIA":                "#E07B39",
    "PATRIA-ORURO":          "#E07B39",
    "LIBRE":                 "#4CAF7D",
    "LIBRE-PANDO":           "#4CAF7D",
    "A-UPP":                 "#9C6FD6",
    "A.S.":                  "#26C6AA",
    "JACHAJAKISASOLFESORC":  "#EF5350",
    "MTS":                   "#F5A623",
    "NGP":                   "#5C9BD6",
    "APB-SUMATE":            "#66BB6A",
    "CREEMOS":               "#FFA726",
    "CREEMOS - PATRIA":      "#FFA726",
    "SPT":                   "#29B6F6",
    "CDC":                   "#AB47BC",
    "PDC":                   "#78909C",
    "MNR":                   "#FF7043",
    "DESPIERTA":             "#26A69A",
    "IH":                    "#42A5F5",
    "VENCEREMOS":            "#EC407A",
    "UPC":                   "#7E57C2",
    "ASLP":                  "#8D6E63",
    "VIDA":                  "#9CCC65",
    "AORA":                  "#26C6DA",
    "JALLALLA LP":           "#D4E157",
    "MDA":                   "#FF8A65",
    "UPP":                   "#4DB6AC",
    "FRI":                   "#BA68C8",
    "VOS":                   "#4FC3F7",
    "SOMOS":                 "#AED581",
    "FE":                    "#FFD54F",
    "otros":                 "#546E7A",
    "Sin datos":             "#1F2937",
}

FALLBACK_COLOR = "#607D8B"

# ── Tema oscuro ───────────────────────────────────────────────────────────────

DARK = {
    "bg_root":    "#080F1A",
    "bg_surface": "#0D1B2E",
    "bg_navbar":  "#0A1628",
    "border":     "rgba(255,255,255,0.055)",
    "text_hi":    "#F1F5F9",
    "text_mid":   "#CBD5E1",
    "text_lo":    "#64748B",
    "text_muted": "#475569",
    "accent":     "#3B82F6",
    "grid":       "rgba(255,255,255,0.04)",
}

# ── Plotly base layout ────────────────────────────────────────────────────────

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, system-ui, sans-serif", color=DARK["text_mid"], size=12),
    hoverlabel=dict(
        bgcolor="#0F172A",
        bordercolor="#334155",
        font=dict(color=DARK["text_hi"], size=12, family="Inter, sans-serif"),
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    margin=dict(t=12, b=12, l=8, r=90),
)

# GeoJSON de municipios usado por el mapa interactivo.
GEOJSON_FILE = DATA_DIR / "municipios.geojson"
