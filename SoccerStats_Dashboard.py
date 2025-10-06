import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="SoccerStats Dashboard ⚽",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">⚽ SoccerStats Dashboard 📊</h1>', unsafe_allow_html=True)
st.markdown("**Analyse des performances des joueurs des 5 grands championnats européens (2023-2024)**")

@st.cache_data
def load_data():
    """Charge toutes les données nettoyées"""
    data = {}
    data_dir = 'datas_cleaned'
    
    if not os.path.exists(data_dir):
        st.error(f"Le dossier {data_dir} n'existe pas. Veuillez d'abord exécuter le script de nettoyage.")
        return None
    
    files = {
        'players': 'top5-players.csv',
        'keepers': 'keepers.csv',
        'defensive': 'Defensive.csv',
        'passing': 'Passing.csv',
        'all_stats': 'All_Stats_Field_Player.csv'
    }
    
    for key, filename in files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            try:
                data[key] = pd.read_csv(filepath)
                st.sidebar.success(f"✓ {filename} chargé")
            except Exception as e:
                st.sidebar.error(f"✗ Erreur lors du chargement de {filename}: {e}")
        else:
            st.sidebar.warning(f"⚠ {filename} non trouvé")
    
    return data

data = load_data()

if data is None or len(data) == 0:
    st.stop()

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choisir une page",
    ["🏠 Accueil", "📊 Analyse Générale", "⚽ Joueurs de Champ", "🥅 Gardiens", "🔍 Comparaison de Joueurs", "📈 Analyses Avancées"]
)

if page == "🏠 Accueil":
    col1, col2, col3 = st.columns(3)
    
    if 'players' in data:
        with col1:
            st.metric("Nombre de joueurs", len(data['players']))
        with col2:
            if 'keepers' in data:
                st.metric("Gardiens", len(data['keepers']))
        with col3:
            if 'Nation' in data['players'].columns:
                st.metric("Nationalités", data['players']['Nation'].nunique())
    
    st.markdown("---")
    
    st.subheader("📋 Aperçu des Datasets")
    
    for key, df in data.items():
        if not df.empty:
            with st.expander(f"Dataset: {key.upper()} ({len(df)} lignes)"):
                st.dataframe(df.head())
                st.write(f"**Colonnes:** {', '.join(df.columns.tolist())}")

elif page == "📊 Analyse Générale":
    st.header("Analyse Générale des Données")
    
    if 'players' in data:
        df = data['players']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Age' in df.columns:
                st.subheader("Distribution par Âge")
                fig, ax = plt.subplots()
                df['Age'].hist(bins=20, ax=ax, alpha=0.7, color='skyblue')
                ax.set_xlabel('Âge')
                ax.set_ylabel('Nombre de joueurs')
                st.pyplot(fig)
        
        with col2:
            if 'Nation' in df.columns:
                st.subheader("Top 10 Nationalités")
                nation_counts = df['Nation'].value_counts().head(10)
                fig, ax = plt.subplots()
                nation_counts.plot(kind='bar', ax=ax, color='lightcoral')
                ax.set_ylabel('Nombre de joueurs')
                plt.xticks(rotation=45)
                st.pyplot(fig)
        
        if 'Comp' in df.columns:
            st.subheader("Répartition par Ligue")
            comp_counts = df['Comp'].value_counts()
            fig = px.pie(values=comp_counts.values, names=comp_counts.index, 
                        title="Distribution des joueurs par ligue")
            st.plotly_chart(fig, use_container_width=True)
        
        if 'Pos' in df.columns:
            st.subheader("Répartition par Poste")
            pos_counts = df['Pos'].value_counts()
            fig = px.bar(x=pos_counts.index, y=pos_counts.values,
                        title="Nombre de joueurs par poste")
            fig.update_xaxis(title="Poste")
            fig.update_yaxis(title="Nombre de joueurs")
            st.plotly_chart(fig, use_container_width=True)

