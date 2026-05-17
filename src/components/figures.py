"""
Fábricas de figuras Plotly.

Cada función recibe un DataFrame (ya transformado) y retorna un go.Figure.
No acceden a datos crudos ni a estado global.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import PLOTLY_BASE
from src.utils.colors import party_color, party_colors_list


# ── Helpers internos ──────────────────────────────────────────────────────────

def _base(**overrides) -> dict:
    """Combina PLOTLY_BASE con overrides específicos de la figura."""
    layout = {**PLOTLY_BASE}
    layout.update(overrides)
    return layout


def _grid_axis() -> dict:
    return {"showgrid": True, "gridcolor": "rgba(255,255,255,0.04)", "zeroline": False}


def _no_axis() -> dict:
    return {"visible": False, "showgrid": False}


# ── Gobernación: barras horizontales ─────────────────────────────────────────

def gobernacion_bars(df: pd.DataFrame, winner: str = "") -> go.Figure:
    """
    Barras horizontales con resultados de gobernación por partido.

    Args:
        df:     DataFrame con columnas [partido, votos, pct].
        winner: Nombre del partido ganador (para destacar con shape).
    """
    if df.empty:
        return go.Figure()

    colors = party_colors_list(df["partido"].tolist())

    fig = go.Figure(go.Bar(
        x=df["pct"],
        y=df["partido"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"  {p:.1f}%" for p in df["pct"]],
        textposition="outside",
        textfont=dict(size=12, color="#64748B"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Votos: <b>%{customdata[0]:,}</b><br>"
            "Porcentaje: <b>%{x:.2f}%</b>"
            "<extra></extra>"
        ),
        customdata=df[["votos"]].values,
    ))

    # Resaltar ganador
    if winner and winner in df["partido"].values:
        idx = df["partido"].tolist().index(winner)
        c   = party_color(winner)
        # Convertir hex a rgba para compatibilidad con Plotly
        r_val = int(c[1:3], 16)
        g_val = int(c[3:5], 16)
        b_val = int(c[5:7], 16)
        fig.add_shape(
            type="rect", xref="paper", yref="y",
            x0=0, x1=1, y0=idx - 0.45, y1=idx + 0.45,
            fillcolor=f"rgba({r_val},{g_val},{b_val},0.1)",
            line=dict(color=f"rgba({r_val},{g_val},{b_val},0.35)", width=1),
            layer="below",
        )

    fig.update_layout(
        **_base(height=max(160, len(df) * 44 + 50)),
        xaxis=_no_axis(),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=13, color="#E2E8F0"),
            tickcolor="rgba(0,0,0,0)",
        ),
    )
    return fig


# ── Municipios: barras horizontales ──────────────────────────────────────────

def municipios_bars(df: pd.DataFrame, top: int = 20) -> go.Figure:
    """
    Barras horizontales de municipios ordenados por habilitados.

    Args:
        df:  DataFrame con columnas [municipio, partido, habilitados, pct_ganador].
        top: Número máximo de municipios a mostrar.
    """
    df = df.head(top)
    if df.empty:
        return go.Figure()

    colors = party_colors_list(df["partido"].tolist())

    fig = go.Figure(go.Bar(
        x=df["habilitados"],
        y=df["municipio"],
        orientation="h",
        marker=dict(color=colors, opacity=0.85, line=dict(width=0)),
        text=df["partido"],
        textposition="outside",
        textfont=dict(size=10, color="#64748B"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Habilitados: <b>%{x:,}</b><br>"
            "Ganador: <b>%{text}</b><br>"
            "% ganador: <b>%{customdata:.1f}%</b>"
            "<extra></extra>"
        ),
        customdata=df["pct_ganador"],
    ))

    fig.update_layout(
        **_base(height=max(280, len(df) * 32 + 60)),
        xaxis={**_grid_axis(), "tickformat": ",", "tickfont": dict(size=10, color="#475569")},
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#E2E8F0")),
    )
    return fig


# ── Análisis: partidos por habilitados ────────────────────────────────────────

def partidos_habilitados_bars(df: pd.DataFrame, top: int = 10) -> go.Figure:
    """
    Barras horizontales de habilitados ganados por partido a nivel nacional.

    Args:
        df: DataFrame con columnas [partido, habilitados, n_municipios].
    """
    df = df.head(top)
    if df.empty:
        return go.Figure()

    colors = party_colors_list(df["partido"].tolist())

    fig = go.Figure(go.Bar(
        x=df["habilitados"],
        y=df["partido"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"  {v:,.0f}" for v in df["habilitados"]],
        textposition="outside",
        textfont=dict(size=11, color="#64748B"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Habilitados ganados: <b>%{x:,}</b><br>"
            "Municipios: <b>%{customdata}</b>"
            "<extra></extra>"
        ),
        customdata=df["n_municipios"],
    ))

    fig.update_layout(
        **_base(height=360),
        xaxis={**_grid_axis(), "tickformat": ",", "tickfont": dict(size=10, color="#475569")},
        yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#E2E8F0")),
    )
    return fig


# ── Análisis: participación por departamento ──────────────────────────────────

def participacion_bars(df: pd.DataFrame) -> go.Figure:
    """
    Barras de participación electoral por departamento.

    Args:
        df: DataFrame con columnas [nombre, participacion_pct, ganador_final].
    """
    if df.empty:
        return go.Figure()

    colors = party_colors_list(df["ganador_final"].tolist())

    fig = go.Figure(go.Bar(
        x=df["participacion_pct"],
        y=df["nombre"],
        orientation="h",
        marker=dict(color=colors, opacity=0.8, line=dict(width=0)),
        text=[f"  {v:.1f}%" for v in df["participacion_pct"]],
        textposition="outside",
        textfont=dict(size=12, color="#64748B"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Participación: <b>%{x:.1f}%</b><br>"
            "Ganador: <b>%{customdata}</b>"
            "<extra></extra>"
        ),
        customdata=df["ganador_final"],
    ))

    fig.update_layout(
        **_base(height=300, margin=dict(t=12, b=12, l=8, r=65)),
        xaxis=_no_axis(),
        yaxis=dict(tickfont=dict(size=12, color="#E2E8F0")),
    )
    return fig


# ── Análisis: Treemap nacional ────────────────────────────────────────────────

def treemap_nacional(df: pd.DataFrame) -> go.Figure:
    """
    Treemap jerárquico Bolivia → Departamento → Municipio.

    Args:
        df: DataFrame con columnas [departamento, municipio, partido,
                                    habilitados, participacion_pct, pct_ganador].
    """
    if df.empty:
        return go.Figure()

    from config import PARTY_COLORS, FALLBACK_COLOR

    color_map = {p: PARTY_COLORS.get(p, FALLBACK_COLOR) for p in df["partido"].unique()}

    fig = px.treemap(
        df,
        path=[px.Constant("Bolivia"), "departamento", "municipio"],
        values="habilitados",
        color="partido",
        color_discrete_map=color_map,
        custom_data=["partido", "habilitados", "pct_ganador", "participacion_pct"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Ganador: <b>%{customdata[0]}</b><br>"
            "Habilitados: <b>%{customdata[1]:,}</b><br>"
            "% ganador: <b>%{customdata[2]:.1f}%</b><br>"
            "Participación: <b>%{customdata[3]:.1f}%</b>"
            "<extra></extra>"
        ),
        textfont=dict(size=11, family="Inter, sans-serif"),
        marker_line_width=0.5,
        marker_line_color="rgba(0,0,0,0.3)",
    )
    fig.update_layout(
        **_base(height=560, margin=dict(t=8, l=0, r=0, b=0)),
    )
    return fig


# ── Análisis: Scatter participación vs % ganador ──────────────────────────────

def scatter_participacion(df: pd.DataFrame) -> go.Figure:
    """
    Scatter de participación vs % del ganador por municipio.

    Args:
        df: DataFrame con columnas [municipio, departamento, partido,
                                    habilitados, participacion_pct, pct_ganador].
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    for partido, grp in df.groupby("partido"):
        fig.add_trace(go.Scatter(
            x=grp["participacion_pct"],
            y=grp["pct_ganador"],
            mode="markers",
            name=partido,
            marker=dict(
                color=party_color(partido),
                size=6,
                opacity=0.72,
                line=dict(width=0.5, color="rgba(0,0,0,0.3)"),
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b> · %{customdata[1]}<br>"
                "Participación: <b>%{x:.1f}%</b><br>"
                "% ganador: <b>%{y:.1f}%</b><br>"
                "Habilitados: <b>%{customdata[2]:,}</b>"
                "<extra></extra>"
            ),
            customdata=grp[["municipio", "departamento", "habilitados"]].values,
            showlegend=True,
        ))

    layout = _base(height=420, margin=dict(t=12, b=50, l=55, r=160))
    layout["legend"] = dict(orientation="v", x=1.02, y=1,
                            bgcolor="rgba(0,0,0,0)", font=dict(size=10))
    fig.update_layout(
        **layout,
        xaxis={
            **_grid_axis(),
            "title": dict(text="Participación (%)", font=dict(size=11, color="#64748B")),
        },
        yaxis={
            **_grid_axis(),
            "title": dict(text="% del ganador", font=dict(size=11, color="#64748B")),
        },
    )
    return fig


