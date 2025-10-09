import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SoccerStats Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        color: #f8f9fa;
        text-align: center;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
        text-shadow: 2px 2px 6px #000000;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #cfcfcf;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 15px;
        text-shadow: 1px 1px 4px #000000;
    }

    [data-testid="stExpander"] {
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
    }

    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SoccerStats Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Classement interactif des meilleurs joueurs européens</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("datas_cleaned/All_Stats_Field_Player.csv")
    return df

df = load_data()

possible_cols = df.columns.tolist()

with st.expander("Filtres de sélection", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        selected_league = st.selectbox(
            "Sélectionne une Ligue",
            sorted(df['Comp'].dropna().unique())
        )
    with col2:
        top_choice = st.selectbox(
            "Choisis un Top 3 à afficher",
            [
                "Top 3 meilleurs défenseurs",
                "Top 3 meilleurs passeurs",
                "Top 3 meilleurs récupérateurs",
                "Top 3 global (score combiné)"
            ]
        )

filtered_df = df[df['Comp'] == selected_league]

if filtered_df.empty:
    st.warning("Aucun joueur trouvé pour cette ligue.")
else:
    if top_choice == "Top 3 meilleurs défenseurs":
        metric = "Tackles_Tkl"
        color_scale = "Greens"
        icon = "🛡️"
        filtered_df["Score"] = filtered_df["Tackles_Tkl"].fillna(0)

    elif top_choice == "Top 3 meilleurs passeurs":
        metric = "passes_reussies"
        color_scale = "Blues"
        icon = "🎯"
        filtered_df["Score"] = filtered_df["passes_reussies"].fillna(0)

    elif top_choice == "Top 3 meilleurs récupérateurs":
        if "Interceptions" in df.columns:
            metric = "Interceptions"
            color_scale = "mrybm"
            icon = "🔥"
            filtered_df["Score"] = filtered_df["Interceptions"].fillna(0)
        else:
            st.warning("La colonne 'Interceptions' n'existe pas dans le dataset.")
            st.stop()

    else:
        metric = "Score"
        color_scale = "Purples"
        icon = "⚡"
        filtered_df["Score"] = (
            filtered_df["Tackles_Tkl"].fillna(0) * 3 +
            filtered_df["passes_reussies"].fillna(0) * 2
        )

    st.markdown(
        f"<h3 class='section-title'>{icon} {top_choice} - {selected_league}</h3>",
        unsafe_allow_html=True
    )

    top3 = filtered_df.sort_values(by="Score", ascending=False).head(3)

    cols_to_show = ['Player', 'Squad', 'Comp', 'Pos', 'Score']
    if metric in df.columns and metric != "Score":
        cols_to_show.insert(4, metric)

    st.dataframe(
        top3[cols_to_show],
        hide_index=True,
        use_container_width=True
    )

    fig = px.bar(
        top3,
        x="Player",
        y="Score",
        color="Score",
        text="Score",
        title=f"{icon} {top_choice} - {selected_league}",
        color_continuous_scale=color_scale
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        xaxis_title="Joueur",
        yaxis_title=f"Score ({metric})",
        title_x=0.5,
        title_font=dict(color="white"),
        font=dict(color="white"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)