elif page == "⚽ Joueurs de Champ":
    st.header("Analyse des Joueurs de Champ")
    
    if 'players' in data:
        df = data['players']
        
        st.sidebar.subheader("Filtres")
        
        if 'Comp' in df.columns:
            leagues = ['Toutes'] + df['Comp'].unique().tolist()
            selected_league = st.sidebar.selectbox("Ligue", leagues)
            if selected_league != 'Toutes':
                df = df[df['Comp'] == selected_league]
        
        if 'Pos' in df.columns:
            positions = ['Tous'] + df['Pos'].unique().tolist()
            selected_pos = st.sidebar.selectbox("Poste", positions)
            if selected_pos != 'Tous':
                df = df[df['Pos'] == selected_pos]
        
        if 'Age' in df.columns:
            age_range = st.sidebar.slider("Âge", 
                                        int(df['Age'].min()), 
                                        int(df['Age'].max()), 
                                        (int(df['Age'].min()), int(df['Age'].max())))
            df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Gls' in df.columns:
                st.subheader("🥅 Top 15 Buteurs")
                top_scorers = df.nlargest(15, 'Gls')[['Player', 'Gls', 'Squad']]
                fig = px.bar(top_scorers, x='Gls', y='Player', orientation='h',
                           hover_data=['Squad'], color='Gls',
                           color_continuous_scale='Reds')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Ast' in df.columns:
                st.subheader("🎯 Top 15 Passeurs")
                top_assist = df.nlargest(15, 'Ast')[['Player', 'Ast', 'Squad']]
                fig = px.bar(top_assist, x='Ast', y='Player', orientation='h',
                           hover_data=['Squad'], color='Ast',
                           color_continuous_scale='Blues')
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
        
        if 'Gls' in df.columns and 'Ast' in df.columns:
            st.subheader("Relation Buts vs Passes Décisives")
            fig = px.scatter(df, x='Gls', y='Ast', hover_data=['Player', 'Squad'],
                           title="Corrélation entre buts et passes décisives")
            st.plotly_chart(fig, use_container_width=True)
        
        if 'Goals_per_minute' in df.columns:
            st.subheader("Top 15 - Efficacité (Buts par minute)")
            df_eff = df[df['Min'] > 500]  # Filtre minimum de minutes
            top_efficiency = df_eff.nlargest(15, 'Goals_per_minute')[['Player', 'Goals_per_minute', 'Gls', 'Min']]
            fig = px.bar(top_efficiency, x='Goals_per_minute', y='Player', orientation='h',
                        hover_data=['Gls', 'Min'])
            st.plotly_chart(fig, use_container_width=True)

