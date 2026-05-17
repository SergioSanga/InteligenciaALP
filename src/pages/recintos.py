"""
Pagina: Recintos electorales.
"""

from __future__ import annotations

from dash import dcc, html

from src.components.figures import mapa_recintos
from src.components.ui import empty_state, kpi_card, kpi_row, party_badge, section_header
from src.utils.data_loader import get_recintos_timestamp
from src.utils.formatters import fmt_number, fmt_pct_raw
from src.utils.transforms import departamentos_con_recintos, recintos_para_mapa


ELECCION_OPTIONS = [
    {"label": "Gobernador", "value": "gobernador"},
    {"label": "Alcalde", "value": "alcalde"},
]

METRICA_OPTIONS = [
    {"label": "% del ganador", "value": "pct_ganador"},
    {"label": "Blanco/nulo %", "value": "invalidos_pct"},
    {"label": "Partido ganador", "value": "partido"},
]


def layout() -> html.Div:
    return html.Div([
        html.Div(
            className="controls-row",
            children=[
                html.Div(className="control-group", children=[
                    html.Label("Eleccion", className="control-label"),
                    dcc.Dropdown(
                        id="recintos-eleccion",
                        options=ELECCION_OPTIONS,
                        value="gobernador",
                        clearable=False,
                        style={"minWidth": "180px", "fontSize": "0.85rem"},
                    ),
                ]),
                html.Div(className="control-group", children=[
                    html.Label("Colorear por", className="control-label"),
                    dcc.RadioItems(
                        id="recintos-color-by",
                        options=METRICA_OPTIONS,
                        value="pct_ganador",
                        inline=True,
                        inputStyle={"marginRight": "5px", "marginLeft": "14px"},
                        style={"fontSize": "0.83rem", "color": "var(--text-lo)", "marginTop": "4px"},
                    ),
                ]),
                html.Div(className="control-group", children=[
                    html.Label("Departamento", className="control-label"),
                    dcc.Dropdown(
                        id="recintos-dept-filter",
                        value="todos",
                        clearable=False,
                        style={"minWidth": "220px", "fontSize": "0.85rem"},
                    ),
                ]),
            ],
        ),
        html.Div(id="recintos-content"),
    ])


def dept_options(eleccion: str = "gobernador") -> list[dict]:
    return departamentos_con_recintos(eleccion or "gobernador")


def render_content(
    eleccion: str = "gobernador",
    color_by: str = "pct_ganador",
    dept_filter: str = "todos",
) -> html.Div:
    df = recintos_para_mapa(eleccion or "gobernador")
    if dept_filter and dept_filter != "todos":
        df = df[df["departamento_id"] == str(dept_filter)].copy()

    if df.empty:
        return html.Div(className="card", children=[empty_state("No hay recintos para esta seleccion.")])

    total_habilitados = int(df["habilitados"].sum())
    timestamp = get_recintos_timestamp()
    eleccion_label = "Gobernador" if eleccion == "gobernador" else "Alcalde"

    kpis = kpi_row([
        kpi_card("Recintos", fmt_number(len(df)), eleccion_label),
        kpi_card("Habilitados", fmt_number(total_habilitados), "en recintos visibles"),
        kpi_card("Prom. ganador", fmt_pct_raw(df["pct_ganador"].mean()), "por recinto"),
        kpi_card("Prom. blanco/nulo", fmt_pct_raw(df["invalidos_pct"].mean()), "por recinto"),
        kpi_card("Actualizacion", timestamp or "s/d", "datos locales"),
    ])

    fig = mapa_recintos(df, color_by=color_by or "pct_ganador")
    sidebar = render_sidebar(df, eleccion_label)

    return html.Div([
        kpis,
        html.Div(
            className="map-layout",
            children=[
                html.Div(
                    className="map-card",
                    children=[
                        dcc.Graph(
                            id="recintos-figure",
                            figure=fig,
                            config={
                                "displayModeBar": True,
                                "modeBarButtonsToRemove": ["select2d", "lasso2d", "toImage"],
                                "displaylogo": False,
                                "scrollZoom": True,
                            },
                            style={"height": "660px"},
                        ),
                    ],
                ),
                html.Div(sidebar, className="map-sidebar"),
            ],
        ),
        html.Div(
            "Datos por recinto de primera vuelta integrados al dashboard. "
            "El partido mostrado es el ganador del territorio de la eleccion: departamento para gobernador y municipio para alcalde.",
            className="map-note",
        ),
    ])


def render_sidebar(df, eleccion_label: str) -> html.Div:
    top = df.sort_values("habilitados", ascending=False).head(18)
    rows = []
    for _, r in top.iterrows():
        rows.append(html.Div(
            className="rank-row",
            children=[
                html.Div(className="rank-main", children=[
                    html.Div(className="rank-name-row", children=[
                        html.Span(r["recinto"], className="rank-name"),
                    ]),
                    html.Div(f"{r['municipio']} · {r['departamento']}", className="rank-sub"),
                    html.Div(
                        f"Ganador {fmt_pct_raw(r['pct_ganador'])} · Blanco/nulo {fmt_pct_raw(r['invalidos_pct'])}",
                        className="rank-sub",
                    ),
                ]),
                party_badge(r["partido"]),
                html.Span(fmt_number(r["habilitados"]), className="rank-hab"),
            ],
        ))

    return html.Div([
        section_header(
            f"Recintos · {eleccion_label}",
            "Top por habilitados",
        ),
        html.Div(rows),
    ])
