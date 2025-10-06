import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import altair as alt

# --- Configuration de la page ---
st.set_page_config(page_title="Analyse Joueurs Football", layout="wide")

# --- Chargement des données ---
players = pd.read_csv("./datas/top5-players.csv")
defensive = pd.read_csv("./datas/Defensive.csv", header=[0,1])  # multi-index sur colonnes

# Nettoyage du fichier défensif
defensive.columns = [
    "_".join([str(c) for c in col if "Unnamed" not in str(c)]).strip()
    for col in defensive.columns.values
]
defensive = defensive.rename(columns={"Player_": "Player"})
defensive = defensive.dropna(subset=["Player"])

# --- Titre ---
st.title("Tableau de bord - Statistiques joueurs (Top 5 ligues)")

# --- 1. Nombre de joueurs par position ---
st.subheader("Nombre de joueurs par position")
fig, ax = plt.subplots(figsize=(8, 5))
sns.countplot(data=players, x="Pos", order=players["Pos"].value_counts().index, palette="viridis", ax=ax)
ax.set_title("Nombre de joueurs par position")
ax.set_xlabel("Position")
ax.set_ylabel("Nombre de joueurs")
st.pyplot(fig)

# --- 2. Répartition des joueurs par nation (top 10) ---
st.subheader("Répartition des joueurs par nation (Top 10)")
fig, ax = plt.subplots(figsize=(10, 6))
top_nations = players["Nation"].value_counts().head(10)
sns.barplot(x=top_nations.values, y=top_nations.index, palette="magma", ax=ax)
ax.set_title("Top 10 nations représentées")
ax.set_xlabel("Nombre de joueurs")
ax.set_ylabel("Nation")
st.pyplot(fig)

# --- 3. Top 10 joueurs par buts marqués ---
st.subheader("Top 10 joueurs par buts marqués")
fig, ax = plt.subplots(figsize=(10, 6))
top_scorers = players.nlargest(10, "Gls")[["Player", "Gls"]]
sns.barplot(x="Gls", y="Player", data=top_scorers, palette="coolwarm", ax=ax)
ax.set_title("Top 10 joueurs par buts marqués")
ax.set_xlabel("Buts")
ax.set_ylabel("Joueur")
st.pyplot(fig)

# --- 4. Top 10 joueurs par interceptions ---
st.subheader("Top 10 joueurs par interceptions")
fig, ax = plt.subplots(figsize=(10, 6))
if "Int" in defensive.columns:
    defensive["Int"] = pd.to_numeric(defensive["Int"], errors="coerce")
    top_interceptions = defensive.dropna(subset=["Int"]).nlargest(10, "Int")[["Player", "Int"]]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Int", y="Player", data=top_interceptions, palette="crest", ax=ax)
    ax.set_title("Top 10 joueurs par interceptions")
    ax.set_xlabel("Interceptions")
    ax.set_ylabel("Joueur")
    st.pyplot(fig)

# --- 5. Efficacité offensive (nuage de points interactif) ---
st.subheader("⚡ Efficacité offensive (xG vs Buts par 90min)")

# Selectbox pour le poste (offensive)
positions_off = players['Pos'].unique()
selected_position_off = st.selectbox(
    "Sélectionner le poste à afficher (offensive)",
    options=positions_off
)

# Filtrer les joueurs selon le poste sélectionné
players_filtered = players[players['Pos'] == selected_position_off]

fig = px.scatter(
    players_filtered,
    x="xG_90",
    y="Gls_90",
    color="Pos",
    hover_data=["Player", "Squad", "xG_90", "Gls_90"],
    size_max=12,
    title=f"Efficacité offensive : xG/90 vs Buts/90 ({selected_position_off})"
)
fig.update_traces(marker=dict(size=10, opacity=0.7))
st.plotly_chart(fig, use_container_width=True)



# --- 6. Efficacité défensive (nuage de points interactif) ---
st.subheader("🛡️ Efficacité défensive (Tackles won vs Interceptions)")

defensive = pd.read_csv("./datas/Defensive.csv", header=1)

# Nettoyage des colonnes
defensive.rename(columns=lambda x: x.strip(), inplace=True)
defensive.columns = defensive.columns.str.replace(' ', '_')

# Conversion en numérique
numeric_cols = ['TklW', 'Int']
for col in numeric_cols:
    if col in defensive.columns:
        defensive[col] = pd.to_numeric(defensive[col], errors='coerce')

# Supprimer les lignes sans données numériques
defensive_clean = defensive.dropna(subset=numeric_cols)

# Selectbox pour le poste (défensive)
positions_def = defensive_clean['Pos'].unique()
selected_position_def = st.selectbox(
    "Sélectionner le poste à afficher (défensive)",
    options=positions_def
)

# Filtrer les joueurs selon le poste sélectionné
defensive_filtered = defensive_clean[defensive_clean['Pos'] == selected_position_def]

# Scatter plot avec Altair
scatter = alt.Chart(defensive_filtered).mark_circle(size=100, opacity=0.7).encode(
    x=alt.X('TklW:Q', title='Tackles won par 90 min'),
    y=alt.Y('Int:Q', title='Interceptions par 90 min'),
    tooltip=['Player:N', 'TklW:Q', 'Int:Q', 'Pos:N'],  # affichage au survol
    color=alt.Color('Pos:N', legend=alt.Legend(title="Poste"))
).interactive()

st.altair_chart(scatter, use_container_width=True)




# --- 7. Buts par 90 minutes (interactif) ---
st.subheader("🥅 Top joueurs par buts/90 min")

top_goals_per90 = players.nlargest(20, "Gls_90")[["Player", "Gls_90", "Squad"]]
fig = px.bar(
    top_goals_per90,
    x="Gls_90",
    y="Player",
    orientation="h",
    hover_data=["Player", "Squad", "Gls_90"],
    color="Gls_90",
    title="Top 20 joueurs par buts/90 min",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig, use_container_width=True)

st.title("Analyse des gardiens : Save% vs GA90")

# Charger le CSV (2ème ligne = header)
df = pd.read_csv("./datas/keepers.csv", header=1)

# Nettoyer Save%
df['Save%'] = pd.to_numeric(df['Save%'], errors='coerce')

# Supprimer les lignes vides
df = df.dropna(subset=['Save%', 'GA90'])

# Graphique Altair
chart = (
    alt.Chart(df)
    .mark_circle(size=100)
    .encode(
        x=alt.X("Save%:Q", title="Pourcentage de Saves (%)"),
        y=alt.Y("GA90:Q", title="GA90 (Buts encaissés par 90 min)", scale=alt.Scale(reverse=True)),
        color=alt.Color("Comp:N", title="Compétition"),
        tooltip=["Player", "Squad", "Comp", "Save%", "GA90"]
    )
    .properties(
        width=800,
        height=500,
        title="Comparaison des gardiens : Save% vs GA90"
    )
)

# Ajouter les noms des joueurs
text = chart.mark_text(align="left", dx=7, dy=-5, fontSize=10).encode(
    text="Player"
)

# Combiner
final_chart = chart + text

# Afficher dans Streamlit
st.altair_chart(final_chart.interactive(), use_container_width=True)