elif page == "🥅 Gardiens":
    st.header("Analyse des Gardiens")
    
    if 'keepers' in data:
        df = data['keepers']
        
        st.sidebar.subheader("Filtres Gardiens")
        
        if 'Comp' in df.columns:
            leagues = ['Toutes'] + df['Comp'].unique().tolist()
            selected_league = st.sidebar.selectbox("Ligue", leagues, key="keeper_league")
            if selected_league != 'Toutes':
                df = df[df['Comp'] == selected_league]
        
        if 'Age' in df.columns:
            age_range = st.sidebar.slider("Âge des gardiens", 
                                        int(df['Age'].min()), 
                                        int(df['Age'].max()), 
                                        (int(df['Age'].min()), int(df['Age'].max())),
                                        key="keeper_age")
            df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
        
        if 'Min' in df.columns:
            min_minutes = st.sidebar.slider("Minutes minimales", 0, int(df['Min'].max()), 500, key="keeper_min")
            df = df[df['Min'] >= min_minutes]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Gardiens analysés", len(df))
        with col2:
            if 'Saves' in df.columns:
                st.metric("Total arrêts", int(df['Saves'].sum()))
        with col3:
            if 'CS' in df.columns:
                st.metric("Total clean sheets", int(df['CS'].sum()))
        with col4:
            if 'GA' in df.columns:
                st.metric("Total buts encaissés", int(df['GA'].sum()))
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Saves' in df.columns:
                st.subheader("🧤 Top 15 - Nombre d'arrêts")
                top_saves = df.nlargest(15, 'Saves')[['Player', 'Saves', 'Squad', 'Comp']]
                fig = px.bar(top_saves, x='Saves', y='Player', orientation='h',
                           hover_data=['Squad', 'Comp'], color='Saves',
                           color_continuous_scale='Greens',
                           title="Gardiens avec le plus d'arrêts")
                fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'CS' in df.columns:
                st.subheader("🛡️ Top 15 - Clean Sheets")
                top_cs = df.nlargest(15, 'CS')[['Player', 'CS', 'Squad', 'Comp']]
                fig = px.bar(top_cs, x='CS', y='Player', orientation='h',
                           hover_data=['Squad', 'Comp'], color='CS',
                           color_continuous_scale='Blues',
                           title="Gardiens avec le plus de clean sheets")
                fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Save%' in df.columns or 'Save_pct' in df.columns:
                save_col = 'Save%' if 'Save%' in df.columns else 'Save_pct'
                st.subheader("📊 Top 15 - Pourcentage d'arrêts")
                df_qualified = df[df['Saves'] > 20]  # Minimum 20 arrêts
                if len(df_qualified) > 0:
                    top_save_pct = df_qualified.nlargest(15, save_col)[['Player', save_col, 'Saves', 'Squad']]
                    fig = px.bar(top_save_pct, x=save_col, y='Player', orientation='h',
                               hover_data=['Saves', 'Squad'], color=save_col,
                               color_continuous_scale='Oranges',
                               title="Meilleur pourcentage d'arrêts (min. 20 arrêts)")
                    fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Pas assez de données pour le pourcentage d'arrêts")
        
        with col2:
            if 'GA' in df.columns:
                st.subheader("🎯 Top 15 - Moins de buts encaissés")
                df_qualified = df[df['Min'] > 900]  # Minimum 10 matchs
                if len(df_qualified) > 0:
                    least_goals = df_qualified.nsmallest(15, 'GA')[['Player', 'GA', 'Squad', 'Min']]
                    fig = px.bar(least_goals, x='GA', y='Player', orientation='h',
                               hover_data=['Squad', 'Min'], color='GA',
                               color_continuous_scale='Reds_r',
                               title="Gardiens ayant encaissé le moins de buts")
                    fig.update_layout(height=600, yaxis={'categoryorder':'total descending'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Pas assez de données pour les buts encaissés")
        
        st.markdown("---")
        st.subheader("📈 Analyses de Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'CS' in df.columns and 'GA' in df.columns:
                st.subheader("Clean Sheets vs Buts Encaissés")
                fig = px.scatter(df, x='GA', y='CS', 
                               hover_data=['Player', 'Squad'],
                               color='Comp' if 'Comp' in df.columns else None,
                               title="Relation entre clean sheets et buts encaissés",
                               labels={'GA': 'Buts encaissés', 'CS': 'Clean Sheets'})
                fig.add_annotation(
                    x=df['GA'].max() * 0.7,
                    y=df['CS'].max() * 0.9,
                    text="Zone optimale:<br>Peu de buts encaissés<br>+ Beaucoup de CS",
                    showarrow=True,
                    arrowhead=2
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Saves' in df.columns and 'Min' in df.columns:
                st.subheader("Arrêts vs Minutes jouées")
                df['Saves_per_90'] = (df['Saves'] / df['Min']) * 90
                fig = px.scatter(df, x='Min', y='Saves_per_90',
                               hover_data=['Player', 'Squad', 'Saves'],
                               color='Comp' if 'Comp' in df.columns else None,
                               title="Arrêts par 90 minutes vs Temps de jeu",
                               labels={'Min': 'Minutes jouées', 'Saves_per_90': 'Arrêts/90min'})
                st.plotly_chart(fig, use_container_width=True)
        
        if 'Comp' in df.columns:
            st.markdown("---")
            st.subheader("📊 Comparaison par Ligue")
            
            league_stats = df.groupby('Comp').agg({
                'Saves': ['mean', 'sum'],
                'CS': ['mean', 'sum'],
                'GA': ['mean', 'sum'],
                'Player': 'count'
            }).round(2)
            
            league_stats.columns = ['Arrêts_moy', 'Arrêts_total', 'CS_moy', 'CS_total', 
                                  'GA_moy', 'GA_total', 'Nb_gardiens']
            league_stats = league_stats.reset_index()
            
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Arrêts moyens par gardien', 'Clean Sheets moyens', 
                              'Buts encaissés moyens', 'Nombre de gardiens'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            fig.add_trace(
                go.Bar(x=league_stats['Comp'], y=league_stats['Arrêts_moy'], 
                      name='Arrêts', marker_color='green'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(x=league_stats['Comp'], y=league_stats['CS_moy'], 
                      name='Clean Sheets', marker_color='blue'),
                row=1, col=2
            )
            
            fig.add_trace(
                go.Bar(x=league_stats['Comp'], y=league_stats['GA_moy'], 
                      name='Buts encaissés', marker_color='red'),
                row=2, col=1
            )
            
            fig.add_trace(
                go.Bar(x=league_stats['Comp'], y=league_stats['Nb_gardiens'], 
                      name='Nombre gardiens', marker_color='orange'),
                row=2, col=2
            )
            
            fig.update_layout(height=600, showlegend=False,
                            title_text="Statistiques des gardiens par ligue")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Tableau détaillé par ligue")
            st.dataframe(league_stats, use_container_width=True)
        
        # Top gardiens toutes catégories
        st.markdown("---")
        st.subheader("🏆 Hall of Fame des Gardiens")
        
        if all(col in df.columns for col in ['Saves', 'CS', 'GA']):
            df_score = df.copy()
            df_score['Saves_norm'] = (df_score['Saves'] - df_score['Saves'].min()) / (df_score['Saves'].max() - df_score['Saves'].min())
            df_score['CS_norm'] = (df_score['CS'] - df_score['CS'].min()) / (df_score['CS'].max() - df_score['CS'].min())
            df_score['GA_norm'] = 1 - ((df_score['GA'] - df_score['GA'].min()) / (df_score['GA'].max() - df_score['GA'].min()))
            
            df_score['Performance_Score'] = (df_score['Saves_norm'] * 0.4 + 
                                           df_score['CS_norm'] * 0.4 + 
                                           df_score['GA_norm'] * 0.2) * 100
            
            top_overall = df_score.nlargest(10, 'Performance_Score')[
                ['Player', 'Squad', 'Comp', 'Saves', 'CS', 'GA', 'Performance_Score']
            ].round(1)
            
            st.dataframe(top_overall, use_container_width=True)
            st.caption("Score basé sur : Arrêts (40%) + Clean Sheets (40%) + Moins de buts encaissés (20%)")
    
    else:
        st.error("❌ Données des gardiens non disponibles")
        st.info("Vérifiez que le fichier 'keepers.csv' existe dans le dossier 'datas_cleaned'")

elif page == "🔍 Comparaison de Joueurs":
    st.header("Comparaison de Joueurs")
    
    if 'players' in data:
        df = data['players']
        
        players_list = df['Player'].unique().tolist()
        
        col1, col2 = st.columns(2)
        
        with col1:
            player1 = st.selectbox("Joueur 1", players_list, key="player1")
        with col2:
            player2 = st.selectbox("Joueur 2", players_list, key="player2")
        
        if player1 != player2:
            p1_data = df[df['Player'] == player1].iloc[0]
            p2_data = df[df['Player'] == player2].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"👤 {player1}")
                st.write(f"**Équipe:** {p1_data.get('Squad', 'N/A')}")
                st.write(f"**Âge:** {p1_data.get('Age', 'N/A')}")
                st.write(f"**Position:** {p1_data.get('Pos', 'N/A')}")
                st.write(f"**Nationalité:** {p1_data.get('Nation', 'N/A')}")
            
            with col2:
                st.subheader(f"👤 {player2}")
                st.write(f"**Équipe:** {p2_data.get('Squad', 'N/A')}")
                st.write(f"**Âge:** {p2_data.get('Age', 'N/A')}")
                st.write(f"**Position:** {p2_data.get('Pos', 'N/A')}")
                st.write(f"**Nationalité:** {p2_data.get('Nation', 'N/A')}")
            
            stats_to_compare = ['Gls', 'Ast', 'Min', 'Starts']
            available_stats = [stat for stat in stats_to_compare if stat in df.columns]
            
            if available_stats:
                st.subheader("📊 Comparaison des Statistiques")
                
                comparison_data = {
                    'Statistique': available_stats,
                    player1: [p1_data.get(stat, 0) for stat in available_stats],
                    player2: [p2_data.get(stat, 0) for stat in available_stats]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                
                if len(available_stats) >= 3:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=comparison_df[player1].tolist(),
                        theta=comparison_df['Statistique'].tolist(),
                        fill='toself',
                        name=player1
                    ))
                    
                    fig.add_trace(go.Scatterpolar(
                        r=comparison_df[player2].tolist(),
                        theta=comparison_df['Statistique'].tolist(),
                        fill='toself',
                        name=player2
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, max(comparison_df[player1].max(), comparison_df[player2].max())]
                            )),
                        showlegend=True,
                        title="Radar Chart - Comparaison"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(comparison_df)

elif page == "📈 Analyses Avancées":
    st.header("Analyses Avancées")
    
    if 'players' in data:
        df = data['players']
        
        tab1, tab2, tab3 = st.tabs(["Corrélations", "Tendances par âge", "Performance par ligue"])
        
        with tab1:
            st.subheader("Matrice de Corrélation")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
                st.pyplot(fig)
        
        with tab2:
            if 'Age' in df.columns and 'Gls' in df.columns:
                st.subheader("Performance en fonction de l'âge")
                age_performance = df.groupby('Age').agg({
                    'Gls': 'mean',
                    'Ast': 'mean' if 'Ast' in df.columns else 'count'
                }).reset_index()
                
                fig = px.line(age_performance, x='Age', y='Gls', 
                            title="Moyenne de buts par âge")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            if 'Comp' in df.columns:
                st.subheader("Comparaison des ligues")
                league_stats = df.groupby('Comp').agg({
                    'Gls': 'mean',
                    'Ast': 'mean' if 'Ast' in df.columns else 'count',
                    'Player': 'count'
                }).reset_index()
                league_stats.rename(columns={'Player': 'Nombre_joueurs'}, inplace=True)
                
                fig = px.bar(league_stats, x='Comp', y='Gls',
                           title="Moyenne de buts par ligue")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(league_stats)

st.markdown("---")
st.markdown("**SoccerStats Dashboard** - Projet d'analyse de données sportives | Équipe: Fatima FALL, Alexandre COURTET, Victor SANSON")