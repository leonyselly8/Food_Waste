import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Food Analytics Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #080b14;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(108,99,255,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(72,207,173,0.06) 0%, transparent 50%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1020 0%, #080b14 100%) !important;
    border-right: 1px solid rgba(108,99,255,0.15) !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6c63ff, #48cfad, #ff6b6b);
}

/* ── Top accent bar ── */
.stApp > header {
    background: transparent !important;
}

/* ── Metric cards ── */
.metric-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6c63ff, #48cfad);
    opacity: 0.8;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 100px; height: 100px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(108,99,255,0.1) 0%, transparent 70%);
}
.metric-card:hover {
    border-color: rgba(108,99,255,0.45);
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(108,99,255,0.15);
}
.metric-icon {
    font-size: 1.6rem;
    margin-bottom: 8px;
    display: block;
}
.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa 0%, #48cfad 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.metric-label {
    font-size: 0.7rem;
    color: #6b7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}
.metric-sub {
    font-size: 0.75rem;
    color: #48cfad;
    margin-top: 8px;
    font-weight: 500;
}
.metric-badge {
    display: inline-block;
    background: rgba(72,207,173,0.12);
    border: 1px solid rgba(72,207,173,0.25);
    color: #48cfad;
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(108,99,255,0.15);
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Page title ── */
.page-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0 0%, #a78bfa 50%, #48cfad 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.page-subtitle {
    color: #4b5563;
    font-size: 0.85rem;
    margin-bottom: 28px;
    font-weight: 400;
}

/* ── Chart containers ── */
.chart-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 4px;
    margin-bottom: 16px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #6b7280;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 8px 18px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6c63ff 0%, #5a52d5 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.35) !important;
}

/* ── Selectbox / inputs ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Divider ── */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(108,99,255,0.3), transparent);
    margin: 16px 0;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0d1020; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #6c63ff, #48cfad);
    border-radius: 4px;
}

/* ── Sidebar nav items ── */
.sidebar-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #48cfad);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.sidebar-tagline {
    font-size: 0.7rem;
    color: #4b5563;
    margin-bottom: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.sidebar-stat {
    background: rgba(108,99,255,0.06);
    border: 1px solid rgba(108,99,255,0.12);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.78rem;
    color: #9ca3af;
    display: flex;
    justify-content: space-between;
}
.sidebar-stat-val {
    color: #a78bfa;
    font-weight: 600;
}

/* ── DataFrames ── */
.stDataFrame {
    border-radius: 14px !important;
    border: 1px solid rgba(108,99,255,0.15) !important;
    overflow: hidden;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    color: #9ca3af !important;
}

/* ── Radio (sidebar nav) ── */
[data-testid="stSidebar"] .stRadio > label { color: #9ca3af !important; font-size: 0.85rem; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] .stRadio div[role="radio"] {
    background: transparent;
    border-radius: 10px;
    padding: 2px 0;
}

/* ── Filter row ── */
.filter-row {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
}

/* ── Info badge ── */
.info-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(108,99,255,0.1);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    color: #a78bfa;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ────────────────────────────────────────────────────────────
PLOT_BG    = "rgba(0,0,0,0)"
PAPER_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.04)"
FONT_COLOR = "#9ca3af"
PALETTE    = ["#6c63ff","#48cfad","#f97316","#fbbf24","#a78bfa","#fb7185","#38bdf8","#34d399","#e879f9","#facc15"]
PALETTE_DIV = ["#6c63ff","#7c74ff","#9188ff","#a69eff","#bbb5ff","#d0ccff","#e4e2ff","#f2f1ff"]

def chart_layout(title="", height=360):
    return dict(
        title=dict(
            text=title,
            font=dict(size=13, color="#d1d5db", family="Space Grotesk"),
            x=0.01, xanchor="left"
        ),
        plot_bgcolor=PLOT_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR, family="Inter", size=11),
        xaxis=dict(
            gridcolor=GRID_COLOR, showgrid=True, zeroline=False,
            linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=10)
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, showgrid=True, zeroline=False,
            linecolor="rgba(255,255,255,0.06)", tickfont=dict(size=10)
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.03)",
            bordercolor="rgba(255,255,255,0.06)",
            borderwidth=1,
            font=dict(color=FONT_COLOR, size=10),
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0
        ),
        margin=dict(l=8, r=8, t=52, b=8),
        height=height,
        hoverlabel=dict(
            bgcolor="#1e2130",
            bordercolor="rgba(108,99,255,0.4)",
            font=dict(color="#e2e8f0", size=11)
        ),
    )

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df_fruits = pd.read_csv("dataset/fruits_clean.csv")
    df_dairy  = pd.read_csv("dataset/dairy_clean.csv")
    df_waste  = pd.read_csv("dataset/food_waste_clean.csv")
    df_expiry = pd.read_csv("dataset/food_expiry_clean.csv")
    for col in ["date","production_date","expiration_date"]:
        if col in df_dairy.columns:
            df_dairy[col] = pd.to_datetime(df_dairy[col], errors="coerce")
    return df_fruits, df_dairy, df_waste, df_expiry

