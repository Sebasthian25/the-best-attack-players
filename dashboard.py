import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Best Attack Players 2025/26",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos personalizados ───────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo y tipografía */
    [data-testid="stAppViewContainer"] { background-color: #0d0d0d; }
    [data-testid="stSidebar"]          { background-color: #111111; border-right: 1px solid #222; }
    h1, h2, h3                         { font-family: 'Georgia', serif; letter-spacing: -0.5px; }

    /* Tarjetas de métrica */
    [data-testid="metric-container"] {
        background: #161616;
        border: 1px solid #2a2a2a;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"]  { color: #777 !important; font-size: 12px !important; }
    [data-testid="stMetricValue"]  { color: #f0f0f0 !important; font-size: 26px !important; }
    [data-testid="stMetricDelta"]  { color: #4caf8a !important; }

    /* Título principal */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f0f0f0;
        border-bottom: 2px solid #2a6ef5;
        padding-bottom: 0.4rem;
        margin-bottom: 1.4rem;
    }
    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1.5rem 0 0.6rem;
    }
    /* Botones del sidebar */
    .stButton > button {
        background: #1a1a1a;
        color: #ccc;
        border: 1px solid #333;
        border-radius: 8px;
        width: 100%;
    }
    .stButton > button:hover { background: #2a6ef5; color: white; border-color: #2a6ef5; }
</style>
""", unsafe_allow_html=True)

LIGA_COLORS = {
    "eng Premier League": "#e63946",
    "es La Liga":         "#f4a261",
    "de Bundesliga":      "#2a6ef5",
    "it Serie A":         "#7b2d8b",
    "fr Ligue 1":         "#2ec4b6",
}

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_attackers.csv")
    return df

df = load_data()

# ── Sidebar — filtros ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filtros")

    ligas_sel = st.multiselect(
        "Liga",
        options=sorted(df["Comp"].unique()),
        default=sorted(df["Comp"].unique()),
    )

    min_min = st.slider(
        "Minutos mínimos jugados",
        min_value=0,
        max_value=int(df["Min"].max()),
        value=900,
        step=90,
    )

    min_goles = st.slider("Mínimo de goles", 0, int(df["Gls"].max()), 0)

    st.markdown("---")
    st.markdown(
        "<p style='color:#555; font-size:11px;'>Datos: 5 grandes ligas · Temporada 2025/26</p>",
        unsafe_allow_html=True,
    )

# ── Filtrado ─────────────────────────────────────────────────────────────────
mask = (
    df["Comp"].isin(ligas_sel) &
    (df["Min"] >= min_min) &
    (df["Gls"] >= min_goles)
)
dff = df[mask].copy()

# ── Título ───────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Best Attack Players 2025/26</p>', unsafe_allow_html=True)

if dff.empty:
    st.warning("No hay jugadores con los filtros seleccionados. Ajusta los valores del sidebar.")
    st.stop()

# ── KPIs ─────────────────────────────────────────────────────────────────────
top_scorer   = dff.loc[dff["Gls"].idxmax()]
top_score    = dff.loc[dff["score"].idxmax()]
top_g90      = dff.loc[dff["goals_per_90"].idxmax()]
top_contrib  = dff.loc[dff["contribution"].idxmax()]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Jugadores filtrados", len(dff))
c2.metric("Máx goles",    f"{int(top_scorer['Gls'])}",  top_scorer["Player"])
c3.metric("Máx G/90",     f"{top_g90['goals_per_90']:.2f}", top_g90["Player"])
c4.metric("Máx score",    f"{top_score['score']:.3f}",   top_score["Player"])
c5.metric("Máx G+A",      f"{int(top_contrib['contribution'])}", top_contrib["Player"])

st.markdown("---")

# ── Fila 1: Top 10 goles/90 · Promedio por liga ───────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.markdown('<p class="section-title">Top 10 — goles por 90 min</p>', unsafe_allow_html=True)
    top10 = dff.nlargest(10, "goals_per_90")[
        ["Player", "Squad", "Comp", "Gls", "goals_per_90"]
    ].reset_index(drop=True)

    fig1 = px.bar(
        top10,
        x="goals_per_90",
        y="Player",
        orientation="h",
        color="Comp",
        color_discrete_map=LIGA_COLORS,
        hover_data={"Squad": True, "Gls": True, "Comp": False},
        text=top10["goals_per_90"].map(lambda v: f"{v:.2f}"),
        template="plotly_dark",
    )
    fig1.update_traces(textposition="outside", textfont_size=11)
    fig1.update_layout(
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=20, t=10, b=10),
        yaxis=dict(autorange="reversed", tickfont_size=12),
        xaxis_title="Goles / 90 min",
        showlegend=False,
        height=340,
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.markdown('<p class="section-title">Promedio por liga</p>', unsafe_allow_html=True)
    by_comp = (
        dff.groupby("Comp")
        .agg(avg_g90=("goals_per_90", "mean"), jugadores=("Player", "count"))
        .reset_index()
        .sort_values("avg_g90", ascending=False)
    )
    fig2 = px.bar(
        by_comp,
        x="avg_g90",
        y="Comp",
        orientation="h",
        color="Comp",
        color_discrete_map=LIGA_COLORS,
        text=by_comp["avg_g90"].map(lambda v: f"{v:.3f}"),
        template="plotly_dark",
    )
    fig2.update_traces(textposition="outside", textfont_size=11)
    fig2.update_layout(
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=20, t=10, b=10),
        yaxis=dict(autorange="reversed", tickfont_size=12, title=""),
        xaxis_title="G/90 promedio",
        showlegend=False,
        height=340,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Fila 2: Scatter tiros vs goles · Eficiencia ───────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown('<p class="section-title">Tiros vs goles</p>', unsafe_allow_html=True)
    scatter_df = dff[dff["Sh"] >= 15].copy()

    fig3 = px.scatter(
        scatter_df,
        x="Sh",
        y="Gls",
        color="Comp",
        color_discrete_map=LIGA_COLORS,
        size="score",
        size_max=22,
        hover_name="Player",
        hover_data={"Squad": True, "Sh": True, "Gls": True, "score": ":.3f", "Comp": False},
        template="plotly_dark",
    )
    # Línea de regresión manual
    m, b = np.polyfit(scatter_df["Sh"], scatter_df["Gls"], 1)
    x_range = np.linspace(scatter_df["Sh"].min(), scatter_df["Sh"].max(), 100)
    fig3.add_trace(go.Scatter(
        x=x_range, y=m * x_range + b,
        mode="lines",
        line=dict(color="#555", dash="dash", width=1),
        name="tendencia",
        showlegend=False,
    ))
    fig3.update_layout(
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=10, t=10, b=10),
        xaxis_title="Tiros totales",
        yaxis_title="Goles",
        legend=dict(
            title="Liga", bgcolor="#161616",
            bordercolor="#333", borderwidth=1,
            font=dict(size=11),
        ),
        height=360,
    )
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.markdown('<p class="section-title">Top 15 — eficiencia de gol (mín 20 tiros)</p>', unsafe_allow_html=True)
    eff_df = (
        dff[dff["Sh"] >= 20]
        .nlargest(15, "goal_efficiency")[["Player", "Squad", "Comp", "Gls", "Sh", "goal_efficiency"]]
        .reset_index(drop=True)
    )
    eff_df["eff_pct"] = (eff_df["goal_efficiency"] * 100).round(1)

    fig4 = px.bar(
        eff_df,
        x="eff_pct",
        y="Player",
        orientation="h",
        color="Comp",
        color_discrete_map=LIGA_COLORS,
        text=eff_df["eff_pct"].map(lambda v: f"{v:.1f}%"),
        hover_data={"Gls": True, "Sh": True, "Comp": False},
        template="plotly_dark",
    )
    fig4.update_traces(textposition="outside", textfont_size=11)
    fig4.update_layout(
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=30, t=10, b=10),
        yaxis=dict(autorange="reversed", tickfont_size=11, title=""),
        xaxis_title="Goles / tiro (%)",
        showlegend=False,
        height=360,
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Fila 3: Score compuesto · Contribución total ──────────────────────────────
col_e, col_f = st.columns(2)

with col_e:
    st.markdown('<p class="section-title">Score compuesto — top 20</p>', unsafe_allow_html=True)
    top20_score = dff.nlargest(20, "score")[["Player", "Squad", "Comp", "score"]].reset_index(drop=True)

    fig5 = px.bar(
        top20_score,
        x="score",
        y="Player",
        orientation="h",
        color="Comp",
        color_discrete_map=LIGA_COLORS,
        text=top20_score["score"].map(lambda v: f"{v:.3f}"),
        hover_data={"Squad": True, "Comp": True},
        template="plotly_dark",
    )
    fig5.update_traces(textposition="outside", textfont_size=10)
    fig5.update_layout(
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=30, t=10, b=10),
        yaxis=dict(autorange="reversed", tickfont_size=11, title=""),
        xaxis_title="Score (0–1)",
        showlegend=False,
        height=460,
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_f:
    st.markdown('<p class="section-title">Goles + asistencias — top 15</p>', unsafe_allow_html=True)
    top15_contrib = dff.nlargest(15, "contribution")[
        ["Player", "Squad", "Comp", "Gls", "Ast", "contribution"]
    ].reset_index(drop=True)

    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        y=top15_contrib["Player"],
        x=top15_contrib["Gls"],
        name="Goles",
        orientation="h",
        marker_color="#2a6ef5",
        text=top15_contrib["Gls"],
        textposition="inside",
    ))
    fig6.add_trace(go.Bar(
        y=top15_contrib["Player"],
        x=top15_contrib["Ast"],
        name="Asistencias",
        orientation="h",
        marker_color="#2ec4b6",
        text=top15_contrib["Ast"],
        textposition="inside",
    ))
    fig6.update_layout(
        barmode="stack",
        paper_bgcolor="#0d0d0d",
        plot_bgcolor="#111",
        margin=dict(l=0, r=10, t=10, b=10),
        yaxis=dict(autorange="reversed", tickfont_size=11, title=""),
        xaxis_title="G + A totales",
        legend=dict(
            bgcolor="#161616", bordercolor="#333",
            borderwidth=1, font=dict(size=11),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
        template="plotly_dark",
        height=460,
    )
    st.plotly_chart(fig6, use_container_width=True)

# ── Tabla detallada ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p class="section-title">Tabla completa</p>', unsafe_allow_html=True)

table_df = (
    dff[[
        "Player", "Squad", "Comp", "Pos", "Min",
        "Gls", "Ast", "contribution",
        "goals_per_90", "assists_per_90",
        "shot_accuracy", "goal_efficiency", "score",
    ]]
    .sort_values("score", ascending=False)
    .reset_index(drop=True)
)
table_df.index += 1

table_df.columns = [
    "Jugador", "Equipo", "Liga", "Pos", "Min",
    "Gls", "Ast", "G+A",
    "G/90", "A/90",
    "Precisión", "Eficiencia", "Score",
]

for col in ["G/90", "A/90", "Precisión", "Eficiencia", "Score"]:
    table_df[col] = table_df[col].round(3)

st.dataframe(
    table_df,
    use_container_width=True,
    height=420,
    column_config={
        "Score":      st.column_config.ProgressColumn("Score", min_value=0, max_value=1, format="%.3f"),
        "G/90":       st.column_config.NumberColumn("G/90",  format="%.3f"),
        "Precisión":  st.column_config.NumberColumn("Precisión", format="%.1%"),
        "Eficiencia": st.column_config.NumberColumn("Eficiencia", format="%.1%"),
    },
)

# Botón de descarga CSV
csv = table_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Descargar tabla como CSV",
    data=csv,
    file_name="top_attackers_filtered.csv",
    mime="text/csv",
)
