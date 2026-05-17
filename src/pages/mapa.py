"""
Pagina: Mapa Nacional interactivo.
"""
from __future__ import annotations
from dash import dcc, html
from src.components.figures import mapa_municipios
from src.components.ui import empty_state, ranking_row, section_header
from src.utils.data_loader import get_geojson
from src.utils.transforms import (
    mapa_filter_options,
    municipios_de_departamento,
    municipios_para_mapa,
)

COLOR_OPTIONS = [
    {"label": "Partido ganador",  "value": "partido"},
    {"label": "% del ganador",    "value": "pct_ganador"},
    {"label": "Participacion %",  "value": "participacion"},
]

DEPT_FILTER_OPTIONS = [{"label": "Todos los departamentos", "value": "todos"}] + [
    {"label": d, "value": d}
    for d in sorted(["Chuquisaca","La Paz","Cochabamba","Oruro","Potosí",
                     "Tarija","Santa Cruz","Beni","Pando"])
]


def layout() -> html.Div:
    return html.Div([
        html.Div(
            className="controls-row",
            children=[
                html.Div(className="control-group", children=[
                    html.Label("Colorear por", className="control-label"),
                    dcc.RadioItems(
                        id="map-color-by",
                        options=COLOR_OPTIONS,
                        value="partido",
                        inline=True,
                        inputStyle={"marginRight": "5px", "marginLeft": "14px"},
                        style={"fontSize": "0.83rem", "color": "var(--text-lo)", "marginTop": "4px"},
                    ),
                ]),
                html.Div(className="control-group", children=[
                    html.Label("Filtrar departamento", className="control-label"),
                    dcc.Dropdown(
                        id="map-dept-filter",
                        options=DEPT_FILTER_OPTIONS,
                        value="todos",
                        clearable=False,
                        style={"minWidth": "220px", "fontSize": "0.85rem"},
                    ),
                ]),
                html.Div(className="control-group", children=[
                    html.Label("Provincia", className="control-label"),
                    dcc.Dropdown(
                        id="map-prov-filter",
                        options=mapa_filter_options()["provincias"],
                        value="todos",
                        clearable=False,
                        style={"minWidth": "220px", "fontSize": "0.85rem"},
                    ),
                ]),
                html.Div(className="control-group", children=[
                    html.Label("Municipio", className="control-label"),
                    dcc.Dropdown(
                        id="map-mun-filter",
                        options=mapa_filter_options()["municipios"],
                        value="todos",
                        clearable=False,
                        style={"minWidth": "240px", "fontSize": "0.85rem"},
                    ),
                ]),
            ],
        ),
        html.Div(
            className="map-layout",
            children=[
                html.Div(
                    className="map-card",
                    children=[
                        dcc.Graph(
                            id="map-figure",
                            config={
                                "displayModeBar": True,
                                "modeBarButtonsToRemove": ["select2d","lasso2d","toImage"],
                                "displaylogo": False,
                                "scrollZoom": True,
                            },
                            style={"height": "100%", "minHeight": "350px"},
                        ),
                    ],
                ),
                html.Div(id="map-sidebar", className="map-sidebar"),
            ],
        ),
        html.Div(
            "El mapa usa los 343 municipios oficiales del dataset. Los 8 municipios AIOC/TIOC "
            "no celebraron eleccion ordinaria de alcalde y aparecen con el color Sin datos.",
            className="map-note",
        ),
    ])


def options_for_filters(dept_filter: str = "todos", prov_filter: str = "todos") -> dict:
    return mapa_filter_options(dept_filter or "todos", prov_filter or "todos")


def render_map(
    color_by: str = "partido",
    dept_filter: str = "todos",
    prov_filter: str = "todos",
    mun_filter: str = "todos",
):
    df      = municipios_para_mapa()
    geojson = get_geojson()

    if dept_filter != "todos":
        df = df[df["departamento"] == dept_filter].copy()
    if prov_filter != "todos":
        df = df[df["provincia_id"] == prov_filter].copy()
    if mun_filter != "todos":
        df = df[df["mun_id"].astype(str) == str(mun_filter)].copy()

    ids = set(df["mun_id"].astype(str))
    geojson = {
        "type": "FeatureCollection",
        "features": [f for f in geojson["features"] if str(f["id"]) in ids],
    }

    return mapa_municipios(df, geojson, color_by=color_by, selected_mun_id=mun_filter)


def render_sidebar(
    dept_filter: str = "todos",
    prov_filter: str = "todos",
    mun_filter: str = "todos",
) -> html.Div:
    df = municipios_para_mapa()
    if dept_filter != "todos":
        df = df[df["departamento"] == dept_filter]
    if prov_filter != "todos":
        df = df[df["provincia_id"] == prov_filter]
    if mun_filter != "todos":
        df = df[df["mun_id"].astype(str) == str(mun_filter)]

    titulo = "Top municipios"
    if mun_filter != "todos" and not df.empty:
        titulo = df.iloc[0]["nombre"]
    elif prov_filter != "todos":
        titulo = f"Provincia {str(prov_filter)[1:3]}"
    elif dept_filter != "todos":
        titulo = dept_filter

    subtitulo = f"{len(df)} municipios visibles - por habilitados"
    df = df.sort_values("habilitados", ascending=False).head(24)

    if df.empty:
        return html.Div([section_header(titulo, subtitulo), empty_state()])

    rows = [
        ranking_row(
            pos=i + 1,
            name=r["nombre"],
            party=r["partido"],
            pct=r["pct_ganador"],
            hab=r["habilitados"],
            sub=f"{r['departamento']} · {r['provincia']} ({r['provincia_id']})",
        )
        for i, r in df.iterrows()
    ]
    return html.Div([section_header(titulo, subtitulo), html.Div(rows)])
