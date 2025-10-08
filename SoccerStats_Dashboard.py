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
    data = {}
    data_dir = 'datas_cleaned'
    
    if not os.path.exists(data_dir):
        st.error(f"Le dossier {data_dir} n'existe pas. Veuillez d'abord exécuter le script de nettoyage.")
        return None
    
    files = {
        'players': 'top5-players.csv',
        'keepers': 'keepers.csv',
        'defensive': 'Defensive.csv',
        'passing': 'Passing.csv'
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(x=pos_counts.values, y=pos_counts.index, orientation='h',
                            title="Nombre de joueurs par poste",
                            color=pos_counts.values,
                            color_continuous_scale='viridis')
                fig.update_xaxis(title="Nombre de joueurs")
                fig.update_yaxis(title="Poste")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig_pie = px.pie(values=pos_counts.values, names=pos_counts.index,
                               title="Répartition en pourcentage par poste")
                fig_pie.update_layout(height=400)
                st.plotly_chart(fig_pie, use_container_width=True)

elif page == "⚽ Joueurs de Champ":
    st.header("Analyse des Joueurs de Champ")
    
    if 'players' in data:
        df = data['players']
        
        st.sidebar.subheader("Filtres")
        
        df_original = df.copy()
        
        if 'Comp' in df.columns:
            leagues = ['Toutes'] + sorted(df['Comp'].unique().tolist())
            selected_league = st.sidebar.selectbox("Ligue", leagues)
            if selected_league != 'Toutes':
                df = df[df['Comp'] == selected_league]
        
        if 'Pos' in df.columns:
            positions = ['Tous'] + sorted(df['Pos'].unique().tolist())
            selected_pos = st.sidebar.selectbox("Poste", positions)
            if selected_pos != 'Tous':
                df = df[df['Pos'] == selected_pos]
        
        if 'Age' in df.columns:
            age_range = st.sidebar.slider("Âge", 
                                        int(df_original['Age'].min()), 
                                        int(df_original['Age'].max()), 
                                        (int(df_original['Age'].min()), int(df_original['Age'].max())))
            df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
        
        if 'Min' in df.columns:
            min_minutes = st.sidebar.slider("Minutes minimales", 0, int(df_original['Min'].max()), 90)
            df = df[df['Min'] >= min_minutes]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Joueurs analysés", len(df))
        with col2:
            if 'Gls' in df.columns:
                st.metric("Total buts", int(df['Gls'].sum()))
        with col3:
            if 'Ast' in df.columns:
                st.metric("Total passes décisives", int(df['Ast'].sum()))
        with col4:
            if 'Min' in df.columns:
                st.metric("Minutes totales", f"{int(df['Min'].sum()):,}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Gls' in df.columns:
                st.subheader("🥅 Top 15 Buteurs")
                top_scorers = df.nlargest(15, 'Gls')[['Player', 'Gls', 'Squad']]
                if len(top_scorers) > 0 and top_scorers['Gls'].max() > 0:
                    fig = px.bar(top_scorers, x='Gls', y='Player', orientation='h',
                               hover_data=['Squad'], 
                               color='Gls',
                               color_continuous_scale='Reds',
                               title="🥅 Classement des meilleurs buteurs")
                    fig.update_layout(
                        height=600,
                        yaxis={'categoryorder':'total ascending'},
                        xaxis_title="Nombre de buts",
                        yaxis_title="Joueurs",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig.update_traces(
                        texttemplate='%{x}', 
                        textposition='outside',
                        textfont_size=12,
                        textfont_color='black'
                    )
                    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                    fig.update_yaxes(showgrid=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Aucune donnée de buts disponible avec les filtres actuels")
        
        with col2:
            if 'Ast' in df.columns:
                st.subheader("🎯 Top 15 Passeurs")
                top_assist = df.nlargest(15, 'Ast')[['Player', 'Ast', 'Squad']]
                if len(top_assist) > 0 and top_assist['Ast'].max() > 0:
                    fig = px.bar(top_assist, x='Ast', y='Player', orientation='h',
                               hover_data=['Squad'], 
                               color='Ast',
                               color_continuous_scale='Blues',
                               title="🎯 Classement des meilleurs passeurs")
                    fig.update_layout(
                        height=600,
                        yaxis={'categoryorder':'total ascending'},
                        xaxis_title="Passes décisives",
                        yaxis_title="Joueurs",
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig.update_traces(
                        texttemplate='%{x}', 
                        textposition='outside',
                        textfont_size=12,
                        textfont_color='black'
                    )
                    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                    fig.update_yaxes(showgrid=False)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Aucune donnée de passes décisives disponible avec les filtres actuels")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Gls' in df.columns and 'Ast' in df.columns:
                st.subheader("📈 Relation Buts vs Passes Décisives")
                df_filtered = df[(df['Gls'] > 0) | (df['Ast'] > 0)]
                if len(df_filtered) > 0:
                    fig = px.scatter(df_filtered, x='Gls', y='Ast', 
                                   hover_data=['Player', 'Squad'],
                                   color='Comp' if 'Comp' in df_filtered.columns else None,
                                   title="Corrélation entre buts et passes décisives",
                                   labels={'Gls': 'Buts', 'Ast': 'Passes décisives'})
                    
                    if len(df_filtered) > 1:
                        from scipy import stats
                        slope, intercept, r_value, p_value, std_err = stats.linregress(df_filtered['Gls'], df_filtered['Ast'])
                        line_x = np.linspace(df_filtered['Gls'].min(), df_filtered['Gls'].max(), 100)
                        line_y = slope * line_x + intercept
                        fig.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', 
                                               name=f'Tendance (R²={r_value**2:.2f})',
                                               line=dict(color='red', dash='dash')))
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Aucune donnée disponible pour cette analyse")
        
        with col2:
            if 'Gls' in df.columns and 'Min' in df.columns:
                st.subheader("⚡ Top 15 - Efficacité offensive")
                df_eff = df[df['Min'] >= 500].copy()
                if len(df_eff) > 0:
                    df_eff['Goals_per_90'] = (df_eff['Gls'] / df_eff['Min']) * 90
                    if 'Ast' in df_eff.columns:
                        df_eff['G+A_per_90'] = ((df_eff['Gls'] + df_eff['Ast']) / df_eff['Min']) * 90
                        top_efficiency = df_eff.nlargest(15, 'G+A_per_90')[['Player', 'G+A_per_90', 'Gls', 'Ast', 'Min']]
                        fig = px.bar(top_efficiency, x='G+A_per_90', y='Player', orientation='h',
                                   hover_data=['Gls', 'Ast', 'Min'],
                                   color='G+A_per_90',
                                   color_continuous_scale='viridis',
                                   title="Buts + Passes décisives par 90 minutes")
                        fig.update_layout(
                            height=600,
                            yaxis={'categoryorder':'total ascending'},
                            xaxis_title="(Buts + Passes) / 90min",
                            yaxis_title="Joueurs",
                            showlegend=False
                        )
                    else:
                        top_efficiency = df_eff.nlargest(15, 'Goals_per_90')[['Player', 'Goals_per_90', 'Gls', 'Min']]
                        fig = px.bar(top_efficiency, x='Goals_per_90', y='Player', orientation='h',
                                   hover_data=['Gls', 'Min'],
                                   color='Goals_per_90',
                                   color_continuous_scale='viridis',
                                   title="Buts par 90 minutes")
                        fig.update_layout(
                            height=600,
                            yaxis={'categoryorder':'total ascending'},
                            xaxis_title="Buts / 90min",
                            yaxis_title="Joueurs",
                            showlegend=False
                        )
                    
                    fig.update_traces(texttemplate='%{x:.2f}', textposition='outside')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Pas assez de données pour calculer l'efficacité (minimum 500 minutes)")
        
        st.markdown("---")
        st.subheader("📊 Analyses Avancées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Age' in df.columns and 'Gls' in df.columns:
                st.subheader("🎂 Performance par tranche d'âge")
                age_stats = df.groupby('Age').agg({
                    'Gls': ['mean', 'sum', 'count'],
                    'Player': 'count'
                }).round(2)
                age_stats.columns = ['Buts_moy', 'Buts_total', 'Joueurs_avec_buts', 'Total_joueurs']
                age_stats = age_stats.reset_index()
                age_stats = age_stats[age_stats['Total_joueurs'] >= 3]
                
                if len(age_stats) > 0:
                    fig = px.line(age_stats, x='Age', y='Buts_moy',
                                title="Moyenne de buts par âge",
                                labels={'Buts_moy': 'Buts moyens', 'Age': 'Âge'})
                    fig.add_bar(x=age_stats['Age'], y=age_stats['Total_joueurs'],
                              name='Nombre de joueurs', yaxis='y2', opacity=0.3)
                    fig.update_layout(
                        yaxis2=dict(title="Nombre de joueurs", overlaying='y', side='right'),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'Squad' in df.columns and 'Gls' in df.columns:
                st.subheader("🏆 Top 10 équipes (buts)")
                team_stats = df.groupby('Squad').agg({
                    'Gls': 'sum',
                    'Ast': 'sum' if 'Ast' in df.columns else 'count',
                    'Player': 'count'
                }).round(2)
                team_stats.columns = ['Total_buts', 'Total_passes', 'Nb_joueurs']
                team_stats = team_stats.reset_index()
                top_teams = team_stats.nlargest(10, 'Total_buts')
                
                if len(top_teams) > 0:
                    fig = px.bar(top_teams, x='Total_buts', y='Squad', orientation='h',
                               hover_data=['Total_passes', 'Nb_joueurs'],
                               color='Total_buts',
                               color_continuous_scale='oranges',
                               title="Équipes avec le plus de buts")
                    fig.update_layout(
                        height=400,
                        yaxis={'categoryorder':'total ascending'},
                        xaxis_title="Total buts",
                        yaxis_title="Équipes",
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📋 Tableau de synthèse des meilleurs joueurs")
        
        if len(df) > 0:
            summary_cols = ['Player', 'Squad', 'Age', 'Pos']
            if 'Gls' in df.columns:
                summary_cols.append('Gls')
            if 'Ast' in df.columns:
                summary_cols.append('Ast')
            if 'Min' in df.columns:
                summary_cols.append('Min')
            
            df_summary = df[summary_cols].copy()
            if 'Gls' in df.columns and 'Min' in df.columns:
                df_summary['Buts/90min'] = ((df['Gls'] / df['Min']) * 90).round(3)
            if 'Ast' in df.columns and 'Min' in df.columns:
                df_summary['Passes/90min'] = ((df['Ast'] / df['Min']) * 90).round(3)
            
            if 'Gls' in df_summary.columns:
                df_summary = df_summary.sort_values('Gls', ascending=False)
            
            st.dataframe(df_summary.head(20), use_container_width=True)

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
                df_qualified = df[df['Saves'] > 20]
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
                df_qualified = df[df['Min'] > 900]
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
        
        st.sidebar.subheader("Filtres de Comparaison")
        
        if 'Pos' in df.columns:
            positions = ['Tous les postes'] + sorted(df['Pos'].unique().tolist())
            selected_position = st.sidebar.selectbox("Filtrer par poste", positions)
            
            if selected_position != 'Tous les postes':
                df_filtered = df[df['Pos'] == selected_position]
                st.info(f"Comparaison limitée aux joueurs du poste: **{selected_position}**")
            else:
                df_filtered = df
        else:
            df_filtered = df
        
        players_list = sorted(df_filtered['Player'].unique().tolist())
        
        if len(players_list) < 2:
            st.warning("Pas assez de joueurs disponibles pour la comparaison avec les filtres actuels.")
            st.stop()
        
        col1, col2 = st.columns(2)
        
        with col1:
            player1 = st.selectbox("Joueur 1", players_list, key="player1")
        with col2:
            available_players2 = [p for p in players_list if p != player1]
            player2 = st.selectbox("Joueur 2", available_players2, key="player2")
        
        if player1 and player2 and player1 != player2:
            p1_data = df_filtered[df_filtered['Player'] == player1].iloc[0]
            p2_data = df_filtered[df_filtered['Player'] == player2].iloc[0]
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.subheader(f"👤 {player1}")
                st.write(f"**Équipe:** {p1_data.get('Squad', 'N/A')}")
                st.write(f"**Âge:** {p1_data.get('Age', 'N/A')}")
                st.write(f"**Position:** {p1_data.get('Pos', 'N/A')}")
                st.write(f"**Nationalité:** {p1_data.get('Nation', 'N/A')}")
                if 'Comp' in p1_data:
                    st.write(f"**Ligue:** {p1_data.get('Comp', 'N/A')}")
            
            with col2:
                st.subheader(f"👤 {player2}")
                st.write(f"**Équipe:** {p2_data.get('Squad', 'N/A')}")
                st.write(f"**Âge:** {p2_data.get('Age', 'N/A')}")
                st.write(f"**Position:** {p2_data.get('Pos', 'N/A')}")
                st.write(f"**Nationalité:** {p2_data.get('Nation', 'N/A')}")
                if 'Comp' in p2_data:
                    st.write(f"**Ligue:** {p2_data.get('Comp', 'N/A')}")
            
            with col3:
                st.subheader("🎯 Analyse")
                if p1_data.get('Pos') == p2_data.get('Pos'):
                    st.success(f"✅ Même poste: {p1_data.get('Pos', 'N/A')}")
                else:
                    st.warning(f"⚠️ Postes différents:\n{p1_data.get('Pos', 'N/A')} vs {p2_data.get('Pos', 'N/A')}")
                
                age_diff = abs(p1_data.get('Age', 0) - p2_data.get('Age', 0))
                st.info(f"📅 Différence d'âge: {age_diff} ans")
                
                if p1_data.get('Comp') == p2_data.get('Comp'):
                    st.success(f"🏆 Même ligue: {p1_data.get('Comp', 'N/A')}")
                else:
                    st.info(f"🌍 Ligues différentes")
            
            stats_to_compare = ['Gls', 'Ast', 'Min', 'Starts']
            if 'Pos' in df_filtered.columns and p1_data.get('Pos') in ['GK']:
                stats_to_compare = ['Saves', 'CS', 'GA', 'Min'] if all(col in df_filtered.columns for col in ['Saves', 'CS', 'GA']) else stats_to_compare
            
            available_stats = [stat for stat in stats_to_compare if stat in df_filtered.columns]
            
            if available_stats:
                st.markdown("---")
                st.subheader("📊 Comparaison des Statistiques")
                
                comparison_data = {
                    'Statistique': available_stats,
                    player1: [p1_data.get(stat, 0) for stat in available_stats],
                    player2: [p2_data.get(stat, 0) for stat in available_stats]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if len(available_stats) >= 3:
                        max_val = max(comparison_df[player1].max(), comparison_df[player2].max())
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatterpolar(
                            r=comparison_df[player1].tolist(),
                            theta=comparison_df['Statistique'].tolist(),
                            fill='toself',
                            name=player1,
                            line_color='rgb(46, 125, 50)',
                            fillcolor='rgba(46, 125, 50, 0.3)'
                        ))
                        
                        fig.add_trace(go.Scatterpolar(
                            r=comparison_df[player2].tolist(),
                            theta=comparison_df['Statistique'].tolist(),
                            fill='toself',
                            name=player2,
                            line_color='rgb(211, 47, 47)',
                            fillcolor='rgba(211, 47, 47, 0.3)'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, max_val * 1.1],
                                    showticklabels=True,
                                    gridcolor='lightgray'
                                ),
                                angularaxis=dict(
                                    showticklabels=True,
                                    gridcolor='lightgray'
                                )
                            ),
                            showlegend=True,
                            title=f"Radar Chart - {player1} vs {player2}",
                            height=500,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Pas assez de statistiques pour créer un radar chart")
                
                with col2:
                    st.subheader("📈 Tableau comparatif")
                    comparison_display = comparison_df.copy()
                    for stat in available_stats:
                        val1 = comparison_display.loc[comparison_display['Statistique'] == stat, player1].iloc[0]
                        val2 = comparison_display.loc[comparison_display['Statistique'] == stat, player2].iloc[0]
                        
                        if val1 > val2:
                            comparison_display.loc[comparison_display['Statistique'] == stat, player1] = f"🟢 {val1}"
                            comparison_display.loc[comparison_display['Statistique'] == stat, player2] = f"🔴 {val2}"
                        elif val2 > val1:
                            comparison_display.loc[comparison_display['Statistique'] == stat, player1] = f"🔴 {val1}"
                            comparison_display.loc[comparison_display['Statistique'] == stat, player2] = f"🟢 {val2}"
                        else:
                            comparison_display.loc[comparison_display['Statistique'] == stat, player1] = f"🟡 {val1}"
                            comparison_display.loc[comparison_display['Statistique'] == stat, player2] = f"🟡 {val2}"
                    
                    st.dataframe(comparison_display, hide_index=True, use_container_width=True)
                
                if 'Min' in available_stats and comparison_df.loc[comparison_df['Statistique'] == 'Min', player1].iloc[0] > 0 and comparison_df.loc[comparison_df['Statistique'] == 'Min', player2].iloc[0] > 0:
                    st.markdown("---")
                    st.subheader("⚡ Statistiques par 90 minutes")
                    
                    per_90_data = []
                    minutes_p1 = p1_data.get('Min', 1)
                    minutes_p2 = p2_data.get('Min', 1)
                    
                    for stat in ['Gls', 'Ast']:
                        if stat in available_stats:
                            val_p1_90 = (p1_data.get(stat, 0) / minutes_p1) * 90
                            val_p2_90 = (p2_data.get(stat, 0) / minutes_p2) * 90
                            per_90_data.append({
                                'Statistique': f"{stat}/90min",
                                player1: round(val_p1_90, 2),
                                player2: round(val_p2_90, 2)
                            })
                    
                    if per_90_data:
                        per_90_df = pd.DataFrame(per_90_data)
                        st.dataframe(per_90_df, hide_index=True, use_container_width=True)
        
        else:
            st.info("Sélectionnez deux joueurs différents pour commencer la comparaison.")
    
    else:
        st.error("❌ Données des joueurs non disponibles")
        st.info("Vérifiez que le fichier 'top5-players.csv' existe dans le dossier 'datas_cleaned'")

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