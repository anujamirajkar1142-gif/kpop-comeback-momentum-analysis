import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Atlantic Recording Corporation — South Korea Analytics",
    page_icon="◈",
    layout="wide"
)

# ------------------------------------------------------------------
# VISUAL SYSTEM — brushed-chrome-on-black, record-label plate aesthetic
# ------------------------------------------------------------------

VOID = "#0A0A0B"
PANEL = "#141518"
PANEL_BORDER = "#2A2C30"
CHROME_HI = "#F2F3F4"
CHROME_MID = "#C7CACD"
CHROME_LO = "#6E7176"
GOLD = "#C9A961"
TEXT_PRIMARY = "#ECEDEE"
TEXT_MUTED = "#8B8E93"

CHART_COLORWAY = [GOLD, CHROME_MID, "#7A8288", "#5C6066", CHROME_HI]
ALBUM_TYPE_COLORS = {"Single": GOLD, "Album": CHROME_MID}
EXPLICIT_COLORS = {"Clean": CHROME_MID, "Explicit": GOLD}

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_PRIMARY};
    }}

    .stApp {{
        background: {VOID};
    }}

    /* ---- Hero plate ---- */
    .plate-header {{
        background: linear-gradient(180deg, #17181A 0%, #0A0A0B 100%);
        border: 1px solid {PANEL_BORDER};
        border-radius: 6px;
        padding: 28px 36px 22px 36px;
        margin-bottom: 6px;
        position: relative;
        overflow: hidden;
    }}
    .plate-header::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, {CHROME_HI}, {GOLD}, {CHROME_HI}, transparent);
        opacity: 0.85;
    }}
    .plate-eyebrow {{
        font-family: 'Oswald', sans-serif;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 4px;
        color: {GOLD};
        text-transform: uppercase;
        margin: 0 0 8px 0;
    }}
    .plate-title {{
        font-family: 'Oswald', sans-serif;
        font-size: 40px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
        background: linear-gradient(180deg, {CHROME_HI} 0%, {CHROME_MID} 55%, {CHROME_LO} 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }}
    .plate-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: {TEXT_MUTED};
        margin: 8px 0 0 0;
        letter-spacing: 0.3px;
    }}

    /* ---- Section eyebrows ---- */
    .section-eyebrow {{
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 34px 0 14px 0;
    }}
    .section-eyebrow .tag {{
        font-family: 'Oswald', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: {TEXT_PRIMARY};
        white-space: nowrap;
    }}
    .section-eyebrow .line {{
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, {CHROME_LO}, transparent);
    }}

    /* ---- Chrome divider (signature element) ---- */
    .chrome-divider {{
        height: 2px;
        border: none;
        margin: 30px 0;
        background: linear-gradient(90deg, transparent 0%, {CHROME_LO} 15%, {CHROME_HI} 50%, {CHROME_LO} 85%, transparent 100%);
        opacity: 0.6;
    }}

    /* ---- KPI plates ---- */
    div[data-testid="stMetric"] {{
        background: linear-gradient(180deg, #17181A 0%, #101113 100%);
        border: 1px solid {PANEL_BORDER};
        border-radius: 4px;
        padding: 16px 18px 14px 18px;
    }}
    div[data-testid="stMetricLabel"] p {{
        font-family: 'Oswald', sans-serif !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: {TEXT_MUTED} !important;
    }}
    div[data-testid="stMetricValue"] {{
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: {GOLD} !important;
    }}

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: {PANEL};
        border-right: 1px solid {PANEL_BORDER};
    }}
    section[data-testid="stSidebar"] h2 {{
        font-family: 'Oswald', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: {GOLD};
    }}

    /* ---- Dataframe ---- */
    div[data-testid="stDataFrame"] {{
        border: 1px solid {PANEL_BORDER};
        border-radius: 4px;
    }}

    /* ---- Footer ---- */
    .plate-footer {{
        text-align: center;
        padding: 22px 0 8px 0;
        font-family: 'Oswald', sans-serif;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: {TEXT_MUTED};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def styled(fig, height=420):
    """Apply the chrome/gold dark template to a plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(family="Inter, sans-serif", color=TEXT_PRIMARY, size=12),
        colorway=CHART_COLORWAY,
        height=height,
        margin=dict(l=40, r=30, t=30, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=PANEL_BORDER, zerolinecolor=PANEL_BORDER)
    fig.update_yaxes(gridcolor=PANEL_BORDER, zerolinecolor=PANEL_BORDER)
    return fig


def section(tag: str):
    st.markdown(
        f"""
        <div class="section-eyebrow">
            <span class="tag">{tag}</span>
            <span class="line"></span>
        </div>
        """,
        unsafe_allow_html=True
    )


def divider():
    st.markdown("<hr class='chrome-divider' />", unsafe_allow_html=True)


# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------

chart_history = pd.read_csv("chart_history.csv", parse_dates=["date"])
reentry_events = pd.read_csv("reentry_events.csv", parse_dates=["reentry_date", "exit_date"])
momentum = pd.read_csv(
    "momentum_enriched.csv",
    parse_dates=["reentry_date", "exit_date", "peak_date", "first_entry_date"]
)
momentum["album_type"] = momentum["album_type"].str.title()

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------

st.markdown(
    """
    <div class="plate-header">
        <p class="plate-eyebrow">Atlantic Recording Corporation · South Korea Top 50</p>
        <p class="plate-title">Comeback &amp; Fandom Intelligence</p>
        <p class="plate-subtitle">Chart re-entry detection, momentum spikes, and fandom-intensity signal — built on daily playlist telemetry.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------
# SIDEBAR — FILTERS
# ------------------------------------------------------------------

st.sidebar.markdown("## Filters")

start_date = chart_history["date"].min()
end_date = chart_history["date"].max()

selected_dates = st.sidebar.date_input(
    "Date range",
    value=(start_date, end_date),
    min_value=start_date,
    max_value=end_date,
)

song_filter = st.sidebar.multiselect("Song", sorted(momentum["song"].dropna().unique()))
artist_filter = st.sidebar.multiselect("Artist", sorted(momentum["artist"].dropna().unique()))
album_filter = st.sidebar.selectbox("Album type", ["All", "Single", "Album"])

min_reentries = int(momentum["reentry_frequency"].min())
max_reentries = int(momentum["reentry_frequency"].max())
reentry_count_filter = st.sidebar.slider("Minimum re-entries per song", min_reentries, max_reentries, min_reentries)

days_outside_filter = st.sidebar.slider("Minimum days outside chart", 0, int(momentum["days_outside"].max()), 0)

filtered = momentum.copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    range_start, range_end = selected_dates
    filtered = filtered[
        (filtered["reentry_date"] >= pd.Timestamp(range_start)) &
        (filtered["reentry_date"] <= pd.Timestamp(range_end))
    ]

if song_filter:
    filtered = filtered[filtered["song"].isin(song_filter)]

if artist_filter:
    filtered = filtered[filtered["artist"].isin(artist_filter)]

if album_filter != "All":
    filtered = filtered[filtered["album_type"] == album_filter]

filtered = filtered[filtered["reentry_frequency"] >= reentry_count_filter]
filtered = filtered[filtered["days_outside"] >= days_outside_filter]

# ------------------------------------------------------------------
# KPIs
# ------------------------------------------------------------------

section("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Songs", chart_history["song"].nunique())
col2.metric("Artists", chart_history["artist"].nunique())
col3.metric("Re-entry Events", len(reentry_events))
col4.metric("Avg Momentum Spike", round(momentum["momentum_spike_score"].mean(), 2))

col5, col6, col7, col8 = st.columns(4)
col5.metric(
    "Avg Re-Entry Frequency",
    round(momentum.groupby("song")["reentry_frequency"].first().mean(), 2),
    help="Average number of re-entries per song — fandom reactivation indicator"
)
col6.metric(
    "Avg Retention (days)",
    round(momentum["post_comeback_retention_days"].mean(), 1),
    help="Days a song stays charting after a comeback re-entry"
)
_album_avg = momentum.groupby("album_type")["momentum_spike_score"].mean()
_advantage_index = round(_album_avg.get("Single", 0) - _album_avg.get("Album", 0), 2)
col7.metric(
    "Album Advantage Index",
    _advantage_index,
    help="Avg momentum spike: Single − Album. Positive = singles comeback stronger."
)
col8.metric(
    "Avg Fandom Intensity",
    round(momentum["fandom_intensity_proxy_score"].mean(), 2),
    help="Composite of re-entry frequency, momentum spike and recovery speed (0–100)"
)

divider()

# ------------------------------------------------------------------
# REENTRY TIMELINE
# ------------------------------------------------------------------

section("Re-Entry Timeline")

timeline = filtered.groupby("reentry_date").size().reset_index(name="count")
fig = px.line(timeline, x="reentry_date", y="count", markers=True)
fig.update_traces(line_color=GOLD, marker=dict(color=CHROME_HI, size=6))
st.plotly_chart(styled(fig), use_container_width=True)

# ------------------------------------------------------------------
# MOMENTUM SPIKE
# ------------------------------------------------------------------

section("Momentum Spike Detection")

top_momentum = filtered.sort_values("momentum_spike_score", ascending=False).head(20)
fig = px.bar(
    top_momentum, x="song", y="momentum_spike_score",
    color="album_type", color_discrete_map=ALBUM_TYPE_COLORS
)
fig.update_xaxes(tickangle=-45)
st.plotly_chart(styled(fig, height=460), use_container_width=True)

# ------------------------------------------------------------------
# COMEBACK VS FIRST ENTRY
# ------------------------------------------------------------------

section("Comeback vs First Entry")

first_entry_available = filtered.dropna(subset=["first_entry_position"])
if first_entry_available.empty:
    st.info("No rows in the current filter selection have first-entry data.")
else:
    fig = px.scatter(
        first_entry_available,
        x="first_entry_position",
        y="reentry_position",
        color="album_type",
        color_discrete_map=ALBUM_TYPE_COLORS,
        hover_data=["song", "artist", "peak_rank"],
        size="momentum_spike_score",
        labels={"first_entry_position": "First Entry Position (rank)", "reentry_position": "Re-entry Position (rank)"},
    )
    st.plotly_chart(styled(fig), use_container_width=True)

# ------------------------------------------------------------------
# CONTENT ATTRIBUTES
# ------------------------------------------------------------------

section("Content Attribute vs Momentum")

c1, c2 = st.columns(2)

with c1:
    st.markdown("**Single vs Album — Comeback Strength**")
    album_summary = filtered.groupby("album_type")["momentum_spike_score"].mean().reset_index()
    fig = px.bar(
        album_summary, x="album_type", y="momentum_spike_score",
        color="album_type", color_discrete_map=ALBUM_TYPE_COLORS
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(styled(fig, height=340), use_container_width=True)

with c2:
    st.markdown("**Explicit vs Clean — Momentum**")
    explicit_summary = filtered.copy()
    explicit_summary["is_explicit"] = explicit_summary["is_explicit"].map({True: "Explicit", False: "Clean"})
    fig = px.box(
        explicit_summary, x="is_explicit", y="momentum_spike_score",
        color="is_explicit", color_discrete_map=EXPLICIT_COLORS
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(styled(fig, height=340), use_container_width=True)

st.markdown("**Song Duration vs Spike Magnitude**")
fig = px.scatter(
    filtered, x="duration_minutes", y="momentum_spike_score",
    color="album_type", color_discrete_map=ALBUM_TYPE_COLORS,
    hover_data=["song"], size="recovery_speed_score",
)
st.plotly_chart(styled(fig), use_container_width=True)

# ------------------------------------------------------------------
# LEADERBOARD
# ------------------------------------------------------------------

section("Fandom Intensity Leaderboard")

leaderboard = filtered.sort_values("fandom_intensity_proxy_score", ascending=False)[
    ["song", "artist", "album_type", "reentry_frequency", "days_outside",
     "momentum_spike_score", "recovery_speed_score", "fandom_intensity_proxy_score"]
]
st.dataframe(leaderboard.head(20), use_container_width=True, hide_index=True)

divider()

st.markdown(
    '<p class="plate-footer">Atlantic Recording Corporation &nbsp;·&nbsp; South Korea Analytics Desk</p>',
    unsafe_allow_html=True
)
