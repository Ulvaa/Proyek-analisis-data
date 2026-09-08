
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ==============================
# CUSTOM THEME
# ==============================
st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
    }

    html, body, [class*="css"] {
        font-family: "Arial", sans-serif;
    }

    /* =========================
       SIDEBAR
       ========================= */
    [data-testid="stSidebar"] {
        background-color: #1E3A5F;
    }

    /* Label sidebar tetap putih */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: white !important;
    }

    /* =========================
       SELECTBOX
       ========================= */

    /* Background kotak select */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: white !important;
        border-radius: 8px;
    }

    /* Teks value selectbox */
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #1F2937 !important;
    }

    /* Teks input */
    [data-testid="stSidebar"] input {
        color: #1F2937 !important;
    }

    /* Icon panah selectbox */
    [data-testid="stSidebar"] svg {
        fill: #1F2937 !important;
    }

    h1 {
        color: #1E3A5F !important;
    }

    h2 {
        color: #244A73 !important;
    }

    h3 {
        color: #2E5D8A !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #A9B5DF !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA
# -----------------------------
@st.cache_data
def load_data():
    day = pd.read_csv("day_data.csv")
    hour = pd.read_csv("hour_data.csv")

    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])

    return day, hour

day, hour = load_data()

# -----------------------------
# LABELS
# -----------------------------
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow"
}

day_map = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}

hour["season_name"] = hour["season"].map(season_map)
hour["weather_name"] = hour["weathersit"].map(weather_map)
hour["day_name"] = hour["weekday"].map(day_map)

day["season_name"] = day["season"].map(season_map)
day["weather_name"] = day["weathersit"].map(weather_map)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🔎 Filter")

years = sorted(hour["yr"].dropna().unique())
year_options = ["All"] + [str(int(y) + 2011) for y in years]

selected_year = st.sidebar.selectbox(
    "Tahun",
    year_options
)

season_options = sorted(hour["season_name"].dropna().unique())
selected_seasons = st.sidebar.multiselect(
    "Musim",
    season_options,
    default=season_options
)

weather_options = sorted(hour["weather_name"].dropna().unique())
selected_weather = st.sidebar.multiselect(
    "Cuaca",
    weather_options,
    default=weather_options
)

filtered_hour = hour[
    hour["season_name"].isin(selected_seasons)
    & hour["weather_name"].isin(selected_weather)
].copy()

filtered_day = day[
    day["season_name"].isin(selected_seasons)
    & day["weather_name"].isin(selected_weather)
].copy()

if selected_year != "All":
    selected_yr = int(selected_year) - 2011
    filtered_hour = filtered_hour[filtered_hour["yr"] == selected_yr]
    filtered_day = filtered_day[filtered_day["yr"] == selected_yr]

# -----------------------------
# HEADER
# -----------------------------
st.title("🚲 Bike Sharing Dashboard")
st.markdown(
    "Analisis pola penyewaan sepeda berdasarkan **waktu, musim, cuaca, "
    "hari kerja, dan hari libur**."
)

if filtered_hour.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

# -----------------------------
# KPI
# -----------------------------
total_rentals = filtered_hour["cnt"].sum()
avg_hourly = filtered_hour["cnt"].mean()
max_hourly = filtered_hour["cnt"].max()

st.markdown("""
<style>
.kpi-card {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #d9d9d9;
    background-color: #ABD2FA;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    text-align: center;
    min-height: 125px;
}

.kpi-title {
    font-size: 16px;
    font-weight: 600;
    font-color : #091540;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
    font-color : #091540;
}
</style>
""", unsafe_allow_html=True)

