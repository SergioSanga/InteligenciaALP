"""
Página: Ranking Nacional.

Muestra KPIs nacionales, ranking de las 9 gobernaciones y
top 25 municipios por habilitados.
Incluye datos de habilitados, votación y abstención.
"""

from dash import html, dcc

from src.components.figures import municipios_bars
from src.components.ui import (
    empty_state,
    kpi_card,
    kpi_row,
    ranking_row,
    section_header,
)
from src.utils.data_loader import get_depts_con_segunda_vuelta
from src.utils.transforms import (
    ranking_departamentos,
    todos_municipios_v1,
)


def layout() -> html.Div:
    df_depts = ranking_departamentos()
    df_muns  = todos_municipios_v1()
    v2_ids   = get_depts_con_segunda_vuelta()

    total_hab  = int(df_depts["habilitados"].sum())
    total_votaron = int(df_depts["votaron"].sum())
    total_no_votaron = int(df_depts["no_votaron"].sum())
    avg_part   = df_depts["participacion_pct"].mean()
    n_muns     = len(df_muns)
    n_v2       = len(v2_ids)

    kpis = kpi_row([
        kpi_card("Departamentos",   "9",                  "Bolivia"),
        kpi_card("Municipios",      str(n_muns),          "1ª vuelta · salteños"),
        kpi_card("Habilitados",     f"{total_hab:,}",     "Total nacional"),
        kpi_card("Votaron",        f"{total_votaron:,}",  "Participaron"),
        kpi_card("No votaron",      f"{total_no_votaron:,}", "Abstención"),
        kpi_card("Participación",   f"{avg_part:.1f}%",   "Promedio salteaciones"),
    ])

    # ── Ranking gobernaciones ─────────────────────────────────────────────────
    rows_depts = []
    for i, r in df_depts.iterrows():
        v2   = r["tiene_segunda_vuelta"]
        tag  = "2ª vuelta" if v2 else ""
        sub  = f"1ª vuelta: {r['ganador_v1']}" if v2 and r["ganador_v1"] != r["ganador_final"] else ""
        sub += f" | Votaron: {r['votaron']:,} | Abstuvo: {r['no_votaron']:,}"
        rows_depts.append(ranking_row(
            pos=i + 1,
            name=r["nombre"],
            party=r["ganador_final"],
            pct=r["pct_ganador_v1"],
            hab=r["habilitados"],
            sub=sub,
            tag=tag,
            tag_cls="tag-v2",
        ))

    # ── Top 25 municipios ─────────────────────────────────────────────────────
    rows_muns = []
    for i, r in df_muns.head(25).iterrows():
        rows_muns.append(ranking_row(
            pos=i + 1,
            name=r["municipio"],
            party=r["partido"],
            pct=r["pct_ganador"],
            hab=r["habilitados"],
            sub=r["departamento"],
        ))

    if not rows_muns:
        rows_muns = [empty_state()]

    return html.Div([
        kpis,
        html.Div(
            className="two-col",
            children=[
                html.Div(
                    className="card",
                    children=[
                        section_header(
                            "Gobernaciones",
                            "Resultado final · ordenado por habilitados",
                        ),
                        html.Div(rows_depts),
                    ],
                ),
                html.Div(
                    className="card",
                    children=[
                        section_header(
                            "Top 25 municipios",
                            "Elecciones de alcalde · 1ª vuelta · por habilitados",
                        ),
                        html.Div(
                            rows_muns,
                            style={"maxHeight": "680px", "overflowY": "auto"},
                        ),
                    ],
                ),
            ],
        ),
    ])