# ── Mapa coroplético nacional ─────────────────────────────────────────────────

def mapa_municipios(
    df: pd.DataFrame,
    geojson: dict,
    color_by: str = "partido",
    selected_mun_id: str = "todos",
) -> go.Figure:
    """
    Mapa coroplético interactivo de Bolivia coloreado por partido ganador.

    Args:
        df:       DataFrame con columnas [mun_id, nombre, departamento, partido,
                                          habilitados, pct_ganador, participacion].
        geojson:  GeoJSON con geometrías de municipios (feature id = mun_id).
        color_by: Campo por el que colorear ('partido', 'pct_ganador', 'participacion').
        selected_mun_id: Municipio a resaltar con borde blanco.
    """
    from config import PARTY_COLORS, FALLBACK_COLOR

    if df.empty:
        return go.Figure()

    if color_by == "partido":
        # Un trace por partido para leyenda con colores correctos
        fig = go.Figure()

        partidos_presentes = df["partido"].unique()
        for partido in sorted(partidos_presentes):
            mask   = df["partido"] == partido
            subset = df[mask]
            color  = PARTY_COLORS.get(partido, FALLBACK_COLOR)

            # Filtrar geojson features de este partido
            ids_partido = set(subset["mun_id"].astype(str).tolist())
            geo_subset  = {
                "type": "FeatureCollection",
                "features": [
                    f for f in geojson["features"]
                    if str(f["id"]) in ids_partido
                ],
            }

            fig.add_trace(go.Choroplethmapbox(
                geojson=geo_subset,
                locations=subset["mun_id"].astype(str),
                z=[1] * len(subset),
                colorscale=[[0, color], [1, color]],
                showscale=False,
                marker_opacity=0.85,
                marker_line_width=0.4,
                marker_line_color="rgba(0,0,0,0.35)",
                name=partido,
                text=subset["nombre"],
                customdata=subset[["departamento", "habilitados", "pct_ganador", "participacion"]].values,
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "<span style='color:#94A3B8'>Depto: </span>%{customdata[0]}<br>"
                    "<span style='color:#94A3B8'>Ganador: </span><b>" + partido + "</b><br>"
                    "<span style='color:#94A3B8'>% ganador: </span><b>%{customdata[2]:.1f}%</b><br>"
                    "<span style='color:#94A3B8'>Habilitados: </span><b>%{customdata[1]:,}</b><br>"
                    "<span style='color:#94A3B8'>Participación: </span><b>%{customdata[3]:.1f}%</b>"
                    "<extra></extra>"
                ),
                showlegend=True,
            ))

    elif color_by in ("pct_ganador", "participacion"):
        label = "% Ganador" if color_by == "pct_ganador" else "Participación %"
        fig = go.Figure(go.Choroplethmapbox(
            geojson=geojson,
            locations=df["mun_id"].astype(str),
            z=df[color_by],
            colorscale="Blues",
            showscale=True,
            colorbar=dict(
                title=dict(text=label, font=dict(size=11, color="#94A3B8")),
                tickfont=dict(size=10, color="#94A3B8"),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(0,0,0,0)",
            ),
            marker_opacity=0.85,
            marker_line_width=0.4,
            marker_line_color="rgba(0,0,0,0.3)",
            text=df["nombre"],
            customdata=df[["departamento", "partido", "habilitados", "pct_ganador", "participacion"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "<span style='color:#94A3B8'>Depto: </span>%{customdata[0]}<br>"
                "<span style='color:#94A3B8'>Ganador: </span><b>%{customdata[1]}</b><br>"
                "<span style='color:#94A3B8'>% ganador: </span><b>%{customdata[3]:.1f}%</b><br>"
                "<span style='color:#94A3B8'>Habilitados: </span><b>%{customdata[2]:,}</b><br>"
                "<span style='color:#94A3B8'>Participación: </span><b>%{customdata[4]:.1f}%</b>"
                "<extra></extra>"
            ),
            showlegend=False,
        ))
    else:
        return go.Figure()

    if selected_mun_id and selected_mun_id != "todos":
        selected_subset = df[df["mun_id"].astype(str) == str(selected_mun_id)]
        if not selected_subset.empty:
            selected_ids = set(selected_subset["mun_id"].astype(str))
            selected_geojson = {
                "type": "FeatureCollection",
                "features": [
                    f for f in geojson["features"]
                    if str(f["id"]) in selected_ids
                ],
            }
            fig.add_trace(go.Choroplethmapbox(
                geojson=selected_geojson,
                locations=selected_subset["mun_id"].astype(str),
                z=[1] * len(selected_subset),
                colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
                showscale=False,
                marker_opacity=0.01,
                marker_line_width=3,
                marker_line_color="#FFFFFF",
                name="Municipio seleccionado",
                hoverinfo="skip",
                showlegend=False,
            ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-16.5, lon=-64.5),
            zoom=4.6,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#CBD5E1", size=11),
        margin=dict(t=0, b=0, l=0, r=0),
        height=620,
        autosize=True,
        legend=dict(
            bgcolor="#0D1B2E",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(size=10, color="#CBD5E1"),
            title=dict(text="Partido ganador", font=dict(size=11, color="#64748B")),
            orientation="v",
            x=1.01, y=1,
            xanchor="left",
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            font=dict(color="#F1F5F9", size=12, family="Inter, sans-serif"),
        ),
        uirevision="bolivia-map",
    )
    return fig


# ── Mapa de recintos ─────────────────────────────────────────────────────────

def mapa_recintos(df: pd.DataFrame, color_by: str = "pct_ganador") -> go.Figure:
    """
    Mapa de puntos por recinto electoral.

    Args:
        df: DataFrame con columnas [recinto, municipio, departamento, partido,
            habilitados, pct_ganador, invalidos_pct, validos_pct, lon, lat].
        color_by: 'partido', 'pct_ganador' o 'invalidos_pct'.
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    custom_cols = [
        "municipio",
        "departamento",
        "partido",
        "habilitados",
        "pct_ganador",
        "validos_pct",
        "invalidos_pct",
        "codigo",
    ]

    if color_by == "partido":
        for partido, grp in df.groupby("partido", dropna=False):
            fig.add_trace(go.Scattermapbox(
                lon=grp["lon"],
                lat=grp["lat"],
                mode="markers",
                name=str(partido),
                text=grp["recinto"],
                customdata=grp[custom_cols].values,
                marker=dict(
                    size=(grp["habilitados"].clip(lower=50) ** 0.35) + 4,
                    color=party_color(str(partido)),
                    opacity=0.78,
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "<span style='color:#94A3B8'>Municipio: </span>%{customdata[0]}<br>"
                    "<span style='color:#94A3B8'>Depto: </span>%{customdata[1]}<br>"
                    "<span style='color:#94A3B8'>Ganador del territorio: </span><b>%{customdata[2]}</b><br>"
                    "<span style='color:#94A3B8'>% ganador en recinto: </span><b>%{customdata[4]:.1f}%</b><br>"
                    "<span style='color:#94A3B8'>Votos validos: </span><b>%{customdata[5]:.1f}%</b><br>"
                    "<span style='color:#94A3B8'>Blanco/nulo: </span><b>%{customdata[6]:.1f}%</b><br>"
                    "<span style='color:#94A3B8'>Habilitados: </span><b>%{customdata[3]:,}</b><br>"
                    "<span style='color:#94A3B8'>Codigo: </span>%{customdata[7]}"
                    "<extra></extra>"
                ),
            ))
    else:
        color_title = "% ganador" if color_by == "pct_ganador" else "Blanco/nulo %"
        colorscale = "YlOrRd" if color_by == "pct_ganador" else "Blues"
        fig.add_trace(go.Scattermapbox(
            lon=df["lon"],
            lat=df["lat"],
            mode="markers",
            text=df["recinto"],
            customdata=df[custom_cols].values,
            marker=dict(
                size=(df["habilitados"].clip(lower=50) ** 0.35) + 4,
                color=df[color_by],
                colorscale=colorscale,
                cmin=float(df[color_by].min()),
                cmax=float(df[color_by].max()),
                opacity=0.78,
                colorbar=dict(
                    title=dict(text=color_title, font=dict(size=11, color="#94A3B8")),
                    tickfont=dict(size=10, color="#94A3B8"),
                    bgcolor="rgba(0,0,0,0)",
                    bordercolor="rgba(0,0,0,0)",
                ),
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "<span style='color:#94A3B8'>Municipio: </span>%{customdata[0]}<br>"
                "<span style='color:#94A3B8'>Depto: </span>%{customdata[1]}<br>"
                "<span style='color:#94A3B8'>Ganador del territorio: </span><b>%{customdata[2]}</b><br>"
                "<span style='color:#94A3B8'>% ganador en recinto: </span><b>%{customdata[4]:.1f}%</b><br>"
                "<span style='color:#94A3B8'>Votos validos: </span><b>%{customdata[5]:.1f}%</b><br>"
                "<span style='color:#94A3B8'>Blanco/nulo: </span><b>%{customdata[6]:.1f}%</b><br>"
                "<span style='color:#94A3B8'>Habilitados: </span><b>%{customdata[3]:,}</b><br>"
                "<span style='color:#94A3B8'>Codigo: </span>%{customdata[7]}"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    center = dict(lat=float(df["lat"].mean()), lon=float(df["lon"].mean()))
    zoom = 4.8 if df["departamento_id"].nunique() > 1 else 6.7
    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=center, zoom=zoom),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", color="#CBD5E1", size=11),
        margin=dict(t=0, b=0, l=0, r=0),
        height=640,
        autosize=True,
        legend=dict(
            bgcolor="#0D1B2E",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(size=10, color="#CBD5E1"),
            title=dict(text="Ganador del territorio", font=dict(size=11, color="#64748B")),
            orientation="v",
            x=1.01, y=1,
            xanchor="left",
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#334155",
            font=dict(color="#F1F5F9", size=12, family="Inter, sans-serif"),
        ),
        uirevision="bolivia-recintos",
    )
    return fig
