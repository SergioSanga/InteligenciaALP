"""
Bolivia · Elecciones Subnacionales 2026
========================================
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

import dash
from dash import Dash, Input, Output, html

from src.pages import analisis, departamento, mapa, ranking, recintos

app = Dash(
    __name__,
    title="Bolivia · Subnacionales 2026",
    assets_folder=str(ROOT / "src" / "assets"),
    suppress_callback_exceptions=True,
)

server = app.server

app.layout = html.Div(
    id="root",
    children=[
        html.Nav(
            className="navbar",
            children=[
                html.Div(
                    className="nav-brand",
                    children=[
                        html.Div("🗳", className="nav-logo"),
                        html.Div([
                            html.Div("Bolivia · Elecciones Subnacionales 2026",
                                     className="nav-title"),
                            html.Div("Resultados por departamento y municipio · 1ª y 2ª vuelta",
                                     className="nav-sub"),
                        ]),
                    ],
                ),
                html.Div(
                    className="nav-author",
                    children=[
                        html.Div("Hecho por", className="author-label"),
                        html.Div("Sergio Armando Sanga Martinez", className="author-name"),
                    ],
                ),
                html.Button("☀ Claro", id="theme-btn", n_clicks=0, className="theme-btn"),
            ],
        ),
        html.Div(
            className="body-wrap",
            children=[
                html.Div(
                    className="tabs-row",
                    children=[
                        html.Button("Ranking nacional", id="tab-ranking",  n_clicks=0, className="tab tab-active"),
                        html.Button("Por departamento", id="tab-dept",     n_clicks=0, className="tab"),
                        html.Button("Mapa interactivo", id="tab-mapa",     n_clicks=0, className="tab"),
                        html.Button("Recintos",        id="tab-recintos", n_clicks=0, className="tab"),
                        html.Button("Análisis",         id="tab-analisis", n_clicks=0, className="tab"),
                    ],
                ),
                html.Div(id="page-content"),
            ],
        ),
    ],
)


@app.callback(
    Output("tab-ranking",  "className"),
    Output("tab-dept",     "className"),
    Output("tab-mapa",     "className"),
    Output("tab-recintos", "className"),
    Output("tab-analisis", "className"),
    Output("page-content", "children"),
    Input("tab-ranking",   "n_clicks"),
    Input("tab-dept",      "n_clicks"),
    Input("tab-mapa",      "n_clicks"),
    Input("tab-recintos",  "n_clicks"),
    Input("tab-analisis",  "n_clicks"),
    prevent_initial_call=False,
)
def switch_tab(n_ranking, n_dept, n_mapa, n_recintos, n_analisis):
    ctx     = dash.callback_context
    trigger = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "tab-ranking"
    b, a    = "tab", "tab tab-active"

    if trigger == "tab-dept":     return b, a, b, b, b, departamento.layout()
    if trigger == "tab-mapa":     return b, b, a, b, b, mapa.layout()
    if trigger == "tab-recintos": return b, b, b, a, b, recintos.layout()
    if trigger == "tab-analisis": return b, b, b, b, a, analisis.layout()
    return a, b, b, b, b, ranking.layout()


@app.callback(
    Output("dept-content", "children"),
    Input("dept-select",   "value"),
    Input("vuelta-select", "value"),
    prevent_initial_call=False,
)
def update_dept_content(dept_id, vuelta):
    return departamento.render_content(dept_id or "1", vuelta or "1")


@app.callback(
    Output("map-figure",     "figure"),
    Input("map-color-by",    "value"),
    Input("map-dept-filter", "value"),
    Input("map-prov-filter", "value"),
    Input("map-mun-filter",  "value"),
    prevent_initial_call=False,
)
def update_map_figure(color_by, dept_filter, prov_filter, mun_filter):
    return mapa.render_map(
        color_by or "partido",
        dept_filter or "todos",
        prov_filter or "todos",
        mun_filter or "todos",
    )


@app.callback(
    Output("map-sidebar",    "children"),
    Input("map-dept-filter", "value"),
    Input("map-prov-filter", "value"),
    Input("map-mun-filter",  "value"),
    prevent_initial_call=False,
)
def update_map_sidebar(dept_filter, prov_filter, mun_filter):
    return mapa.render_sidebar(
        dept_filter or "todos",
        prov_filter or "todos",
        mun_filter or "todos",
    )


@app.callback(
    Output("map-prov-filter", "options"),
    Output("map-prov-filter", "value"),
    Input("map-dept-filter",  "value"),
    prevent_initial_call=False,
)
def update_map_province_options(dept_filter):
    options = mapa.options_for_filters(dept_filter or "todos")["provincias"]
    return options, "todos"


@app.callback(
    Output("map-mun-filter",  "options"),
    Output("map-mun-filter",  "value"),
    Input("map-dept-filter",  "value"),
    Input("map-prov-filter",  "value"),
    prevent_initial_call=False,
)
def update_map_municipio_options(dept_filter, prov_filter):
    options = mapa.options_for_filters(
        dept_filter or "todos",
        prov_filter or "todos",
    )["municipios"]
    return options, "todos"


@app.callback(
    Output("recintos-dept-filter", "options"),
    Output("recintos-dept-filter", "value"),
    Input("recintos-eleccion", "value"),
    prevent_initial_call=False,
)
def update_recintos_dept_options(eleccion):
    return recintos.dept_options(eleccion or "gobernador"), "todos"


@app.callback(
    Output("recintos-content", "children"),
    Input("recintos-eleccion", "value"),
    Input("recintos-color-by", "value"),
    Input("recintos-dept-filter", "value"),
    prevent_initial_call=False,
)
def update_recintos_content(eleccion, color_by, dept_filter):
    return recintos.render_content(
        eleccion or "gobernador",
        color_by or "pct_ganador",
        dept_filter or "todos",
    )


app.clientside_callback(
    """
    function(n) {
        const root = document.getElementById('root');
        if (n % 2 === 1) { root.classList.add('light'); return '🌙 Oscuro'; }
        root.classList.remove('light');
        return '☀ Claro';
    }
    """,
    Output("theme-btn", "children"),
    Input("theme-btn",  "n_clicks"),
)


if __name__ == "__main__":
    from config import APP_DEBUG, APP_HOST, APP_PORT
    print(f"""
  ╔══════════════════════════════════════════════╗
  ║   Bolivia · Subnacionales 2026               ║
  ║   http://localhost:{APP_PORT}                        ║
  ╚══════════════════════════════════════════════╝
    """)
    app.run(debug=APP_DEBUG, host=APP_HOST, port=APP_PORT)
