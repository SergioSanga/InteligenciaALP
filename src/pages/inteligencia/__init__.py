"""
Módulo: Inteligencia Territorial y Potencial de Firmas
Bolivia · Elecciones Subnacionales 2026

Incluye:
- Dashboard estratégico (IPRF)
- Potencial de Recolección de Firmas
- Mapa de calor territorial
- Rankings territoriales
- Recomendaciones automáticas
"""

from dash import html

from src.pages.inteligencia.dashboard import layout as dashboard_layout
from src.pages.inteligencia.potencial import layout as potencial_layout


def layout() -> html.Div:
    return html.Div([
        html.Div(
            className="construccion-overlay",
            children=[
                html.Div(
                    className="construccion-box",
                    children=[
                        html.Div("🚧", className="construccion-icon"),
                        html.Div("Módulo en Construcción", className="construccion-title"),
                        html.Div("Esta sección estará disponible pronto.", className="construccion-sub"),
                        html.Div("Próximamente: Análisis Territorial y Recolección de Firmas", className="construccion-detail"),
                    ],
                ),
            ],
        ),
    ])