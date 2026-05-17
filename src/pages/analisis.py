"""
Página: Análisis.

Visualizaciones exploratorias a nivel nacional:
  - Habilitados ganados por partido (top 10)
  - Participación por departamento
  - Treemap nacional Bolivia → Departamento → Municipio
  - Scatter participación vs % ganador
"""

from dash import dcc, html

from src.components.figures import (
    municipios_bars,
    participacion_bars,
    partidos_habilitados_bars,
    scatter_participacion,
    treemap_nacional,
)
from src.components.ui import section_header
from src.utils.transforms import (
    habilitados_por_partido,
    participacion_por_departamento,
    todos_municipios_v1,
)


def layout() -> html.Div:
    df_partidos = habilitados_por_partido()
    df_part     = participacion_por_departamento()
    df_all      = todos_municipios_v1()

    fig_partidos = partidos_habilitados_bars(df_partidos, top=10)
    fig_part     = participacion_bars(df_part)
    fig_tree     = treemap_nacional(df_all)
    fig_scatter  = scatter_participacion(df_all)

    return html.Div([
        html.Div(
            className="two-col",
            style={"marginBottom": "16px"},
            children=[
                html.Div(
                    className="card",
                    children=[
                        section_header(
                            "Habilitados ganados por partido",
                            "Top 10 · guardias · 1ª vuelta · nivel nacional",
                        ),
                        dcc.Graph(figure=fig_partidos, config={"displayModeBar": False}),
                    ],
                ),
                html.Div(
                    className="card",
                    children=[
                        section_header(
                            "Participación por departamento",
                            "Gobernaciones · 1ª vuelta · color = ganador final",
                        ),
                        dcc.Graph(figure=fig_part, config={"displayModeBar": False}),
                    ],
                ),
            ],
        ),
        html.Div(
            className="card",
            style={"marginBottom": "16px"},
            children=[
                section_header(
                    "Distribución nacional de habilitados",
                    "Bolivia → Departamento → Municipio · tamaño = habilitados · color = partido ganador",
                ),
                dcc.Graph(figure=fig_tree, config={"displayModeBar": False}),
            ],
        ),
        html.Div(
            className="card",
            children=[
                section_header(
                    "Participación vs. % del ganador",
                    "Municipios · alcalde · 1ª vuelta · cada punto = un municipio",
                ),
                dcc.Graph(figure=fig_scatter, config={"displayModeBar": False}),
            ],
        ),
    ])