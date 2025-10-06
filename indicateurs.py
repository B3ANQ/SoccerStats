import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Indicateurs avancés", layout="wide", page_icon="📈")
st.title("Indicateurs avancés & KPI composites")

df = pd.read_csv('datas_cleaned/All_Stats_Field_Player.csv')

df_indic = df[['Player', 'Pos', 'passes_reussies', 'passes_progressives_distance',
               'Interceptions', 'Tackles_Tkl', 'duel_gagné', 'duel_total',
               'Short_Cmp%', 'Medium_Cmp%', 'Long_Cmp%']].copy()

radar_cols = ['passes_reussies', 'passes_progressives_distance', 'Interceptions',
              'Tackles_Tkl', 'duel_gagné', 'duel_total',
              'Short_Cmp%', 'Medium_Cmp%', 'Long_Cmp%']

for col in radar_cols:
    df_indic[col] = df_indic[col].astype(str).str.replace(r'[^\d\.]', '', regex=True)
    df_indic[col] = pd.to_numeric(df_indic[col], errors='coerce')

df_indic['duel_reussite'] = df_indic['duel_gagné'] / df_indic['duel_total']
df_indic['efficacité_passes'] = df_indic[['Short_Cmp%', 'Medium_Cmp%', 'Long_Cmp%']].mean(axis=1)

df_indic['impact_global'] = (
    df_indic['passes_reussies'] * 0.3 +
    df_indic['passes_progressives_distance'] * 0.2 +
    df_indic['Interceptions'] * 0.15 +
    df_indic['Tackles_Tkl'] * 0.15 +
    df_indic['duel_reussite'] * 100 * 0.2
)

st.markdown("###  Tableau des indicateurs enrichis")
st.dataframe(df_indic[['Player', 'Pos', 'passes_reussies', 'passes_progressives_distance',
                       'Interceptions', 'Tackles_Tkl', 'duel_reussite',
                       'efficacité_passes', 'impact_global']].round(2))

st.markdown("###  Profil radar d’un joueur")
joueur = st.selectbox("Choisir un joueur", df_indic['Player'].dropna().sort_values())
data_joueur = df_indic[df_indic['Player'] == joueur].iloc[0]

labels = ['Passes réussies', 'Passes progressives', 'Interceptions', 'Tacles', 'Duels gagnés', 'Précision passes']
values = [
    data_joueur['passes_reussies'],
    data_joueur['passes_progressives_distance'],
    data_joueur['Interceptions'],
    data_joueur['Tackles_Tkl'],
    data_joueur['duel_gagné'],
    data_joueur['efficacité_passes']
]

max_vals = [df_indic[col].max() for col in
            ['passes_reussies', 'passes_progressives_distance', 'Interceptions',
             'Tackles_Tkl', 'duel_gagné', 'efficacité_passes']]
values_norm = [v / m * 100 if pd.notna(v) and m != 0 else 0 for v, m in zip(values, max_vals)]

fig, ax = plt.subplots(figsize=(2.5, 2.5), subplot_kw=dict(polar=True))
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values_norm += values_norm[:1]
angles += angles[:1]

ax.set_facecolor("#f9f9f9")
ax.spines["polar"].set_visible(False)
ax.grid(color="lightgray", linestyle="--", linewidth=0.5)
ax.plot(angles, values_norm, color='#007acc', linewidth=2)
ax.fill(angles, values_norm, color='#007acc', alpha=0.2)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=7)
ax.set_yticklabels([])
ax.set_title(f"Profil radar de {joueur}", size=10, pad=8)


st.markdown("<div style='text-align: center; max-width: 280px; margin: auto;'>", unsafe_allow_html=True)
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)
