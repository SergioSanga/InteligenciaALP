"""
Dashboard: Potencial de Recolección de Firmas
Módulo de Inteligencia Territorial y Análisis Electoral
"""

from dash import html, dcc
from src.components.ui import kpi_card, kpi_row, section_header, ranking_row, empty_state


def calcular_recomendacion(r: dict) -> str:
    """Genera recomendación automática basada en los datos del registro."""
    parts = []
    iprf = r.get("iprf", 0)
    participacion = r.get("participacion", 0)
    densidad = r.get("densidad", 0)
    votaron = r.get("votaron", 0)

    if iprf >= 75:
        if participacion >= 80:
            parts.append("Zona óptima para recolección. Alta participación electoral y población concentrada.")
        elif densidad >= 1500:
            parts.append("Zona urbana estratégica. Alta densidad poblacional facilita instalação de mesas.")
        else:
            parts.append("Zona con alto potencial. Combinación favorable de factores territoriales.")
    elif iprf >= 50:
        if participacion >= 70:
            parts.append("Zona recomendada. Participación electoral aceptable con potencial de mobilization.")
        else:
            parts.append("Zona con potencial moderado. Requiere estrategia de mobilisation local.")
    else:
        if participacion < 60:
            parts.append("Zona de baja prioridad. Baja participación histórica. Considerar alternativas.")
        else:
            parts.append("Zona con potencial limitado. Requiere evaluation de viabilidad local.")

    return parts[0] if parts else "Zona sin datos suficientes para generar recomendación."


