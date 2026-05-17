# Bolivia · Elecciones Subnacionales 2026

Dashboard interactivo que presenta los resultados de las elecciones subnacionales de Bolivia (Gobernaciones y Alcaldías) para el período 2026, tanto en primera como segunda vuelta.

---

## ¿Qué hace este proyecto?

Permite visualizar, analizar y explorar los resultados electorales de Bolivia de forma interactiva:

| Pestaña | Descripción |
|---------|-------------|
| **Ranking nacional** | KPIs nacionales (9 departamentos, 343 municipios) + ranking de gobernaciones por ganadores + top 25 municipios por habilitados |
| **Por departamento** | Selecciona un departamento y vuelta (1ª/2ª) para ver: resultados de gobernación por partido, ranking completo de municipios, gráficos interactivos |
| **Mapa interactivo** | Mapa coroplético de Bolivia coloreado por partido ganador, % del ganador o participación. Filtra por departamento, provincia y municipio |
| **Recintos** | Mapa de puntos con recintos electorales. Muestra datos de Gobernador o Alcalde con métricas por recinto |
| **Análisis** | Gráficos exploratorios: habilitados ganados por partido, participación por departamento, treemap nacional Bolivia→Depto→Municipio, scatter participación vs % ganador |

---

## Características principales

- **Temas**: Oscuro (default) y claro - toggle en navbar
- **Responsive**: Funciona en desktop, tablet y móvil
- **Interactividad**: Hover en gráficos, filtros dinámicos, tooltips
- **Mapas**: Mapbox con GeoJSON de municipios y recintos electorales
- **Filtros**: Por departamento, provincia, municipio, tipo de elección
- **Primera y Segunda vuelta**: Datos de ambas vueltas disponibles

---

## Instalación

```bash
# 1. Clonar o entrar al directorio
cd dashboardALP

# 2. Crear entorno virtual (recomendado)
python3 -m venv .venv

# 3. Activar entorno
source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar

```bash
python app.py
```

Abre tu navegador en: **http://localhost:8050**

---

## Requisitos

- Python 3.10+
- dash >= 2.14.0
- plotly >= 5.18.0
- pandas >= 2.0.0
- geopandas >= 0.14.0
- topojson >= 1.8

---

## Estructura del proyecto

```
dashboardALP/
├── app.py                 # App principal Dash + callbacks
├── config.py              # Config, colores de partidos, constantes
├── requirements.txt       # Dependencias
├── README.md              # Este archivo
├── data/
│   ├── departamentos.json
│   ├── gobernaciones_primera_vuelta.json
│   ├── gobernaciones_segunda_vuelta.json
│   ├── municipios_primera_vuelta.json
│   ├── municipios_segunda_vuelta.json
│   ├── municipios.geojson        # GeoJSON para mapa coroplético
│   ├── municipios_2026.gpkg
│   └── recintos/                 # Datos de recintos electorales
│       └── primera_vuelta/
├── src/
│   ├── pages/
│   │   ├── ranking.py       # Ranking nacional
│   │   ├── departamento.py  # Por departamento
│   │   ├── mapa.py          # Mapa interactivo
│   │   ├── recintos.py      # Recintos electorales
│   │   └── analisis.py      # Análisis y gráficos
│   ├── components/
│   │   ├── figures.py        # Gráficos Plotly
│   │   └── ui.py             # Componentes UI reutilizables
│   ├── utils/
│   │   ├── data_loader.py    # Carga de datos JSON
│   │   ├── transforms.py     # Transformaciones DataFrames
│   │   ├── colors.py         # Colores por partido
│   │   └── formatters.py    # Formateo de números/porcentajes
│   └── assets/
│       └── styles.css        # CSS con tema claro/oscuro
```

---

## Conceptos clave

### Gobernaciones
Elección de gobernador por departamento. Algunas gobernaciones fueron a segunda vuelta (ballottage).

### Alcaldías
Elección de alcalde por municipio. Primera vuelta únicamente en el dataset actual.

### Segunda vuelta
Departamentos donde ningún candidato obtuvo >50% en primera vuelta. Se realizó una segunda vuelta.

### Recintos electorales
Centros de votación con datos granulares: votos por partido, porcentaje de ganador, blancos/nulos por recinto.

### Partidos políticos
Colores asignados a cada partido según la configuración en `config.py`.

---

## Autor

**Sergio Armando Sanga Martinez**

---

## Notas técnicas

- **Framework**: Dash ( Plotly ) - framework Python para apps web interactivas
- **Mapas**: Plotly Mapbox con tiles de Carto Dark Matter
- **Tema**: CSS custom properties para switch entre tema oscuro y claro
- **Responsive**:
  - Mobile: <768px
  - Tablet: 768px - 1100px
  - Desktop: >1100px
- **No requiere base de datos**: Los datos están en archivos JSON estáticos