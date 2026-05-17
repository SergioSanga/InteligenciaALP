"""
Página principal: Dashboard Estratégico de Inteligencia Territorial.
"""

from dash import dcc, html

from src.components.ui import kpi_card, kpi_row, section_header
from src.utils.iprf import ranking_deptos, ranking_municipios


def layout() -> html.Div:
    df_depts = ranking_deptos()
    df_muns = ranking_municipios()
    
    total_depts = len(df_depts)
    alta_prioridad = len(df_depts[df_depts["prioridad"] == "Alta"])
    media_prioridad = len(df_depts[df_depts["prioridad"] == "Media"])
    baja_prioridad = len(df_depts[df_depts["prioridad"] == "Baja"])
    
    total_muns = len(df_muns)
    muns_alta = len(df_muns[df_muns["prioridad"] == "Alta"])
    
    total_votantes = int(df_muns["votantes"].sum())
    avg_iprf = round(df_depts["iprf"].mean(), 1)
    
    kpis = kpi_row([
        kpi_card("Departamentos", str(total_depts), "en análisis"),
        kpi_card("Alta Prioridad", str(alta_prioridad), "zonas estratégicas"),
        kpi_card("Media Prioridad", str(media_prioridad), "zonas potenciales"),
        kpi_card("Baja Prioridad", str(baja_prioridad), "zonas secundarias"),
        kpi_card("Municipios", str(total_muns), "analizados"),
        kpi_card("Votantes Total", f"{total_votantes:,}", "en territorio"),
    ])
    
    depts_rows = []
    for i, r in df_depts.iterrows():
        color_iprf = "#22C55E" if r["iprf"] >= 75 else ("#F59E0B" if r["iprf"] >= 50 else "#EF4444")
        depts_rows.append(html.Div(
            className="rank-row",
            children=[
                html.Span(f"{list(df_depts.index).index(i)+1:02d}", className="rank-pos"),
                html.Div(
                    className="rank-main",
                    children=[
                        html.Div(r["nombre"], className="rank-name"),
                        html.Div(f"Afinidad: {r['afinidad']}% · Participación: {r['participacion']}%", className="rank-sub"),
                    ],
                ),
                html.Div(
                    r["prioridad"],
                    className="badge",
                    style={
                        "background": f"rgba({255 if r['prioridad']=='Alta' else 245 if r['prioridad']=='Media' else 239},"
                                     f"{157 if r['prioridad']=='Alta' else 158 if r['prioridad']=='Media' else 68},"
                                     f"{68 if r['prioridad']=='Alta' else 11 if r['prioridad']=='Media' else 68},0.15)",
                        "color": color_iprf,
                        "border": f"1px solid {color_iprf}",
                    },
                ),
                html.Div(
                    f"{r['iprf']:.1f}",
                    className="rank-pct",
                    style={"color": color_iprf, "fontWeight": "700"},
                ),
                html.Span(f"{r['votantes']:,}", className="rank-hab"),
            ],
        ))
    
    muns_rows = []
    for i, r in df_muns.head(20).iterrows():
        color_iprf = "#22C55E" if r["iprf"] >= 75 else ("#F59E0B" if r["iprf"] >= 50 else "#EF4444")
        muns_rows.append(html.Div(
            className="rank-row",
            children=[
                html.Span(f"{list(df_muns.head(20).index).index(i)+1:02d}", className="rank-pos"),
                html.Div(
                    className="rank-main",
                    children=[
                        html.Div(r["nombre"], className="rank-name"),
                        html.Div(f"{r['departamento']} · {r['clasificacion']}", className="rank-sub"),
                    ],
                ),
                html.Div(
                    r["prioridad"],
                    className="badge",
                    style={
                        "background": f"rgba({255 if r['prioridad']=='Alta' else 245 if r['prioridad']=='Media' else 239},"
                                     f"{157 if r['prioridad']=='Alta' else 158 if r['prioridad']=='Media' else 68},"
                                     f"{68 if r['prioridad']=='Alta' else 11 if r['prioridad']=='Media' else 68},0.15)",
                        "color": color_iprf,
                        "border": f"1px solid {color_iprf}",
                    },
                ),
                html.Div(
                    f"{r['iprf']:.1f}",
                    className="rank-pct",
                    style={"color": color_iprf, "fontWeight": "700"},
                ),
                html.Span(f"{r['votantes']:,}", className="rank-hab"),
            ],
        ))
    
    return html.Div([
        kpis,
        section_header("Departamentos por IPRF", "Índice de Potencial de Recolección de Firmas"),
        html.Div(
            depts_rows,
            style={"maxHeight": "400px", "overflowY": "auto", "marginBottom": "24px"},
        ),
        section_header("Municipios Prioritarios", "Top 20 por IPRF · scroll para ver más"),
        html.Div(muns_rows, style={"maxHeight": "500px", "overflowY": "auto"}),
    ])