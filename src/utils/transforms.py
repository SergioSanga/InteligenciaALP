"""
Transformaciones y agregaciones sobre los datasets crudos.

Todas las funciones son puras: reciben datos, retornan DataFrames.
No tienen efectos secundarios ni acceden a disco directamente.
"""

from __future__ import annotations

import pandas as pd

from src.utils.data_loader import (
    get_departamentos,
    get_depts_con_segunda_vuelta,
    get_gobernaciones_v1,
    get_gobernaciones_v2,
    get_municipios_v1,
    get_municipios_v2,
    get_recintos_departamentos,
    get_recintos_municipios,
    get_recintos_resultados,
)


# ── Departamentos ─────────────────────────────────────────────────────────────

def ranking_departamentos() -> pd.DataFrame:
    """
    DataFrame con una fila por departamento, ordenado por habilitados desc.

    Columnas:
        id, nombre, ganador_v1, ganador_final, habilitados,
        votaron, no_votaron, participacion_pct, pct_ganador_v1, tiene_segunda_vuelta
    """
    depts  = get_departamentos()
    man_v2 = get_gobernaciones_v2()
    v2_ids = get_depts_con_segunda_vuelta()

    rows = []
    for did, info in depts.items():
        g = info.get("gobernador", {})
        habilitado = g.get("habilitados", 0)
        validos_pct = g.get("validos", 0)
        votaron = round(habilitado * validos_pct)
        no_votaron = habilitado - votaron
        winner_final = man_v2[did]["ganador"] if did in man_v2 else g.get("nombre", "—")
        rows.append({
            "id":                   did,
            "nombre":               info["nombre_departamento"],
            "ganador_v1":           g.get("nombre", "—"),
            "ganador_final":        winner_final,
            "habilitados":          habilitado,
            "votaron":              votaron,
            "no_votaron":           no_votaron,
            "participacion_pct":    round(validos_pct * 100, 1),
            "pct_ganador_v1":       round(g.get("ganador", 0) * 100, 1),
            "tiene_segunda_vuelta": did in v2_ids,
        })

    return (
        pd.DataFrame(rows)
        .sort_values("habilitados", ascending=False)
        .reset_index(drop=True)
    )


def partidos_gobernacion(dept_id: str, vuelta: str = "1") -> pd.DataFrame:
    """
    Resultados por partido para la gobernación de un departamento.

    Columnas: partido, votos, pct
    """
    man = get_gobernaciones_v1() if vuelta == "1" else get_gobernaciones_v2()
    info = man.get(dept_id, {})
    partidos = info.get("partidos", {})
    if not partidos:
        return pd.DataFrame(columns=["partido", "votos", "pct"])

    total = sum(partidos.values())
    rows = [
        {"partido": p, "votos": v, "pct": round(v / total * 100, 2)}
        for p, v in partidos.items()
    ]
    return (
        pd.DataFrame(rows)
        .sort_values("votos", ascending=False)
        .reset_index(drop=True)
    )


# ── Municipios ────────────────────────────────────────────────────────────────

def municipios_de_departamento(dept_name: str, vuelta: str = "1") -> pd.DataFrame:
    """
    Municipios de un departamento con resultados de alcalde (v1) o gobernador (v2).

    Columnas: municipio, partido, habilitados, participacion_pct, pct_ganador
    """
    src  = get_municipios_v1() if vuelta == "1" else get_municipios_v2()
    tipo = "alcalde"            if vuelta == "1" else "gobernador"

    rows = []
    for info in src.values():
        if info.get("departamento") != dept_name:
            continue
        t = info.get(tipo)
        if not t:
            continue
        rows.append({
            "municipio":       info["nombre_municipio"],
            "partido":         t.get("nombre", "—"),
            "habilitados":     t.get("habilitados", 0),
            "participacion_pct": round(t.get("validos", 0) * 100, 1),
            "pct_ganador":     round(t.get("ganador", 0) * 100, 1),
        })

    if not rows:
        return pd.DataFrame(columns=["municipio", "partido", "habilitados",
                                     "participacion_pct", "pct_ganador"])

    return (
        pd.DataFrame(rows)
        .sort_values("habilitados", ascending=False)
        .reset_index(drop=True)
    )


def todos_municipios_v1() -> pd.DataFrame:
    """
    Todos los 343 municipios con resultados de alcalde (1ª vuelta).

    Columnas: departamento, municipio, partido, habilitados, participacion_pct, pct_ganador
    """
    rows = []
    for info in get_municipios_v1().values():
        al = info.get("alcalde")
        if not al:
            continue
        rows.append({
            "departamento":    info["departamento"],
            "municipio":       info["nombre_municipio"],
            "partido":         al.get("nombre", "—"),
            "habilitados":     al.get("habilitados", 0),
            "participacion_pct": round(al.get("validos", 0) * 100, 1),
            "pct_ganador":     round(al.get("ganador", 0) * 100, 1),
        })

    return (
        pd.DataFrame(rows)
        .sort_values("habilitados", ascending=False)
        .reset_index(drop=True)
    )


def habilitados_por_partido() -> pd.DataFrame:
    """
    Habilitados totales ganados por cada partido a nivel nacional (alcaldes, v1).

    Columnas: partido, habilitados, n_municipios
    """
    df = todos_municipios_v1()
    return (
        df.groupby("partido")
        .agg(habilitados=("habilitados", "sum"), n_municipios=("municipio", "count"))
        .sort_values("habilitados", ascending=False)
        .reset_index()
    )


