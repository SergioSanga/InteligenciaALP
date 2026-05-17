"""
Página: Por Departamento.

Permite seleccionar un departamento y vuelta para ver:
  - KPIs del departamento
  - Resultados de gobernación (barras por partido)
  - Ranking completo de municipios
  - Chart top 20 municipios por habilitados
"""

from dash import dcc, html

from src.components.figures import gobernacion_bars, municipios_bars
from src.components.ui import (
    empty_state,
    kpi_card,
    kpi_row,
    ranking_row,
    section_header,
)
from src.utils.data_loader import (
    get_departamentos,
    get_depts_con_segunda_vuelta,
    get_gobernaciones_v1,
    get_gobernaciones_v2,
)
from src.utils.transforms import (
    municipios_de_departamento,
    partidos_gobernacion,
    ranking_departamentos,
)


# ── Opciones de dropdown ──────────────────────────────────────────────────────

def _dept_options() -> list[dict]:
    depts = get_departamentos()
    return [
        {"label": v["nombre_departamento"], "value": k}
        for k, v in sorted(depts.items(), key=lambda x: x[1]["nombre_departamento"])
    ]


# ── Layout estático (controles + contenedor dinámico) ─────────────────────────

def layout() -> html.Div:
    """Layout inicial con controles; el contenido se actualiza vía callback."""
    return html.Div([
        # Controles
        html.Div(
            className="controls-row",
            children=[
                html.Div(
                    className="control-group",
                    children=[
                        html.Label("Departamento", className="control-label"),
                        dcc.Dropdown(
                            id="dept-select",
                            options=_dept_options(),
                            value="1",
                            clearable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    className="control-group",
                    children=[
                        html.Label("Vuelta", className="control-label"),
                        dcc.RadioItems(
                            id="vuelta-select",
                            options=[
                                {"label": "  1ª vuelta", "value": "1"},
                                {"label": "  2ª vuelta", "value": "2"},
                            ],
                            value="1",
                            inline=True,
                            className="radio-items",
                            inputStyle={"marginRight": "5px", "marginLeft": "14px"},
                        ),
                    ],
                ),
            ],
        ),
        # Contenido dinámico (rellenado por callback)
        html.Div(id="dept-content"),
    ])


# ── Función de contenido (llamada desde callback) ─────────────────────────────

def render_content(dept_id: str, vuelta: str) -> html.Div:
    """
    Renderiza el contenido completo del departamento seleccionado.
    Llamada desde el callback en app.py.
    """
    depts   = get_departamentos()
    v2_ids  = get_depts_con_segunda_vuelta()
    dept    = depts.get(dept_id, {})
    dname   = dept.get("nombre_departamento", "?")
    g       = dept.get("gobernador", {})
    tiene_v2 = dept_id in v2_ids

    # Si piden 2ª vuelta pero el dept no la tuvo, forzar a 1ª
    vuelta_efectiva = vuelta if (vuelta == "1" or tiene_v2) else "1"

    # Ganador final
    man_v2       = get_gobernaciones_v2()
    ganador_final = man_v2[dept_id]["ganador"] if tiene_v2 else g.get("nombre", "—")
    pct_v1        = round(g.get("ganador", 0) * 100, 1)
    participacion = round(g.get("validos", 0) * 100, 1)
    habilitados   = g.get("habilitados", 0)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    kpis = kpi_row([
        kpi_card("Habilitados",   f"{habilitados:,}", dname),
        kpi_card("Participación", f"{participacion:.1f}%", "votos válidos / habilitados"),
        kpi_card("Ganador 1ª V.", g.get("nombre", "—"), f"{pct_v1:.1f}% de los votos"),
        kpi_card(
            "Resultado final",
            ganador_final,
            "Ganó en 2ª vuelta" if tiene_v2 else "Resuelto en 1ª vuelta",
        ),
    ])

    # ── Gobernación bars ──────────────────────────────────────────────────────
    df_partidos  = partidos_gobernacion(dept_id, vuelta_efectiva)
    man_key      = get_gobernaciones_v1() if vuelta_efectiva == "1" else get_gobernaciones_v2()
    winner_label = man_key.get(dept_id, {}).get("ganador", "")
    fig_gob      = gobernacion_bars(df_partidos, winner=winner_label)
    vuelta_label = f"{'2ª' if vuelta_efectiva == '2' else '1ª'} vuelta"

    gob_card = html.Div(
        className="card",
        style={"marginBottom": "16px"},
        children=[
            section_header(
                f"Gobernación · {vuelta_label}",
                "Resultados por partido",
            ),
            dcc.Graph(figure=fig_gob, config={"displayModeBar": False}),
        ],
    )

    # ── Municipios ────────────────────────────────────────────────────────────
    df_muns   = municipios_de_departamento(dname, vuelta_efectiva)
    tipo_lbl  = "Alcaldes · 1ª vuelta" if vuelta_efectiva == "1" else "Gobernador por municipio · 2ª vuelta"
    fig_muns  = municipios_bars(df_muns, top=20)

    mun_rows = (
        [
            ranking_row(
                pos=i + 1,
                name=r["municipio"],
                party=r["partido"],
                pct=r["pct_ganador"],
                hab=r["habilitados"],
            )
            for i, r in df_muns.iterrows()
        ]
        if not df_muns.empty
        else [empty_state()]
    )

    bottom = html.Div(
        className="two-col",
        children=[
            html.Div(
                className="card",
                children=[
                    section_header(
                        f"Municipios · {tipo_lbl}",
                        "Ordenado por habilitados",
                    ),
                    html.Div(
                        mun_rows,
                        style={"maxHeight": "560px", "overflowY": "auto"},
                    ),
                ],
            ),
            html.Div(
                className="card",
                children=[
                    section_header(
                        "Top 20 municipios",
                        "Color = partido ganador · tamaño = habilitados",
                    ),
                    dcc.Graph(figure=fig_muns, config={"displayModeBar": False}),
                ],
            ),
        ],
    )

    return html.Div([kpis, gob_card, bottom])