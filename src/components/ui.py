"""
Componentes UI reutilizables.

Cada función retorna un elemento Dash (html.Div, html.Span, etc.)
y es completamente independiente de callbacks o estado global.
"""

from __future__ import annotations

from dash import html

from src.utils.colors import badge_style, party_color
from src.utils.formatters import fmt_number, fmt_pct_raw


# ── KPI Card ──────────────────────────────────────────────────────────────────

def kpi_card(label: str, value: str, sub: str = "") -> html.Div:
    """Tarjeta de métrica clave (KPI)."""
    return html.Div(
        className="kpi-card",
        children=[
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
            html.Div(sub,   className="kpi-sub") if sub else None,
        ],
    )


def kpi_row(cards: list[html.Div]) -> html.Div:
    """Fila horizontal de KPI cards."""
    return html.Div(cards, className="kpi-row")


# ── Party Badge ───────────────────────────────────────────────────────────────

def party_badge(party: str) -> html.Span:
    """Badge coloreado con el nombre del partido."""
    return html.Span(party, className="badge", style=badge_style(party))


# ── Progress Bar ──────────────────────────────────────────────────────────────

def progress_bar(pct: float, party: str) -> html.Div:
    """Barra de progreso de 2px, coloreada por partido."""
    return html.Div(
        className="progress-track",
        children=html.Div(
            className="progress-fill",
            style={
                "width": f"{min(pct, 100):.1f}%",
                "background": party_color(party),
            },
        ),
    )


# ── Ranking Row ───────────────────────────────────────────────────────────────

def ranking_row(
    pos:     int,
    name:    str,
    party:   str,
    pct:     float,
    hab:     int,
    sub:     str = "",
    tag:     str = "",
    tag_cls: str = "tag-default",
) -> html.Div:
    """
    Fila de ranking con número, nombre, badge de partido, % ganador y habilitados.

    Args:
        pos:     Posición en el ranking.
        name:    Nombre del municipio o departamento.
        party:   Partido ganador.
        pct:     Porcentaje del ganador (0–100).
        hab:     Número de habilitados.
        sub:     Texto secundario (p.ej. nombre del departamento).
        tag:     Etiqueta opcional (p.ej. "2ª vuelta").
        tag_cls: Clase CSS para la etiqueta.
    """
    return html.Div(
        className="rank-row",
        children=[
            html.Span(f"{pos:02d}", className="rank-pos"),
            html.Div(
                className="rank-main",
                children=[
                    html.Div(
                        className="rank-name-row",
                        children=[
                            html.Span(name, className="rank-name"),
                            html.Span(tag, className=f"tag {tag_cls}") if tag else None,
                        ],
                    ),
                    html.Div(sub, className="rank-sub") if sub else None,
                    progress_bar(pct, party),
                ],
            ),
            party_badge(party),
            html.Span(fmt_pct_raw(pct), className="rank-pct"),
            html.Span(fmt_number(hab),  className="rank-hab"),
        ],
    )


# ── Section Header ────────────────────────────────────────────────────────────

def section_header(title: str, subtitle: str = "") -> html.Div:
    return html.Div([
        html.Div(title,    className="section-title"),
        html.Div(subtitle, className="section-sub") if subtitle else None,
    ])


# ── Empty State ───────────────────────────────────────────────────────────────

def empty_state(msg: str = "Sin datos para esta selección.") -> html.Div:
    return html.Div(msg, className="empty-state")