def participacion_por_departamento() -> pd.DataFrame:
    """
    Participación electoral en gobernaciones (1ª vuelta) por departamento.

    Columnas: nombre, participacion_pct, ganador_final
    """
    return (
        ranking_departamentos()[["nombre", "participacion_pct", "ganador_final"]]
        .sort_values("participacion_pct")
        .reset_index(drop=True)
    )


def municipios_para_mapa() -> pd.DataFrame:
    """
    DataFrame con todos los municipios enriquecidos para el mapa coroplético.
    Incluye los 343 con datos electorales y los 8 AIOC/TIOC sin datos.

    Columnas: mun_id, nombre, departamento, partido, habilitados,
              pct_ganador, participacion
    """
    from src.utils.data_loader import get_geojson
    geojson = get_geojson()
    m1      = get_municipios_v1()
    geo_ids = {str(f["id"]) for f in geojson["features"]}

    rows = []
    for mid, info in m1.items():
        geo_id = "80001" if mid == "80502" and "80001" in geo_ids else mid
        if geo_id not in geo_ids:
            continue
        al   = info.get("alcalde", {})
        code = str(mid).zfill(5)
        rows.append({
            "mun_id":        geo_id,
            "data_mun_id":   mid,
            "provincia_id":  f"{code[:1]}{code[1:3]}",
            "provincia":     f"Provincia {code[1:3]}",
            "nombre":        info.get("nombre_municipio", "Sin datos"),
            "departamento":  info.get("departamento", "—"),
            "partido":       al.get("nombre", "Sin datos"),
            "habilitados":   al.get("habilitados", 0),
            "pct_ganador":   round(al.get("ganador", 0) * 100, 1),
            "participacion": round(al.get("validos", 0) * 100, 1),
        })

    return pd.DataFrame(rows)


def mapa_filter_options(dept_filter: str = "todos", provincia_filter: str = "todos") -> dict:
    """Opciones encadenadas para departamento, provincia y municipio."""
    df = municipios_para_mapa()
    if dept_filter != "todos":
        df = df[df["departamento"] == dept_filter]

    provincias = (
        df[["provincia_id", "provincia"]]
        .drop_duplicates()
        .sort_values(["provincia_id"])
    )
    provincia_options = [{"label": "Todas las provincias", "value": "todos"}] + [
        {"label": f"{r['provincia']} ({r['provincia_id']})", "value": r["provincia_id"]}
        for _, r in provincias.iterrows()
    ]

    if provincia_filter != "todos":
        df = df[df["provincia_id"] == provincia_filter]

    municipios = (
        df[["mun_id", "nombre"]]
        .drop_duplicates()
        .sort_values("nombre")
    )
    municipio_options = [{"label": "Todos los municipios", "value": "todos"}] + [
        {"label": r["nombre"], "value": str(r["mun_id"])}
        for _, r in municipios.iterrows()
    ]

    return {
        "provincias": provincia_options,
        "municipios": municipio_options,
    }


# ── Recintos ─────────────────────────────────────────────────────────────────

def _dept_id_from_municipio(municipio_id: str) -> str:
    return str(municipio_id or "").lstrip("0")[:1]


def recintos_para_mapa(eleccion: str = "gobernador") -> pd.DataFrame:
    """
    Recintos electorales de primera vuelta con coordenadas.

    Para gobernador, el partido ganador de referencia es el ganador del
    departamento; para alcalde, el ganador del municipio.
    """
    resultados = get_recintos_resultados(eleccion)
    municipios = get_recintos_municipios()
    deptos = get_recintos_departamentos()

    rows = []
    for codigo, info in resultados.items():
        municipio_id = str(info.get("municipio", ""))
        municipio = municipios.get(municipio_id, {})
        dept_id = _dept_id_from_municipio(municipio_id)
        depto = deptos.get(dept_id, {})

        if eleccion == "alcalde":
            scope = municipio.get("alcalde", {})
            territorio = municipio.get("nombre_municipio", "Sin municipio")
        else:
            scope = depto.get("gobernador", {})
            territorio = depto.get("nombre_departamento", "Sin departamento")

        x = info.get("x")
        y = info.get("y")
        if x is None or y is None:
            continue

        validos = float(info.get("validos") or 0)
        ganador = float(info.get("ganador") or 0)
        rows.append({
            "codigo": codigo,
            "recinto": info.get("recinto", "Recinto sin nombre"),
            "municipio_id": municipio_id,
            "municipio": municipio.get("nombre_municipio", "Sin municipio"),
            "departamento_id": dept_id,
            "departamento": municipio.get("departamento") or depto.get("nombre_departamento", "Sin departamento"),
            "territorio": territorio,
            "partido": scope.get("nombre", "Sin datos"),
            "habilitados": int(float(info.get("habilitados") or 0)),
            "validos_pct": round(validos * 100, 1),
            "invalidos_pct": round((1 - validos) * 100, 1),
            "pct_ganador": round(ganador * 100, 1),
            "lon": float(x),
            "lat": float(y),
        })

    return pd.DataFrame(rows)


def departamentos_con_recintos(eleccion: str = "gobernador") -> list[dict]:
    """Opciones de departamento presentes en los datos de recintos."""
    df = recintos_para_mapa(eleccion)
    if df.empty:
        return [{"label": "Todos los departamentos", "value": "todos"}]
    opts = (
        df[["departamento_id", "departamento"]]
        .drop_duplicates()
        .sort_values("departamento")
    )
    return [{"label": "Todos los departamentos", "value": "todos"}] + [
        {"label": r["departamento"], "value": r["departamento_id"]}
        for _, r in opts.iterrows()
    ]