def layout() -> html.Div:
    from src.utils.iprf import (
        ranking_deptos, ranking_municipios, ranking_recintos,
        clasificar_prioridad, calcular_iprf
    )

    df_depts = ranking_deptos()
    df_muns = ranking_municipios()
    df_recs = ranking_recintos()

    total_hab = int(df_depts["habilitados"].sum())
    total_votaron = int(df_depts["votaron"].sum())
    alta_prioridad = len(df_depts[df_depts["prioridad"] == "Alta"])
    media_prioridad = len(df_depts[df_depts["prioridad"] == "Media"])
    baja_prioridad = len(df_depts[df_depts["prioridad"] == "Baja"])
    avg_iprf = round(df_depts["iprf"].mean(), 1)

    kpis = kpi_row([
        kpi_card("Territorios Analizados", str(len(df_depts)), "Departamentos"),
        kpi_card("Municipios", str(len(df_muns)), "En análisis"),
        kpi_card("Habilitados", f"{total_hab:,}", "Total nacional"),
        kpi_card("Votaron", f"{total_votaron:,}", "1ª vuelta"),
        kpi_card("IPRF Promedio", f"{avg_iprf:.1f}", "Índice territorial"),
        kpi_card("Zonas Alta Pri.", str(alta_prioridad), "Prioridad"),
    ])

    rows_dept = []
    for i, r in df_depts.iterrows():
        color = "#22C55E" if r["iprf"] >= 75 else ("#F59E0B" if r["iprf"] >= 50 else "#EF4444")
        row_data = {
            "iprf": r["iprf"],
            "participacion": r["participacion"],
            "densidad": r["densidad"],
            "votaron": r["votaron"],
        }
        rows_dept.append(html.Div(
            className="rank-row",
            children=[
                html.Span(f"{list(df_depts.index).index(i)+1:02d}", className="rank-pos"),
                html.Div(className="rank-main", children=[
                    html.Div(r["nombre"], className="rank-name"),
                    html.Div(f"Votaron: {r['votaron']:,} | Abstuvo: {r['no_votaron']:,} | Part: {r['participacion']}%", className="rank-sub"),
                    html.Div(calcular_recomendacion(row_data), style={"fontSize": "0.65rem", "color": "var(--accent)", "marginTop": "4px"}),
                ]),
                html.Div(r["prioridad"], className="badge", style={
                    "background": f"rgba({255 if r['prioridad']=='Alta' else 245 if r['prioridad']=='Media' else 239},{157 if r['prioridad']=='Alta' else 158 if r['prioridad']=='Media' else 68},{68 if r['prioridad']=='Alta' else 11 if r['prioridad']=='Media' else 68},0.15)",
                    "color": color,
                    "border": f"1px solid {color}",
                }),
                html.Div(f"{r['iprf']:.1f}", className="rank-pct", style={"color": color, "fontWeight": "700"}),
                html.Span(f"{r['votantes']:,}", className="rank-hab"),
            ],
        ))

    rows_mun = []
    for i, r in df_muns.iterrows():
        color = "#22C55E" if r["iprf"] >= 75 else ("#F59E0B" if r["iprf"] >= 50 else "#EF4444")
        row_data = {
            "iprf": r["iprf"],
            "participacion": r["participacion"],
            "densidad": r.get("densidad", 0),
            "votaron": r.get("votaron", 0),
        }
        rows_mun.append(html.Div(
            className="rank-row",
            children=[
                html.Span(f"{i+1:02d}", className="rank-pos"),
                html.Div(className="rank-main", children=[
                    html.Div(r["nombre"], className="rank-name"),
                    html.Div(f"{r['departamento']} · {r['clasificacion']}", className="rank-sub"),
                    html.Div(calcular_recomendacion(row_data), style={"fontSize": "0.62rem", "color": "var(--accent)", "marginTop": "2px"}),
                ]),
                html.Div(r["prioridad"], className="badge", style={
                    "background": f"rgba({255 if r['prioridad']=='Alta' else 245 if r['prioridad']=='Media' else 239},{157 if r['prioridad']=='Alta' else 158 if r['prioridad']=='Media' else 68},{68 if r['prioridad']=='Alta' else 11 if r['prioridad']=='Media' else 68},0.15)",
                    "color": color,
                    "border": f"1px solid {color}",
                }),
                html.Div(f"{r['iprf']:.1f}", className="rank-pct", style={"color": color, "fontWeight": "700"}),
                html.Span(f"{r['votantes']:,}", className="rank-hab"),
            ],
        ))

    return html.Div([
        section_header("Dashboard Estratégico", "Índice de Potencial de Recolección de Firmas (IPRF) · Análisis territorial híbrido"),
        kpis,
        html.Div(
            className="two-col",
            style={"marginBottom": "16px"},
            children=[
                html.Div(className="card", children=[
                    section_header("Departamentos por IPRF", "Ranking territorial con recomendación automática"),
                    html.Div(rows_dept, style={"maxHeight": "450px", "overflowY": "auto"}),
                ]),
                html.Div(className="card", children=[
                    section_header("Municipios Prioritarios", f"Top {len(rows_mun)} por IPRF · click para ver recomendación"),
                    html.Div(rows_mun[:25], style={"maxHeight": "450px", "overflowY": "auto"}),
                ]),
            ],
        ),
        section_header("Estadísticas de Prioridad Territorial", "Distribución de zonas por clasificación IPRF"),
        html.Div(
            className="two-col",
            children=[
                html.Div(className="card", children=[
                    section_header("Distribución por Prioridad", f"Alta: {alta_prioridad} | Media: {media_prioridad} | Baja: {baja_prioridad}"),
                    html.Div([
                        html.Div(className="stat-bar", children=[
                            html.Div("Alta Prioridad", style={"width": "30%", "color": "#22C55E", "fontWeight": "600"}),
                            html.Div(f"{alta_prioridad} deptos", style={"marginLeft": "8px", "color": "var(--text-mid)"}),
                        ]),
                        html.Div(style={"height": "8px", "background": "#22C55E", "borderRadius": "4px", "marginBottom": "16px", "opacity": "0.8"}),
                        html.Div(className="stat-bar", children=[
                            html.Div("Media Prioridad", style={"width": "30%", "color": "#F59E0B", "fontWeight": "600"}),
                            html.Div(f"{media_prioridad} deptos", style={"marginLeft": "8px", "color": "var(--text-mid)"}),
                        ]),
                        html.Div(style={"height": "8px", "background": "#F59E0B", "borderRadius": "4px", "marginBottom": "16px", "opacity": "0.8"}),
                        html.Div(className="stat-bar", children=[
                            html.Div("Baja Prioridad", style={"width": "30%", "color": "#EF4444", "fontWeight": "600"}),
                            html.Div(f"{baja_prioridad} deptos", style={"marginLeft": "8px", "color": "var(--text-mid)"}),
                        ]),
                        html.Div(style={"height": "8px", "background": "#EF4444", "borderRadius": "4px", "opacity": "0.8"}),
                    ]),
                ]),
                html.Div(className="card", children=[
                    section_header("Factores del IPRF", "Ponderación del Índice de Potencial"),
                    html.Div([
                        html.Div(["30% · Afinidad Política", "20% · Participación Electoral", "15% · Densidad Poblacional", "15% · Concentración Urbana", "10% · Accesibilidad", "10% · Potencial Movilización"], style={"color": "var(--text-mid)", "fontSize": "0.78rem"}),
                    ]),
                ]),
            ],
        ),
    ])