df_fruits, df_dairy, df_waste, df_expiry = load_data()

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>🥗 FoodLens</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-tagline'>Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Overview", "🍎  Fruits", "🥛  Dairy", "♻️  Food Waste", "⏰  Food Expiry"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem;color:#4b5563;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;'>Dataset Summary</div>", unsafe_allow_html=True)

    for label, val in [("🍎 Fruits", f"{len(df_fruits)} rows"),
                       ("🥛 Dairy", f"{len(df_dairy):,} rows"),
                       ("♻️ Food Waste", f"{len(df_waste)} rows"),
                       ("⏰ Food Expiry", f"{len(df_expiry)} rows")]:
        st.markdown(f"""<div class='sidebar-stat'>
            <span>{label}</span>
            <span class='sidebar-stat-val'>{val}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem;color:#374151;text-align:center;'>Built with Streamlit & Plotly</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: render metric card
# ═══════════════════════════════════════════════════════════════════════════════
def metric(icon, value, label, sub="", badge=""):
    sub_html   = f"<div class='metric-sub'>{sub}</div>" if sub else ""
    badge_html = f"<div class='metric-badge'>{badge}</div>" if badge else ""
    return f"""<div class='metric-card'>
        <span class='metric-icon'>{icon}</span>
        <div class='metric-value'>{value}</div>
        <div class='metric-label'>{label}</div>
        {sub_html}{badge_html}
    </div>"""


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("<div class='page-title'>Food Analytics Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Comprehensive insights across fruits, dairy, global waste & expiry patterns</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    rev_m = df_dairy["approx._total_revenue(inr)"].sum() / 1e6
    waste_avg = df_waste["combined_figures_(kg/capita/year)"].mean()
    waste_pct = df_expiry["waste_flag"].mean() * 100

    with c1: st.markdown(metric("🍎", len(df_fruits), "Fruit Varieties", f"{df_fruits['season'].nunique()} seasons", "FRUITS"), unsafe_allow_html=True)
    with c2: st.markdown(metric("🥛", f"₹{rev_m:.1f}M", "Dairy Revenue", f"{df_dairy['product_name'].nunique()} products", "DAIRY"), unsafe_allow_html=True)
    with c3: st.markdown(metric("♻️", f"{waste_avg:.0f}", "Avg Waste kg/cap", f"{df_waste['country'].nunique()} countries", "WASTE"), unsafe_allow_html=True)
    with c4: st.markdown(metric("⏰", f"{waste_pct:.1f}%", "Expiry Waste Rate", f"{df_expiry['product_category'].nunique()} categories", "EXPIRY"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown("<div class='section-header'>♻️ Top 15 Countries — Food Waste per Capita</div>", unsafe_allow_html=True)
        top15 = df_waste.nlargest(15, "combined_figures_(kg/capita/year)")
        fig = go.Figure(go.Bar(
            x=top15["combined_figures_(kg/capita/year)"],
            y=top15["country"],
            orientation="h",
            marker=dict(
                color=top15["combined_figures_(kg/capita/year)"],
                colorscale=[[0,"#312e81"],[0.5,"#6c63ff"],[1,"#a78bfa"]],
                line=dict(width=0)
            ),
            text=top15["combined_figures_(kg/capita/year)"].astype(str) + " kg",
            textposition="outside",
            textfont=dict(size=9, color="#9ca3af"),
        ))
        fig.update_layout(**chart_layout("", 420))
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("<div class='section-header'>🌍 Waste by Region</div>", unsafe_allow_html=True)
        region_avg = df_waste.groupby("region")["combined_figures_(kg/capita/year)"].mean().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=region_avg["region"],
            values=region_avg["combined_figures_(kg/capita/year)"],
            hole=0.6,
            marker=dict(colors=PALETTE, line=dict(color="#080b14", width=2)),
            textinfo="label+percent",
            textfont=dict(size=10),
        ))
        fig2.add_annotation(text="Avg Waste<br>by Region", x=0.5, y=0.5,
                            font=dict(size=11, color="#d1d5db", family="Space Grotesk"),
                            showarrow=False)
        fig2.update_layout(**chart_layout("", 420))
        st.plotly_chart(fig2, use_container_width=True)

    # Revenue trend + waste category side by side
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='section-header'>🥛 Dairy Revenue Trend</div>", unsafe_allow_html=True)
        dairy_time = df_dairy.dropna(subset=["date"]).copy()
        dairy_time["month"] = dairy_time["date"].dt.to_period("M").dt.to_timestamp()
        rev_trend  = dairy_time.groupby("month")["approx._total_revenue(inr)"].sum().reset_index()
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=rev_trend["month"], y=rev_trend["approx._total_revenue(inr)"],
            mode="lines", fill="tozeroy",
            line=dict(color="#6c63ff", width=2.5),
            fillcolor="rgba(108,99,255,0.08)",
            hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>"
        ))
        fig3.update_layout(**chart_layout("", 280))
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-header'>⏰ Waste Rate by Product Category</div>", unsafe_allow_html=True)
        cat_waste = df_expiry.groupby("product_category")["waste_flag"].mean().reset_index()
        cat_waste["pct"] = cat_waste["waste_flag"] * 100
        cat_waste = cat_waste.sort_values("pct", ascending=True)
        fig4 = go.Figure(go.Bar(
            x=cat_waste["pct"], y=cat_waste["product_category"],
            orientation="h",
            marker=dict(
                color=cat_waste["pct"],
                colorscale=[[0,"#065f46"],[0.5,"#fbbf24"],[1,"#dc2626"]],
                line=dict(width=0)
            ),
            text=cat_waste["pct"].round(1).astype(str) + "%",
            textposition="outside",
            textfont=dict(size=9, color="#9ca3af"),
        ))
        fig4.update_layout(**chart_layout("", 280))
        st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FRUITS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🍎  Fruits":
    st.markdown("<div class='page-title'>🍎 Fruits Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Nutritional profiles, seasonal patterns & shelf life insights</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='filter-row'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1,2,1])
        with f1:
            season_opts = ["All"] + sorted(df_fruits["season"].dropna().unique().tolist())
            sel_season  = st.selectbox("🌱 Season", season_opts)
        with f2:
            taste_opts = sorted(df_fruits["taste_profile"].dropna().unique().tolist())
            sel_taste  = st.multiselect("🍬 Taste Profile", taste_opts, default=[])
        with f3:
            sort_by = st.selectbox("📊 Sort By", ["calories","sugar_g","fiber_g_per_100g","shelf_life_days"])
        st.markdown("</div>", unsafe_allow_html=True)

    df_f = df_fruits.copy()
    if sel_season != "All": df_f = df_f[df_f["season"] == sel_season]
    if sel_taste:           df_f = df_f[df_f["taste_profile"].isin(sel_taste)]

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric("🍎", len(df_f), "Fruits Shown", f"of {len(df_fruits)} total"), unsafe_allow_html=True)
    with c2: st.markdown(metric("🔥", f"{df_f['calories'].mean():.0f}", "Avg Calories", "per fruit"), unsafe_allow_html=True)
    with c3: st.markdown(metric("⏳", f"{df_f['shelf_life_days'].mean():.0f}d", "Avg Shelf Life"), unsafe_allow_html=True)
    with c4: st.markdown(metric("🍬", f"{df_f['sugar_g'].mean():.1f}g", "Avg Sugar"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊  Nutritional Profile", "🌱  Season & Shelf Life", "🔬  Correlation Matrix"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            df_sorted = df_f.sort_values(sort_by, ascending=False)
            fig = go.Figure(go.Bar(
                x=df_sorted["fruit_name"],
                y=df_sorted[sort_by],
                marker=dict(
                    color=df_sorted[sort_by],
                    colorscale=[[0,"#312e81"],[0.5,"#6c63ff"],[1,"#48cfad"]],
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{x}</b><br>" + sort_by + ": %{y}<extra></extra>"
            ))
            fig.update_layout(**chart_layout(f"{sort_by.replace('_',' ').title()} by Fruit", 340))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.scatter(
                df_f, x="sugar_g", y="calories",
                size="fiber_g_per_100g", color="taste_profile",
                hover_name="fruit_name",
                color_discrete_sequence=PALETTE,
                size_max=35,
                labels={"sugar_g":"Sugar (g)","calories":"Calories","fiber_g_per_100g":"Fiber"}
            )
            fig2.update_traces(
                marker=dict(line=dict(width=1, color="rgba(255,255,255,0.2)")),
                hovertemplate="<b>%{hovertext}</b><br>Sugar: %{x}g<br>Calories: %{y}<extra></extra>"
            )
            fig2.update_layout(**chart_layout("Sugar vs Calories  ·  bubble = fiber", 340))
            st.plotly_chart(fig2, use_container_width=True)

        # Radar chart — nutritional fingerprint
        st.markdown("<div class='section-header'>🔭 Nutritional Fingerprint (Radar)</div>", unsafe_allow_html=True)
        top8 = df_f.nlargest(8, "calories")
        cats = ["sugar_g","calories","water_percent","fiber_g_per_100g","avg_weight_g","shelf_life_days"]
        fig_r = go.Figure()
        for i, row in top8.iterrows():
            vals = [row[c] for c in cats]
            maxv = [df_f[c].max() for c in cats]
            norm = [v/m*100 if m else 0 for v,m in zip(vals,maxv)]
            fig_r.add_trace(go.Scatterpolar(
                r=norm + [norm[0]], theta=cats + [cats[0]],
                fill="toself", name=row["fruit_name"],
                line=dict(width=1.5),
                fillcolor="rgba(108,99,255,0.05)"
            ))
        fig_r.update_layout(
            **chart_layout("", 400),
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, gridcolor=GRID_COLOR, tickfont=dict(size=8), range=[0,110]),
                angularaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=9))
            )
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            sc = df_f["season"].value_counts().reset_index()
            sc.columns = ["season","count"]
            fig = go.Figure(go.Pie(
                labels=sc["season"], values=sc["count"],
                hole=0.58, marker=dict(colors=PALETTE, line=dict(color="#080b14",width=2)),
                textinfo="label+percent", textfont=dict(size=10)
            ))
            fig.add_annotation(text=f"{len(df_f)}<br>Fruits", x=0.5, y=0.5,
                                font=dict(size=13, color="#d1d5db", family="Space Grotesk"), showarrow=False)
            fig.update_layout(**chart_layout("Fruits by Season", 320))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.violin(
                df_f, x="season", y="shelf_life_days",
                color="season", color_discrete_sequence=PALETTE,
                box=True, points="all",
                labels={"shelf_life_days":"Shelf Life (days)","season":""}
            )
            fig2.update_layout(**chart_layout("Shelf Life Distribution by Season", 320))
            st.plotly_chart(fig2, use_container_width=True)

        # Timeline-style shelf life bar
        df_sl = df_f.sort_values("shelf_life_days", ascending=True)
        fig3 = go.Figure(go.Bar(
            x=df_sl["shelf_life_days"], y=df_sl["fruit_name"],
            orientation="h",
            marker=dict(
                color=df_sl["shelf_life_days"],
                colorscale=[[0,"#7f1d1d"],[0.5,"#fbbf24"],[1,"#065f46"]],
                line=dict(width=0)
            ),
            text=df_sl["shelf_life_days"].astype(str) + " days",
            textposition="outside", textfont=dict(size=9, color="#9ca3af"),
            hovertemplate="<b>%{y}</b><br>Shelf life: %{x} days<extra></extra>"
        ))
        fig3.update_layout(**chart_layout("Shelf Life Ranking", 360))
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        num_cols = ["sugar_g","calories","acidity_ph","avg_weight_g","water_percent","fiber_g_per_100g","shelf_life_days"]
        corr = df_f[num_cols].corr().round(2)
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0,"#312e81"],[0.3,"#1e2130"],[0.7,"#1e2130"],[1,"#48cfad"]],
            zmid=0, text=corr.values,
            texttemplate="%{text}",
            textfont=dict(size=10),
            hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>r = %{z}<extra></extra>",
            showscale=True,
            colorbar=dict(
                tickfont=dict(color=FONT_COLOR, size=9),
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(255,255,255,0.05)",
                thickness=12
            )
        ))
        fig.update_layout(**chart_layout("Nutritional Correlation Matrix", 420))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Raw Data Table"):
        st.dataframe(df_f.reset_index(drop=True), use_container_width=True, height=280)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DAIRY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🥛  Dairy":
    st.markdown("<div class='page-title'>🥛 Dairy Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Revenue performance, stock management & sales channel breakdown</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='filter-row'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1:
            prod_opts  = ["All"] + sorted(df_dairy["product_name"].dropna().unique().tolist())
            sel_prod   = st.selectbox("📦 Product", prod_opts)
        with f2:
            brand_opts = ["All"] + sorted(df_dairy["brand"].dropna().unique().tolist())
            sel_brand  = st.selectbox("🏷️ Brand", brand_opts)
        with f3:
            chan_opts   = ["All"] + sorted(df_dairy["sales_channel"].dropna().unique().tolist())
            sel_chan    = st.selectbox("🛒 Sales Channel", chan_opts)
        st.markdown("</div>", unsafe_allow_html=True)

    df_d = df_dairy.copy()
    if sel_prod  != "All": df_d = df_d[df_d["product_name"]  == sel_prod]
    if sel_brand != "All": df_d = df_d[df_d["brand"]         == sel_brand]
    if sel_chan   != "All": df_d = df_d[df_d["sales_channel"] == sel_chan]

    c1, c2, c3, c4 = st.columns(4)
    total_rev  = df_d["approx._total_revenue(inr)"].sum() / 1e6
    avg_price  = df_d["price_per_unit_(sold)"].mean()
    avg_shelf  = df_d["shelf_life_(days)"].mean()
    with c1: st.markdown(metric("📋", f"{len(df_d):,}", "Records"), unsafe_allow_html=True)
    with c2: st.markdown(metric("💰", f"₹{total_rev:.1f}M", "Total Revenue", f"{df_d['brand'].nunique()} brands"), unsafe_allow_html=True)
    with c3: st.markdown(metric("🏷️", f"₹{avg_price:.0f}", "Avg Price / Unit"), unsafe_allow_html=True)
    with c4: st.markdown(metric("📅", f"{avg_shelf:.0f}d", "Avg Shelf Life"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["💰  Revenue", "📦  Stock & Sales", "🗺️  Location"])

    with tab1:
        c1, c2 = st.columns([3,2])
        with c1:
            rev_prod = df_d.groupby("product_name")["approx._total_revenue(inr)"].sum().reset_index()
            rev_prod.columns = ["product","revenue"]
            rev_prod = rev_prod.sort_values("revenue", ascending=True).tail(10)
            fig = go.Figure(go.Bar(
                x=rev_prod["revenue"], y=rev_prod["product"],
                orientation="h",
                marker=dict(
                    color=rev_prod["revenue"],
                    colorscale=[[0,"#312e81"],[1,"#48cfad"]],
                    line=dict(width=0)
                ),
                text=(rev_prod["revenue"]/1e3).round(0).astype(int).astype(str) + "k",
                textposition="outside", textfont=dict(size=9, color="#9ca3af"),
                hovertemplate="<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>"
            ))
            fig.update_layout(**chart_layout("Revenue by Product (Top 10)", 340))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            rev_chan = df_d.groupby("sales_channel")["approx._total_revenue(inr)"].sum().reset_index()
            rev_chan.columns = ["channel","revenue"]
            fig2 = go.Figure(go.Pie(
                labels=rev_chan["channel"], values=rev_chan["revenue"],
                hole=0.58,
                marker=dict(colors=PALETTE, line=dict(color="#080b14",width=2)),
                textinfo="label+percent", textfont=dict(size=10)
            ))
            fig2.add_annotation(text="Sales<br>Channel", x=0.5, y=0.5,
                                 font=dict(size=11, color="#d1d5db", family="Space Grotesk"), showarrow=False)
            fig2.update_layout(**chart_layout("", 340))
            st.plotly_chart(fig2, use_container_width=True)

        dairy_time = df_d.dropna(subset=["date"]).copy()
        dairy_time["month"] = dairy_time["date"].dt.to_period("M").dt.to_timestamp()
        rev_time   = dairy_time.groupby(["month","product_name"])["approx._total_revenue(inr)"].sum().reset_index()
        fig3 = px.line(
            rev_time, x="month", y="approx._total_revenue(inr)",
            color="product_name", color_discrete_sequence=PALETTE,
            labels={"approx._total_revenue(inr)":"Revenue (INR)","month":"","product_name":"Product"}
        )
        fig3.update_traces(line=dict(width=2))
        fig3.update_layout(**chart_layout("Monthly Revenue Trend by Product", 300))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            stock = df_d.groupby("product_name").agg(
                stock=("quantity_in_stock_(liters/kg)","sum"),
                sold=("quantity_sold_(liters/kg)","sum")
            ).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="In Stock", x=stock["product_name"], y=stock["stock"],
                                 marker_color="#6c63ff", marker_line_width=0))
            fig.add_trace(go.Bar(name="Sold", x=stock["product_name"], y=stock["sold"],
                                 marker_color="#48cfad", marker_line_width=0))
            fig.update_layout(**chart_layout("Stock vs Sold by Product", 340), barmode="group")
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            shelf = df_d.groupby("storage_condition")["shelf_life_(days)"].mean().reset_index()
            fig2 = go.Figure(go.Bar(
                x=shelf["storage_condition"],
                y=shelf["shelf_life_(days)"],
                marker=dict(
                    color=shelf["shelf_life_(days)"],
                    colorscale=[[0,"#fbbf24"],[1,"#48cfad"]],
                    line=dict(width=0)
                ),
                text=shelf["shelf_life_(days)"].round(0).astype(int).astype(str) + " d",
                textposition="outside", textfont=dict(size=9, color="#9ca3af"),
            ))
            fig2.update_layout(**chart_layout("Avg Shelf Life by Storage Condition", 340))
            st.plotly_chart(fig2, use_container_width=True)

        # Farm size distribution
        farm_rev = df_d.groupby("farm_size")["approx._total_revenue(inr)"].sum().reset_index()
        farm_rev.columns = ["farm_size","revenue"]
        fig3 = go.Figure(go.Pie(
            labels=farm_rev["farm_size"], values=farm_rev["revenue"],
            hole=0.55, marker=dict(colors=PALETTE, line=dict(color="#080b14",width=2)),
            textinfo="label+percent", textfont=dict(size=10)
        ))
        fig3.add_annotation(text="By Farm<br>Size", x=0.5, y=0.5,
                             font=dict(size=11, color="#d1d5db", family="Space Grotesk"), showarrow=False)
        fig3.update_layout(**chart_layout("Revenue by Farm Size", 300))
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        rev_loc = df_d.groupby("customer_location")["approx._total_revenue(inr)"].sum().reset_index()
        rev_loc.columns = ["location","revenue"]
        fig = px.treemap(
            rev_loc, path=["location"], values="revenue",
            color="revenue",
            color_continuous_scale=[[0,"#1e1b4b"],[0.5,"#6c63ff"],[1,"#48cfad"]],
        )
        fig.update_traces(
            textfont=dict(size=12, family="Space Grotesk"),
            hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<extra></extra>"
        )
        fig.update_layout(**chart_layout("Revenue by Customer Location", 460))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Raw Data Table"):
        st.dataframe(df_d.reset_index(drop=True), use_container_width=True, height=300)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FOOD WASTE
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "♻️  Food Waste":
    st.markdown("<div class='page-title'>♻️ Global Food Waste</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Per-capita waste estimates across countries, regions & supply chain segments</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='filter-row'>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            region_opts = ["All"] + sorted(df_waste["region"].dropna().unique().tolist())
            sel_region  = st.selectbox("🌍 Region", region_opts)
        with f2:
            conf_opts   = ["All"] + sorted(df_waste["confidence_in_estimate"].dropna().unique().tolist())
            sel_conf    = st.selectbox("📊 Confidence Level", conf_opts)
        st.markdown("</div>", unsafe_allow_html=True)

    df_w = df_waste.copy()
    if sel_region != "All": df_w = df_w[df_w["region"]                == sel_region]
    if sel_conf   != "All": df_w = df_w[df_w["confidence_in_estimate"] == sel_conf]

    c1, c2, c3, c4 = st.columns(4)
    total_hh = df_w["household_estimate_(tonnes/year)"].sum() / 1e6
    total_fs = df_w["food_service_estimate_(tonnes/year)"].sum() / 1e6
    with c1: st.markdown(metric("🌍", len(df_w), "Countries", f"{df_w['region'].nunique()} regions"), unsafe_allow_html=True)
    with c2: st.markdown(metric("📦", f"{df_w['combined_figures_(kg/capita/year)'].mean():.0f}", "Avg Waste kg/cap"), unsafe_allow_html=True)
    with c3: st.markdown(metric("🏠", f"{total_hh:.1f}M t", "Household Waste"), unsafe_allow_html=True)
    with c4: st.markdown(metric("🍽️", f"{total_fs:.1f}M t", "Food Service Waste"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🌍  By Country", "🏭  By Segment", "📊  Distribution"])

    with tab1:
        top20 = df_w.sort_values("combined_figures_(kg/capita/year)", ascending=False).head(20)
        fig = px.bar(
            top20, x="country", y="combined_figures_(kg/capita/year)",
            color="region", color_discrete_sequence=PALETTE,
            labels={"combined_figures_(kg/capita/year)":"kg/capita/year","country":""}
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(**chart_layout("Top 20 Countries by Food Waste per Capita", 380))
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.scatter(
            df_w,
            x="household_estimate_(kg/capita/year)",
            y="food_service_estimate_(kg/capita/year)",
            size="combined_figures_(kg/capita/year)",
            color="region", hover_name="country",
            color_discrete_sequence=PALETTE, size_max=30,
            labels={
                "household_estimate_(kg/capita/year)":"Household (kg/cap)",
                "food_service_estimate_(kg/capita/year)":"Food Service (kg/cap)"
            }
        )
        fig2.update_traces(
            marker=dict(line=dict(width=1, color="rgba(255,255,255,0.15)")),
            hovertemplate="<b>%{hovertext}</b><br>Household: %{x}<br>Food Service: %{y}<extra></extra>"
        )
        fig2.update_layout(**chart_layout("Household vs Food Service Waste", 360))
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        region_seg = df_w.groupby("region").agg(
            household=("household_estimate_(tonnes/year)","sum"),
            retail=("retail_estimate_(tonnes/year)","sum"),
            food_service=("food_service_estimate_(tonnes/year)","sum")
        ).reset_index()

        fig = go.Figure()
        for col, color, label in [
            ("household","#6c63ff","Household"),
            ("retail","#48cfad","Retail"),
            ("food_service","#f97316","Food Service")
        ]:
            fig.add_trace(go.Bar(name=label, x=region_seg["region"], y=region_seg[col],
                                 marker_color=color, marker_line_width=0))
        fig.update_layout(**chart_layout("Waste by Segment & Region (tonnes/year)", 380), barmode="stack")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(
                df_w, x="combined_figures_(kg/capita/year)",
                nbins=30, color_discrete_sequence=["#6c63ff"],
                labels={"combined_figures_(kg/capita/year)":"kg/capita/year"}
            )
            fig.update_traces(marker_line_width=0)
            fig.update_layout(**chart_layout("Waste Distribution Across Countries", 320))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            conf_data = df_w["confidence_in_estimate"].value_counts().reset_index()
            conf_data.columns = ["confidence","count"]
            fig2 = go.Figure(go.Pie(
                labels=conf_data["confidence"], values=conf_data["count"],
                hole=0.58, marker=dict(colors=PALETTE, line=dict(color="#080b14",width=2)),
                textinfo="label+percent", textfont=dict(size=10)
            ))
            fig2.add_annotation(text="Confidence<br>Level", x=0.5, y=0.5,
                                 font=dict(size=10, color="#d1d5db", family="Space Grotesk"), showarrow=False)
            fig2.update_layout(**chart_layout("", 320))
            st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Full Dataset"):
        st.dataframe(df_w.reset_index(drop=True), use_container_width=True, height=320)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FOOD EXPIRY
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "⏰  Food Expiry":
    st.markdown("<div class='page-title'>⏰ Food Expiry & Waste Patterns</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Storage behaviour, expiry intervals & category-level waste analysis</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='filter-row'>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            cat_opts = ["All"] + sorted(df_expiry["product_category"].dropna().unique().tolist())
            sel_cat  = st.selectbox("📦 Product Category", cat_opts)
        with f2:
            storage_opts = ["All","Fridge","Freezer","Pantry"]
            sel_storage  = st.selectbox("🧊 Storage Type", storage_opts)
        st.markdown("</div>", unsafe_allow_html=True)

    df_e = df_expiry.copy()
    if sel_cat != "All": df_e = df_e[df_e["product_category"] == sel_cat]
    if sel_storage == "Fridge":  df_e = df_e[df_e["storage_fridge"]  == True]
    elif sel_storage == "Freezer": df_e = df_e[df_e["storage_freezer"] == True]
    elif sel_storage == "Pantry":  df_e = df_e[df_e["storage_pantry"]  == True]

    c1, c2, c3, c4 = st.columns(4)
    wp      = df_e["waste_flag"].mean() * 100
    avg_exp = df_e["days_until_expiry"].mean()
    avg_qty = df_e["quantity"].mean()
    with c1: st.markdown(metric("📋", f"{len(df_e):,}", "Records"), unsafe_allow_html=True)
    with c2: st.markdown(metric("⚠️", f"{wp:.1f}%", "Waste Rate", "items wasted"), unsafe_allow_html=True)
    with c3: st.markdown(metric("📅", f"{avg_exp:.1f}d", "Avg Days to Expiry"), unsafe_allow_html=True)
    with c4: st.markdown(metric("🛒", f"{avg_qty:.1f}", "Avg Quantity Purchased"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📦  Category Analysis", "🗓️  Time Patterns", "📊  Expiry Intervals"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            cat_waste = df_e.groupby("product_category")["waste_flag"].mean().reset_index()
            cat_waste.columns = ["category","waste_rate"]
            cat_waste["waste_rate"] *= 100
            cat_waste = cat_waste.sort_values("waste_rate", ascending=True)
            fig = go.Figure(go.Bar(
                x=cat_waste["waste_rate"], y=cat_waste["category"],
                orientation="h",
                marker=dict(
                    color=cat_waste["waste_rate"],
                    colorscale=[[0,"#065f46"],[0.5,"#fbbf24"],[1,"#dc2626"]],
                    line=dict(width=0)
                ),
                text=cat_waste["waste_rate"].round(1).astype(str) + "%",
                textposition="outside", textfont=dict(size=9, color="#9ca3af"),
                hovertemplate="<b>%{y}</b><br>Waste Rate: %{x:.1f}%<extra></extra>"
            ))
            fig.update_layout(**chart_layout("Waste Rate by Category", 340))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig2 = px.violin(
                df_e, x="product_category", y="days_until_expiry",
                color="product_category", color_discrete_sequence=PALETTE,
                box=True, points=False,
                labels={"days_until_expiry":"Days Until Expiry","product_category":""}
            )
            fig2.update_layout(**chart_layout("Days Until Expiry Distribution", 340))
            st.plotly_chart(fig2, use_container_width=True)

        # Storage comparison dual axis
        storage_data = {
            "Storage": ["Fridge","Freezer","Pantry"],
            "Count": [
                int(df_e["storage_fridge"].sum()),
                int(df_e["storage_freezer"].sum()),
                int(df_e["storage_pantry"].sum())
            ],
            "Waste Rate": [
                df_e[df_e["storage_fridge"]]["waste_flag"].mean()*100,
                df_e[df_e["storage_freezer"]]["waste_flag"].mean()*100,
                df_e[df_e["storage_pantry"]]["waste_flag"].mean()*100,
            ]
        }
        df_storage = pd.DataFrame(storage_data)
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(go.Bar(
            name="Count", x=df_storage["Storage"], y=df_storage["Count"],
            marker_color="#6c63ff", marker_line_width=0, opacity=0.8
        ), secondary_y=False)
        fig3.add_trace(go.Scatter(
            name="Waste Rate (%)", x=df_storage["Storage"], y=df_storage["Waste Rate"],
            mode="lines+markers",
            marker=dict(size=10, color="#ff6b6b", line=dict(width=2, color="#080b14")),
            line=dict(color="#ff6b6b", width=2.5)
        ), secondary_y=True)
        fig3.update_layout(
            title=dict(text="Storage Type — Count vs Waste Rate",
                       font=dict(size=13, color="#d1d5db", family="Space Grotesk"), x=0.01),
            plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
            font=dict(color=FONT_COLOR, family="Inter", size=11),
            legend=dict(bgcolor="rgba(255,255,255,0.03)", bordercolor="rgba(255,255,255,0.06)",
                        borderwidth=1, font=dict(size=10)),
            margin=dict(l=8,r=8,t=52,b=8), height=320,
            hoverlabel=dict(bgcolor="#1e2130", bordercolor="rgba(108,99,255,0.4)",
                            font=dict(color="#e2e8f0", size=11)),
        )
        fig3.update_yaxes(title_text="Count", gridcolor=GRID_COLOR, secondary_y=False)
        fig3.update_yaxes(title_text="Waste Rate (%)", gridcolor=GRID_COLOR, secondary_y=True)
        fig3.update_xaxes(gridcolor=GRID_COLOR)
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                     7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        day_map   = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}

        c1, c2 = st.columns(2)
        with c1:
            mw = df_e.groupby("purchase_month")["waste_flag"].mean().reset_index()
            mw["month_name"] = mw["purchase_month"].map(month_map)
            mw["pct"] = mw["waste_flag"] * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=mw["purchase_month"], y=mw["pct"],
                mode="lines+markers+text",
                line=dict(color="#6c63ff", width=2.5),
                marker=dict(size=9, color="#6c63ff", line=dict(width=2, color="#080b14")),
                fill="tozeroy", fillcolor="rgba(108,99,255,0.07)",
                text=mw["pct"].round(1).astype(str) + "%",
                textposition="top center", textfont=dict(size=8),
                hovertemplate="<b>%{x}</b><br>Waste Rate: %{y:.1f}%<extra></extra>"
            ))
            fig.update_layout(**chart_layout("Monthly Waste Rate", 320))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            dw = df_e.groupby("purchase_day_of_week")["waste_flag"].mean().reset_index()
            dw["day_name"] = dw["purchase_day_of_week"].map(day_map)
            dw["pct"] = dw["waste_flag"] * 100
            fig2 = go.Figure(go.Bar(
                x=dw["day_name"], y=dw["pct"],
                marker=dict(
                    color=dw["pct"],
                    colorscale=[[0,"#312e81"],[1,"#fb7185"]],
                    line=dict(width=0)
                ),
                text=dw["pct"].round(1).astype(str) + "%",
                textposition="outside", textfont=dict(size=9, color="#9ca3af"),
                hovertemplate="<b>%{x}</b><br>Waste Rate: %{y:.1f}%<extra></extra>"
            ))
            fig2.update_layout(**chart_layout("Day of Week Waste Rate", 320))
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            ic = df_e["intervals_until_expiry"].value_counts().reset_index()
            ic.columns = ["interval","count"]
            fig = go.Figure(go.Bar(
                x=ic["interval"], y=ic["count"],
                marker=dict(
                    color=ic["count"],
                    colorscale=[[0,"#312e81"],[1,"#48cfad"]],
                    line=dict(width=0)
                ),
                hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
            ))
            fig.update_layout(**chart_layout("Count by Expiry Interval", 340))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            used = df_e.groupby("product_category")["used_before_expiry"].mean().reset_index()
            used.columns = ["category","used_pct"]
            used["used_pct"] *= 100
            used = used.sort_values("used_pct", ascending=True)
            fig2 = go.Figure(go.Bar(
                x=used["used_pct"], y=used["category"],
                orientation="h",
                marker=dict(
                    color=used["used_pct"],
                    colorscale=[[0,"#dc2626"],[0.5,"#fbbf24"],[1,"#065f46"]],
                    line=dict(width=0)
                ),
                text=used["used_pct"].round(1).astype(str) + "%",
                textposition="outside", textfont=dict(size=9, color="#9ca3af"),
                hovertemplate="<b>%{y}</b><br>Used: %{x:.1f}%<extra></extra>"
            ))
            fig2.update_layout(**chart_layout("% Used Before Expiry by Category", 340))
            st.plotly_chart(fig2, use_container_width=True)

    with st.expander("📋 Raw Data Table"):
        st.dataframe(df_e.reset_index(drop=True), use_container_width=True, height=300)