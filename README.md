# Best Attack Players 2025/26

Análisis de rendimiento ofensivo de jugadores de las 5 grandes ligas europeas (temporada 2025/26) usando Python, SQL y PostgreSQL. Incluye pipeline de datos completo y dashboard interactivo.

---

## Demo

![Dashboard preview](assets/dashboard_preview.png)

---

## Estructura del proyecto

```
the-best-attack-players/
├── data/
│   ├── players_data_light-2025_2026.csv   # datos crudos
│   └── clean_attackers.csv                # datos procesados
├── src/
│   ├── transform.py                       # limpieza y cálculo de métricas
│   └── load.py                            # carga a PostgreSQL
├── sql/
│   ├── schema.sql                         # definición de tabla
│   └── queries.sql                        # análisis en SQL
├── dashboard.py                           # dashboard interactivo (Streamlit)
├── iniciar_dashboard.bat                  # acceso rápido en Windows
├── requirements.txt
└── README.md
```

---

## Pipeline

```
CSV crudo → transform.py → clean_attackers.csv → load.py → PostgreSQL → queries.sql
                                                         ↘
                                                      dashboard.py (Streamlit)
```

1. **Extracción** — datos de FBref con estadísticas de delanteros de Premier League, La Liga, Serie A, Bundesliga y Ligue 1
2. **Transformación** — filtrado de jugadores ofensivos, limpieza de nulos, cálculo de métricas
3. **Carga** — inserción en PostgreSQL con `psycopg2`
4. **Análisis** — queries SQL para rankings y comparativas por liga
5. **Visualización** — dashboard con Streamlit y Plotly

---

## Métricas calculadas

| Métrica | Fórmula |
|---|---|
| `goals_per_90` | `(goles / minutos) × 90` |
| `assists_per_90` | `(asistencias / minutos) × 90` |
| `shot_accuracy` | `tiros al arco / tiros totales` |
| `goal_efficiency` | `goles / tiros totales` |
| `contribution` | `goles + asistencias` |
| `score` | `G/90 × 0.4 + A/90 × 0.2 + eficiencia × 0.2 + tiros/90 × 0.2` (normalizado 0–1) |

---

## Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/the-best-attack-players.git
cd the-best-attack-players
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Correr el dashboard (sin PostgreSQL)

```bash
streamlit run dashboard.py
```

Abre `http://localhost:8501` en tu navegador.

### 4. Cargar a PostgreSQL (opcional)

```bash
# Crear la tabla
psql -d football_analysis -f sql/schema.sql

# Cargar datos
python src/load.py
```

---

## Tecnologías

- **Python** — pandas, numpy
- **Streamlit + Plotly** — dashboard interactivo
- **PostgreSQL + psycopg2** — base de datos
- **SQL** — análisis y rankings

---

## Hallazgos principales

- Harry Kane lidera en goles/90 min (1.38) entre jugadores con más de 900 minutos
- La Bundesliga tiene el mayor promedio de goles/90 entre las 5 ligas (0.30)
- Erling Haaland y Kylian Mbappé dominan en volumen total (116 y 132 tiros respectivamente)

---

## Autor

Proyecto de análisis de datos deportivos — temporada 2025/26.