k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Penyewaan</div>
            <div class="kpi-value">{total_rentals:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Rata-rata per Jam</div>
            <div class="kpi-value">{avg_hourly:,.1f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Penyewaan Tertinggi</div>
            <div class="kpi-value">{max_hourly:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =========================================================
# 1. HARI DAN JAM DENGAN PENYEWAAN TERBANYAK
# =========================================================
st.header("Waktu dengan Penyewaan Tertinggi")

st.subheader("Pada hari apa dan jam berapa jumlah penyewaan sepeda terbanyak?")

# Aggregate by weekday-hour
heatmap_data = (
    filtered_hour
    .groupby(["weekday", "hr"])["cnt"]
    .mean()
    .unstack(fill_value=0)
    .reindex(index=range(7), columns=range(24), fill_value=0)
)

# Find maximum weekday-hour combination
max_pair = heatmap_data.stack().idxmax()
max_value = heatmap_data.loc[max_pair[0], max_pair[1]]
max_day = day_map[max_pair[0]]
max_hour = max_pair[1]

c1, c2 = st.columns([2.2, 1])

with c1:
    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(heatmap_data.values, aspect="auto", cmap="Blues")

    ax.set_xticks(range(24))
    ax.set_yticks(range(7))
    ax.set_xticklabels(range(24))
    ax.set_yticklabels([day_map[i] for i in range(7)])

    ax.set_xlabel("Jam")
    ax.set_ylabel("Hari")
    ax.set_title("Rata-rata Penyewaan Berdasarkan Hari dan Jam")

    fig.colorbar(im, ax=ax, label="Rata-rata Penyewaan")
    st.pyplot(fig)
    plt.close(fig)

with c2:
    st.metric("Hari dengan puncak", max_day)
    st.metric("Jam dengan puncak", f"{max_hour:02d}:00")
    st.metric("Rata-rata penyewaan", f"{max_value:,.1f}")

    st.info(
        f"Puncak rata-rata penyewaan terjadi pada "
        f"**{max_day}, pukul {max_hour:02d}:00**."
    )

# Overall weekday
weekday_avg = (
    filtered_hour.groupby("weekday")["cnt"]
    .mean()
    .reindex(range(7))
)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(
    [day_map[i] for i in range(7)],
    weekday_avg.values,
    color = "#0A2947"
)
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xlabel("Hari")
ax.tick_params(axis="x", rotation=30)
ax.set_title("Rata-rata Penyewaan per Hari")
st.pyplot(fig)
plt.close(fig)

st.divider()

# =========================================================
# 2. MUSIM DAN CUACA
# =========================================================
st.header("Pengaruh Musim dan Cuaca")

st.subheader("Bagaimana pengaruh musim dan cuaca terhadap jumlah penyewaan sepeda?")

season_avg = (
    filtered_hour.groupby("season_name")["cnt"]
    .mean()
    .sort_values(ascending=False)
)

weather_avg = (
    filtered_hour.groupby("weather_name")["cnt"]
    .mean()
    .sort_values(ascending=False)
)

c1, c2 = st.columns(2)

with c1:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(season_avg.index, season_avg.values, color=["#2D336B", "#7886C7", "#A9B5DF", "#C6CFF0"])
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Rata-rata Penyewaan Berdasarkan Musim")
    st.pyplot(fig)
    plt.close(fig)

with c2:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(weather_avg.index, weather_avg.values,  color=["#2D336B", "#7886C7", "#A9B5DF", "#C6CFF0"])
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
    ax.tick_params(axis="x", rotation=25)
    st.pyplot(fig)
    plt.close(fig)

best_season = season_avg.idxmax()
best_weather = weather_avg.idxmax()

st.success(
    f"🌱 Rata-rata penyewaan tertinggi berdasarkan musim adalah "
    f"**{best_season}**. "
    f"Sedangkan kondisi cuaca dengan rata-rata penyewaan tertinggi adalah "
    f"**{best_weather}**."
)

# Cross analysis: season x weather
st.subheader("Interaksi Musim dan Cuaca")

season_weather = (
    filtered_hour
    .groupby(["season_name", "weather_name"])["cnt"]
    .mean()
    .unstack()
)

st.dataframe(
    season_weather.style.format("{:,.1f}"),
    use_container_width=True
)

st.divider()

# =========================================================
# 3. WORKING DAY VS HOLIDAY
# =========================================================
st.header("Hari Kerja vs Hari Libur")

st.subheader(
    "Bagaimana perbandingan penyewaan sepeda pada hari kerja dan hari libur?"
)

# workingday: 1 = working day, 0 = non-working day
filtered_hour["day_type"] = filtered_hour["workingday"].map({
    1: "Hari Kerja",
    0: "Hari Libur / Weekend"
})

day_type_avg = (
    filtered_hour.groupby("day_type")["cnt"]
    .mean()
    .reindex(["Hari Kerja", "Hari Libur / Weekend"])
)

day_type_total = (
    filtered_hour.groupby("day_type")["cnt"]
    .sum()
    .reindex(["Hari Kerja", "Hari Libur / Weekend"])
)

# Pie chart total penyewaan
fig, ax = plt.subplots(figsize=(8, 5))

colors = ["#2D336B","#7886C7"]

wedges, texts, autotexts = ax.pie(
    day_type_avg.values,
    labels=day_type_avg.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    textprops={"fontsize": 11}
)
# Persentase dibuat lebih jelas
for autotext in autotexts:
    autotext.set_fontweight("bold")
    autotext.set_color("white")

ax.set_title("Proporsi Rata-Rata Penyewaan: Hari Kerja vs Hari Libur/Weekend")
ax.axis("equal")
st.pyplot(fig)
plt.close(fig)
