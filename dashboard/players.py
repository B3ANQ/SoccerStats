import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def show_players():
    """Fonction principale pour afficher la page des joueurs"""

def get_club_logo(club_name):
    """Retourne le chemin vers le logo du club."""
    import os
    
    club_mapping = {
        # Premier League
        "Arsenal": "premier_league/Arsenal.png",
        "Chelsea": "premier_league/Chelsea.png",
        "Liverpool": "premier_league/Liverpool.png",
        "Manchester City": "premier_league/Man City.png",
        "Manchester United": "premier_league/Man United.png",
        "Tottenham": "premier_league/Tottenham.png",
        "Newcastle": "premier_league/Newcastle.png",
        "Brighton": "premier_league/Brighton.png",
        "West Ham": "premier_league/West Ham.png",
        "Aston Villa": "premier_league/Aston Villa.png",
        "Fulham": "premier_league/Fulham.png",
        "Brentford": "premier_league/Brentford.png",
        "Crystal Palace": "premier_league/Crystal Palace.png",
        "Bournemouth": "premier_league/Bournemouth.png",
        "Wolves": "premier_league/Wolverhampton.png",
        "Everton": "premier_league/Everton.png",
        "Nottingham Forest": "premier_league/Nottingham.png",
        "Sheffield United": "premier_league/Sheff Utd.png",
        "Burnley": "premier_league/Burnley.png",
        "Luton Town": "premier_league/Luton.png",
        
        # La Liga
        "Real Madrid": "liga/Real Madrid.png",
        "Barcelona": "liga/Barcelone.png",
        "Atlético Madrid": "liga/Atlético.png",
        "Athletic Club": "liga/Bilbao.png",
        "Real Sociedad": "liga/Real Sociedad.png",
        "Betis": "liga/Betis.png",
        "Villarreal": "liga/Villarreal.png",
        "Valencia": "liga/Valence.png",
        "Sevilla": "liga/Séville.png",
        "Girona": "liga/Girona.png",
        "Las Palmas": "liga/Las Palmas.png",
        "Getafe": "liga/Getafe.png",
        "Osasuna": "liga/Osasuna.png",
        "Celta Vigo": "liga/Celta Vigo.png",
        "Rayo Vallecano": "liga/Vallecano.png",
        "Cádiz": "liga/Cadix.png",
        "Mallorca": "liga/Majorque.png",
        "Almería": "liga/Almería.png",
        "Granada": "liga/Grenade.png",
        "Alavés": "liga/Alavés.png",
        
        # Bundesliga
        "Bayern Munich": "bundesliga/Bayern Munich.png",
        "Dortmund": "bundesliga/Dortmund.png",
        "RB Leipzig": "bundesliga/Leipzig.png",
        "Bayer Leverkusen": "bundesliga/Leverkusen.png",
        "Eintracht Frankfurt": "bundesliga/Francfort.png",
        "VfB Stuttgart": "bundesliga/Stuttgart.png",
        "Freiburg": "bundesliga/Fribourg.png",
        "Union Berlin": "bundesliga/Union Berlin.png",
        "Werder Bremen": "bundesliga/Brême.png",
        "Borussia Mönchengladbach": "bundesliga/M_gladbach.png",
        "VfL Wolfsburg": "bundesliga/Wolfsbourg.png",
        "Mainz 05": "bundesliga/Mayence.png",
        "FC Köln": "bundesliga/Cologne.png",
        "Hoffenheim": "bundesliga/Hoffenheim.png",
        "FC Augsburg": "bundesliga/Augsbourg.png",
        "VfL Bochum": "bundesliga/Bochum.png",
        "Heidenheim": "bundesliga/Heidenheim.png",
        "Darmstadt": "bundesliga/Darmstadt.png",
        
        # Serie A
        "Juventus": "serie_a/Juventus.png",
        "Inter": "serie_a/Inter Milan.png",
        "AC Milan": "serie_a/Milan.png",
        "Napoli": "serie_a/Naples.png",
        "Roma": "serie_a/Rome.png",
        "Lazio": "serie_a/Lazio.png",
        "Atalanta": "serie_a/Atalanta.png",
        "Fiorentina": "serie_a/Fiorentina.png",
        "Torino": "serie_a/Torino.png",
        "Bologna": "serie_a/Bologne.png",
        "Sassuolo": "serie_a/Sassuolo.png",
        "Monza": "serie_a/Monza.png",
        "Udinese": "serie_a/Udinese.png",
        "Genoa": "serie_a/Genoa.png",
        "Lecce": "serie_a/Lecce.png",
        "Empoli": "serie_a/Empoli.png",
        "Cagliari": "serie_a/Cagliari.png",
        "Hellas Verona": "serie_a/Hellas.png",
        "Salernitana": "serie_a/Salernitana.png",
        "Frosinone": "serie_a/Frosinone.png",
        
        # Ligue 1
        "Paris S-G": "ligue_1/PSG.png",
        "Marseille": "ligue_1/Marseille.png",
        "Monaco": "ligue_1/Monaco.png",
        "Lyon": "ligue_1/Lyon.png",
        "Lille": "ligue_1/Lille.png",
        "Nice": "ligue_1/Nice.png",
        "Rennes": "ligue_1/Rennes.png",
        "Lens": "ligue_1/Lens.png",
        "Nantes": "ligue_1/Nantes.png",
        "Strasbourg": "ligue_1/Strasbourg.png",
        "Montpellier": "ligue_1/Montpellier.png",
        "Reims": "ligue_1/Reims.png",
        "Toulouse": "ligue_1/Toulouse.png",
        "Brest": "ligue_1/Brest.png",
        "Le Havre": "ligue_1/Le Havre.png",
        "Lorient": "ligue_1/Lorient.png",
        "Metz": "ligue_1/Metz.png",
        "Clermont": "ligue_1/Clermont.png"
    }
    
    logo_path = club_mapping.get(club_name)
    if logo_path:
        full_path = f"logos/{logo_path}"
        if os.path.exists(full_path):
            return full_path
    return None

def get_league_logo(league_name):
    """Retourne le chemin vers le logo de la ligue."""
    import os
    
    league_mapping = {
        "Premier League": "logos/PL.png",
        "La Liga": "logos/Liga.png",
        "Bundesliga": "logos/Bundesliga.png",
        "Serie A": "logos/Serie_A.png",
        "Ligue 1": "logos/L1.png"
    }
    
    logo_path = league_mapping.get(league_name)
    if logo_path and os.path.exists(logo_path):
        return logo_path
    return None

def get_country_flag(country_name):
    """Retourne l'emoji du drapeau du pays."""
    country_flags = {
        "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Spain": "🇪🇸", "Germany": "🇩🇪", "Italy": "🇮🇹", "France": "🇫🇷",
        "Brazil": "🇧🇷", "Argentina": "🇦🇷", "Portugal": "🇵🇹", "Netherlands": "🇳🇱", "Belgium": "🇧🇪",
        "Croatia": "🇭🇷", "Morocco": "🇲🇦", "Serbia": "🇷🇸", "Poland": "🇵🇱", "Ukraine": "🇺🇦",
        "Denmark": "🇩🇰", "Sweden": "🇸🇪", "Norway": "🇳🇴", "Austria": "🇦🇹", "Switzerland": "🇨🇭",
        "Czech Republic": "🇨🇿", "Slovakia": "🇸🇰", "Hungary": "🇭🇺", "Slovenia": "🇸🇮", "Finland": "🇫🇮",
        "Iceland": "🇮🇸", "Ireland": "🇮🇪", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Northern Ireland": "🏴󠁧󠁢󠁮󠁩󠁲󠁿",
        "Turkey": "🇹🇷", "Greece": "🇬🇷", "Bulgaria": "🇧🇬", "Romania": "🇷🇴", "Russia": "🇷🇺",
        "Japan": "🇯🇵", "South Korea": "🇰🇷", "Australia": "🇦🇺", "United States": "🇺🇸", "Canada": "🇨🇦",
        "Mexico": "🇲🇽", "Colombia": "🇨🇴", "Uruguay": "🇺🇾", "Chile": "🇨🇱", "Peru": "🇵🇪",
        "Ecuador": "🇪🇨", "Venezuela": "🇻🇪", "Paraguay": "🇵🇾", "Bolivia": "🇧🇴", "Costa Rica": "🇨🇷",
        "Nigeria": "🇳🇬", "Ghana": "🇬🇭", "Senegal": "🇸🇳", "Algeria": "🇩🇿", "Tunisia": "🇹🇳",
        "Egypt": "🇪🇬", "Cameroon": "🇨🇲", "Ivory Coast": "🇨🇮", "Mali": "🇲🇱", "Burkina Faso": "🇧🇫"
    }
    return country_flags.get(country_name, "🌍")

@st.cache_data
def load_data():
    top5_players = pd.read_csv('datas_cleaned/top5-players.csv')
    defensive = pd.read_csv('datas_cleaned/Defensive.csv')
    passing = pd.read_csv('datas_cleaned/Passing.csv')
    keepers = pd.read_csv('datas_cleaned/keepers.csv')
    players_positions = pd.read_csv('datas_cleaned/players_positions.csv')
    premier_league_positions = pd.read_csv('datas_cleaned/premier_league_players_positions.csv')
    bundesliga_positions = pd.read_csv('datas_cleaned/bundesliga_players_positions.csv')
    liga_positions = pd.read_csv('datas_cleaned/liga_players_positions.csv')
    ligue_1_positions = pd.read_csv('datas_cleaned/ligue_1_players_positions.csv')
    serie_a_positions = pd.read_csv('datas_cleaned/serie_a_players_positions.csv')
    
    all_positions = pd.concat([
        players_positions,
        premier_league_positions,
        bundesliga_positions,
        liga_positions,
        ligue_1_positions,
        serie_a_positions
    ], ignore_index=True).drop_duplicates(subset=['Name'])
    
    defensive = defensive.rename(columns={'Col_1': 'Player'})
    passing = passing.rename(columns={'Col_1': 'Player'})
    keepers = keepers.rename(columns={
        'Col_1': 'Player', 
        'Col_2': 'Nation', 
        'Col_4': 'Squad', 
        'Col_5': 'Comp', 
        'Col_6': 'Age',
        'Playing Time.2': 'Min',
        'Performance': 'GA',
        'Performance.1': 'GA90',
        'Performance.2': 'SoTA',
        'Performance.3': 'Saves',
        'Performance.4': 'Save%',
        'Performance.5': 'W',
        'Performance.6': 'D',
        'Performance.7': 'L',
        'Performance.8': 'CS',
        'Performance.9': 'CS%',
        'Playing Time': 'MP',
        'Playing Time.1': 'Starts'
    })
    
    return top5_players, defensive, passing, keepers, all_positions

def get_player_stats(player_name, top5_df, defensive_df, passing_df, keepers_df, positions_df):
    player_data = {}
    
    if 'Player' in keepers_df.columns:
        keepers_match = keepers_df[keepers_df['Player'] == player_name]
        if not keepers_match.empty:
            player_data['goalkeeper'] = keepers_match.iloc[0]
            return player_data
    
    top5_match = top5_df[top5_df['Player'] == player_name]
    defensive_match = defensive_df[defensive_df['Player'] == player_name]
    passing_match = passing_df[passing_df['Player'] == player_name]
    position_match = positions_df[positions_df['Name'] == player_name]
    
    if not top5_match.empty:
        player_stats = top5_match.iloc[0].to_dict()
        
        if not position_match.empty:
            player_stats['Detailed_Position'] = position_match.iloc[0]['Position']
        
        if not defensive_match.empty:
            defensive_stats = defensive_match.iloc[0].to_dict()
            for key, value in defensive_stats.items():
                if key not in player_stats or pd.isna(player_stats.get(key)):
                    player_stats[f"def_{key}"] = value
        
        if not passing_match.empty:
            passing_stats = passing_match.iloc[0].to_dict()
            for key, value in passing_stats.items():
                if key not in player_stats or pd.isna(player_stats.get(key)):
                    player_stats[f"pass_{key}"] = value
        
        player_data['general'] = pd.Series(player_stats)
    
    return player_data

def display_player_info(player_data):
    if 'general' in player_data:
        info = player_data['general']
        
        # Récupérer les logos
        club_logo = get_club_logo(info.get('Squad', ''))
        league_logo = get_league_logo(info.get('Comp', ''))
        country_flag = get_country_flag(info.get('Nation', ''))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{info.get('Age', 'N/A')}")
            nation_display = f"{country_flag} {info.get('Nation', 'N/A')}" if country_flag else info.get('Nation', 'N/A')
            st.metric("Nation", nation_display)
        
        with col2:
            detailed_pos = info.get('Detailed_Position', info.get('Pos', 'N/A'))
            base_pos = info.get('Pos', 'N/A')
            if detailed_pos != base_pos and pd.notna(detailed_pos):
                st.metric("Position", f"{detailed_pos} ({base_pos})")
            else:
                st.metric("Position", base_pos)
            
            # Affichage du club avec logo
            squad_name = info.get('Squad', 'N/A')
            if club_logo:
                col_logo, col_text = st.columns([1, 3])
                with col_logo:
                    st.image(club_logo, width=30)
                with col_text:
                    st.write(f"**Squad:** {squad_name}")
            else:
                st.metric("Squad", squad_name)
        
        with col3:
            # Affichage de la compétition avec logo
            comp_name = info.get('Comp', 'N/A')
            if league_logo:
                col_logo, col_text = st.columns([1, 3])
                with col_logo:
                    st.image(league_logo, width=30)
                with col_text:
                    st.write(f"**Competition:** {comp_name}")
            else:
                st.metric("Competition", comp_name)
            st.metric("Minutes Played", f"{info.get('Min', 0)}")
        
        with col4:
            st.metric("Goals", f"{info.get('Gls', 0)}")
            st.metric("Assists", f"{info.get('Ast', 0)}")
    
    elif 'goalkeeper' in player_data:
        info = player_data['goalkeeper']
        
        # Récupérer les logos pour les gardiens
        club_logo = get_club_logo(info.get('Squad', ''))
        league_logo = get_league_logo(info.get('Comp', ''))
        country_flag = get_country_flag(info.get('Nation', ''))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{info.get('Age', 'N/A')}")
            nation_display = f"{country_flag} {info.get('Nation', 'N/A')}" if country_flag else info.get('Nation', 'N/A')
            st.metric("Nation", nation_display)
        
        with col2:
            st.metric("Position", "🥅 GK")
            # Affichage du club avec logo
            squad_name = info.get('Squad', 'N/A')
            if club_logo:
                col_logo, col_text = st.columns([1, 3])
                with col_logo:
                    st.image(club_logo, width=30)
                with col_text:
                    st.write(f"**Squad:** {squad_name}")
            else:
                st.metric("Squad", squad_name)
        
        with col3:
            # Affichage de la compétition avec logo
            comp_name = info.get('Comp', 'N/A')
            if league_logo:
                col_logo, col_text = st.columns([1, 3])
                with col_logo:
                    st.image(league_logo, width=30)
                with col_text:
                    st.write(f"**Competition:** {comp_name}")
            else:
                st.metric("Competition", comp_name)
            st.metric("Minutes Played", f"{info.get('Min', 0)}")
        
        with col4:
            st.metric("Saves", f"{info.get('Saves', 0)}")
            st.metric("Save %", f"{info.get('Save%', 0)}%")

def create_fifa_style_radar(player_data, player_name):
    fig = go.Figure()
    
    if 'general' in player_data:
        info = player_data['general']
        position = info.get('Detailed_Position', info.get('Pos', 'Unknown'))
        
        def safe_get(key, default=0, multiplier=1):
            value = info.get(key, default)
            try:
                return float(value) * multiplier if pd.notna(value) else default
            except (ValueError, TypeError):
                return default
        
        if position in ['BU', 'AG', 'AD', 'MOG', 'MOD']:
            stats = {
                'Pace': min(100, (safe_get('PrgR', 0, 3) + safe_get('PrgC', 0, 2)) / 2),
                'Shooting': min(100, safe_get('Gls_90', 0, 25) + safe_get('xG_90', 0, 20) + safe_get('G+A_90', 0, 15)),
                'Passing': min(100, (safe_get('Ast_90', 0, 30) + safe_get('pass_Cmp%', 0, 0.6) + safe_get('pass_xA', 0, 20)) / 2),
                'Dribbling': min(100, safe_get('PrgR', 0, 4) + safe_get('PrgC', 0, 3) + safe_get('pass_KP', 0, 3)),
                'Defending': min(100, (safe_get('def_Tkl', 0, 1) + safe_get('def_Int', 0, 1)) / 2),
                'Physical': min(100, (safe_get('Min', 0, 0.04) + safe_get('90s', 0, 6) + (12 - safe_get('CrdY', 0))) / 3)
            }
        elif position in ['MDC', 'MC', 'MOC', 'MG', 'MD']:
            stats = {
                'Pace': min(100, (safe_get('PrgR', 0, 2) + safe_get('PrgC', 0, 2.5)) / 2),
                'Shooting': min(100, safe_get('Gls_90', 0, 20) + safe_get('xG_90', 0, 15) + safe_get('G+A_90', 0, 10)),
                'Passing': min(100, (safe_get('Ast_90', 0, 25) + safe_get('pass_Cmp%', 0, 0.9) + safe_get('pass_xA', 0, 15) + safe_get('pass_PrgP', 0, 1)) / 3),
                'Dribbling': min(100, safe_get('PrgR', 0, 3) + safe_get('PrgC', 0, 2) + safe_get('pass_KP', 0, 2)),
                'Defending': min(100, (safe_get('def_Tkl', 0, 2.5) + safe_get('def_Int', 0, 2.5) + safe_get('def_Blocks', 0, 4)) / 2),
                'Physical': min(100, (safe_get('Min', 0, 0.03) + safe_get('90s', 0, 5) + (10 - safe_get('CrdY', 0))) / 2)
            }
        elif position in ['DG', 'DD', 'DC', 'DL', 'DR']:
            stats = {
                'Pace': min(100, (safe_get('PrgR', 0, 1.5) + safe_get('PrgC', 0, 2)) / 2),
                'Shooting': min(100, safe_get('Gls_90', 0, 15) + safe_get('xG_90', 0, 10)),
                'Passing': min(100, (safe_get('Ast_90', 0, 20) + safe_get('pass_Cmp%', 0, 1) + safe_get('pass_PrgP', 0, 1.5)) / 2),
                'Dribbling': min(100, safe_get('PrgR', 0, 2) + safe_get('PrgC', 0, 1.5)),
                'Defending': min(100, (safe_get('def_Tkl', 0, 3) + safe_get('def_Int', 0, 3) + safe_get('def_Blocks', 0, 4) + safe_get('def_Clr', 0, 1)) / 3),
                'Physical': min(100, (safe_get('Min', 0, 0.03) + safe_get('90s', 0, 5) + (12 - safe_get('CrdY', 0))) / 2)
            }
        else:
            stats = {
                'Pace': min(100, (safe_get('PrgR', 0, 2) + safe_get('PrgC', 0, 2)) / 2),
                'Shooting': min(100, safe_get('Gls_90', 0, 20) + safe_get('xG_90', 0, 15) + safe_get('G+A_90', 0, 10)),
                'Passing': min(100, (safe_get('Ast_90', 0, 25) + safe_get('pass_Cmp%', 0, 0.8) + safe_get('pass_xA', 0, 15)) / 2),
                'Dribbling': min(100, safe_get('PrgR', 0, 3) + safe_get('PrgC', 0, 2) + safe_get('pass_KP', 0, 2)),
                'Defending': min(100, (safe_get('def_Tkl', 0, 2) + safe_get('def_Int', 0, 2) + safe_get('def_Blocks', 0, 3)) / 2),
                'Physical': min(100, (safe_get('Min', 0, 0.03) + safe_get('90s', 0, 5) + (10 - safe_get('CrdY', 0))) / 2)
            }
        
        categories = list(stats.keys())
        values = list(stats.values())
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_name,
            line_color='rgb(0, 150, 136)',
            fillcolor='rgba(0, 150, 136, 0.3)'
        ))
        
    elif 'goalkeeper' in player_data:
        info = player_data['goalkeeper']
        
        def safe_float(value, default=0):
            try:
                if pd.notna(value) and str(value) != 'Unknown':
                    return float(value)
                return default
            except (ValueError, TypeError):
                return default
        
        save_pct = safe_float(info.get('Save%', 0))
        ga90 = safe_float(info.get('GA90', 0))
        cs_pct = safe_float(info.get('CS%', 0))
        
        stats = {
            'Diving': min(100, save_pct * 1.2),
            'Handling': min(100, max(0, 100 - ga90 * 30)),
            'Kicking': min(100, 70),
            'Reflexes': min(100, save_pct * 1.3),
            'Speed': min(100, 60),
            'Positioning': min(100, cs_pct * 2)
        }
        
        categories = list(stats.keys())
        values = list(stats.values())
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_name,
            line_color='rgb(255, 87, 34)',
            fillcolor='rgba(255, 87, 34, 0.3)'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(128, 128, 128, 0.3)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='white')
            ),
            bgcolor='rgba(0, 0, 0, 0.8)'
        ),
        showlegend=False,
        height=400,
        title=dict(
            text=f"{player_name} - FIFA Style Stats",
            x=0.5,
            font=dict(size=16, color='white')
        ),
        paper_bgcolor='rgba(0, 0, 0, 0.9)',
        plot_bgcolor='rgba(0, 0, 0, 0.9)',
        font=dict(color='white')
    )
    
    return fig

def create_comparison_radar(players_data):
    fig = go.Figure()
    
    colors = ['#00BFA5', '#FF5722', '#9C27B0', '#2196F3', '#FF9800']
    fill_colors = ['rgba(0, 191, 165, 0.15)', 'rgba(255, 87, 34, 0.15)', 'rgba(156, 39, 176, 0.15)', 'rgba(33, 150, 243, 0.15)', 'rgba(255, 152, 0, 0.15)']
    all_values = []
    
    for i, (player_name, data) in enumerate(players_data.items()):
        if 'general' in data:
            info = data['general']
            
            def safe_get_comp(key, default=0):
                value = info.get(key, default)
                try:
                    return float(value) if pd.notna(value) else default
                except (ValueError, TypeError):
                    return default
            
            stats = {
                'Goals/90': round(safe_get_comp('Gls_90', 0), 2),
                'Assists/90': round(safe_get_comp('Ast_90', 0), 2),
                'xG/90': round(safe_get_comp('xG_90', 0), 2),
                'xA/90': round(safe_get_comp('xAG_90', 0), 2),
                'Progressive Actions': round((safe_get_comp('PrgC', 0) + safe_get_comp('PrgP', 0)) / 20, 2),
                'Tackles': round(safe_get_comp('def_Tkl', 0) / 5, 2),
                'Interceptions': round(safe_get_comp('def_Int', 0) / 5, 2),
                'Pass Completion%': round(safe_get_comp('pass_Cmp%', 0) / 10, 2),
                'Key Passes': round(safe_get_comp('pass_KP', 0) / 5, 2),
                'Blocks': round(safe_get_comp('def_Blocks', 0) / 3, 2)
            }
            
        elif 'goalkeeper' in data:
            info = data['goalkeeper']
            
            def safe_float_comp(value, default=0):
                try:
                    if pd.notna(value) and str(value) != 'Unknown':
                        return float(value)
                    return default
                except (ValueError, TypeError):
                    return default
            
            save_pct = safe_float_comp(info.get('Save%', 0))
            ga90 = safe_float_comp(info.get('GA90', 0))
            cs_pct = safe_float_comp(info.get('CS%', 0))
            
            stats = {
                'Save%': round(save_pct, 2),
                'CS%': round(cs_pct, 2),
                'GA Prevention': round(max(0, 3 - ga90), 2),
                'Matches': round(safe_float_comp(info.get('MP', 0)), 2),
                'Saves': round(safe_float_comp(info.get('Saves', 0)) / 10, 2),
                'Wins': round(safe_float_comp(info.get('W', 0)), 2)
            }
        else:
            continue
        
        categories = list(stats.keys())
        values = list(stats.values())
        all_values.extend(values)
        
        color = colors[i % len(colors)]
        fill_color = fill_colors[i % len(fill_colors)]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=player_name,
            line=dict(color=color, width=3),
            fillcolor=fill_color,
            marker=dict(size=8, color=color),
            hovertemplate='<b>%{fullData.name}</b><br>%{theta}: %{r}<extra></extra>'
        ))
    
    max_val = max(all_values) if all_values else 1
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val * 1.2],
                gridcolor='rgba(255, 255, 255, 0.2)',
                linecolor='rgba(255, 255, 255, 0.3)',
                tickfont=dict(size=10, color='white'),
                showticklabels=True
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='white', family='Arial Black'),
                linecolor='rgba(255, 255, 255, 0.3)',
                gridcolor='rgba(255, 255, 255, 0.2)'
            ),
            bgcolor='rgba(0, 0, 0, 0.9)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='white')
        ),
        height=600,
        title=dict(
            text="📊 Advanced Player Comparison",
            x=0.5,
            font=dict(size=18, color='white', family='Arial Black')
        ),
        paper_bgcolor='rgba(20, 20, 20, 1)',
        plot_bgcolor='rgba(20, 20, 20, 1)',
        font=dict(color='white', family='Arial')
    )
    
    return fig

def show_players():
    """Fonction principale pour afficher la page des joueurs"""
    st.title("⚽ Soccer Stats Players Dashboard")
    
    top5_df, defensive_df, passing_df, keepers_df, positions_df = load_data()
    
    all_players_df = top5_df[['Player', 'Nation', 'Pos', 'Squad', 'Comp']].copy()
    
    all_players_df = all_players_df.merge(
        positions_df.rename(columns={'Name': 'Player', 'Position': 'Detailed_Position'}),
        on='Player', 
        how='left'
    )
    
    if 'Player' in keepers_df.columns:
        keepers_for_filter = keepers_df[['Player', 'Nation', 'Squad', 'Comp']].copy()
        keepers_for_filter['Pos'] = 'GK'
        keepers_for_filter['Detailed_Position'] = 'GK'
        all_players_df = pd.concat([all_players_df, keepers_for_filter], ignore_index=True)
    
    all_players_df = all_players_df.drop_duplicates(subset=['Player'])
    
    st.header("🔍 Advanced Filters")
    
    with st.expander("ℹ️ Position Guide"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**🎯 Attackers**")
            st.write("- **BU**: Buteur (Striker)")
            st.write("- **AG**: Ailier Gauche")
            st.write("- **AD**: Ailier Droit")
            st.write("- **MOG**: Milieu Offensif Gauche")
            st.write("- **MOD**: Milieu Offensif Droit")
        
        with col2:
            st.write("**⚡ Midfielders**")
            st.write("- **MDC**: Milieu Défensif Central")
            st.write("- **MC**: Milieu Central")
            st.write("- **MOC**: Milieu Offensif Central")
            st.write("- **MG**: Milieu Gauche")
            st.write("- **MD**: Milieu Droit")
        
        with col3:
            st.write("**🛡️ Defenders**")
            st.write("- **DG**: Défenseur Gauche")
            st.write("- **DD**: Défenseur Droit")
            st.write("- **DC**: Défenseur Central")
            st.write("- **DL**: Défenseur Latéral")
            st.write("- **DR**: Défenseur Relanceur")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leagues = ["all"] + sorted([league for league in all_players_df['Comp'].dropna().unique().tolist() if league != 'Comp'])
        selected_league = st.selectbox("🏆 League", leagues, index=0)
    
    with col2:
        detailed_positions = ["all"] + sorted([pos for pos in all_players_df['Detailed_Position'].dropna().unique().tolist() if pos not in ['Position', 'Unknown']])
        selected_detailed_position = st.selectbox("🎯 Detailed Position", detailed_positions, index=0)
    
    with col3:
        nations = ["all"] + sorted([nation for nation in all_players_df['Nation'].dropna().unique().tolist() if nation not in ['Nation', 'Unknown']])
        selected_nation = st.selectbox("🌍 Nationality", nations, index=0)
    
    filtered_df = all_players_df.copy()
    
    if selected_league != "all":
        filtered_df = filtered_df[filtered_df['Comp'] == selected_league]
    
    if selected_detailed_position != "all":
        filtered_df = filtered_df[filtered_df['Detailed_Position'] == selected_detailed_position]
    
    if selected_nation != "all":
        filtered_df = filtered_df[filtered_df['Nation'] == selected_nation]
    
    if not filtered_df.empty:
        player_names = filtered_df['Player'].tolist()
        
        st.header("👤 Player Selection")
        selected_player = st.selectbox("Select a player to analyze", [""] + player_names)
        
        if selected_player:
            player_data = get_player_stats(selected_player, top5_df, defensive_df, passing_df, keepers_df, positions_df)
            
            st.header(f"📊 {selected_player} - Player Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_player_info(player_data)
            
            with col2:
                st.plotly_chart(
                    create_fifa_style_radar(player_data, selected_player), 
                    config={'displayModeBar': True, 'displaylogo': False},
                    use_container_width=True
                )
            
            st.divider()
            
            if 'general' in player_data:
                info = player_data['general']
                
                def safe_display_get(key, default=0):
                    value = info.get(key, default)
                    try:
                        return float(value) if pd.notna(value) else default
                    except (ValueError, TypeError):
                        return default
                
                st.subheader("⚡ Performance Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Offensive Stats**")
                    perf_data = {
                        'Goals per 90': safe_display_get('Gls_90'),
                        'Assists per 90': safe_display_get('Ast_90'),
                        'xG per 90': safe_display_get('xG_90'),
                        'xA per 90': safe_display_get('xAG_90'),
                        'Key Passes': safe_display_get('pass_KP'),
                        'Goal+Assist per 90': safe_display_get('G+A_90')
                    }
                    st.bar_chart(perf_data)
                
                with col2:
                    st.write("**Defensive Stats**")
                    def_data = {
                        'Tackles': safe_display_get('def_Tkl'),
                        'Tackles Won': safe_display_get('def_TklW'),
                        'Interceptions': safe_display_get('def_Int'),
                        'Blocks': safe_display_get('def_Blocks'),
                        'Clearances': safe_display_get('def_Clr'),
                        'Errors': safe_display_get('def_Err')
                    }
                    st.bar_chart(def_data)
                
                with col3:
                    st.write("**Passing Stats**")
                    pass_data = {
                        'Pass Completion %': safe_display_get('pass_Cmp%'),
                        'Progressive Passes': safe_display_get('pass_PrgP'),
                        'Pass Distance': safe_display_get('pass_TotDist') / 100,
                        'Long Passes Completed': safe_display_get('pass_Long'),
                        'Crosses to Penalty Area': safe_display_get('pass_CrsPA'),
                        'Expected Assists': safe_display_get('pass_xA')
                    }
                    st.bar_chart(pass_data)
            
            elif 'goalkeeper' in player_data:
                info = player_data['goalkeeper']
                
                st.subheader("🥅 Goalkeeper Performance")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Performance Metrics**")
                    gk_perf_data = {}
                    
                    def safe_float_display(value, default=0):
                        try:
                            if pd.notna(value) and str(value) != 'Unknown':
                                return float(value)
                            return default
                        except (ValueError, TypeError):
                            return default
                    
                    ga90 = safe_float_display(info.get('GA90', 0))
                    save_pct = safe_float_display(info.get('Save%', 0))
                    saves = safe_float_display(info.get('Saves', 0))
                    
                    if ga90 > 0:
                        gk_perf_data['Goals Against per 90'] = ga90
                    if save_pct > 0:
                        gk_perf_data['Save %'] = save_pct
                    if saves > 0:
                        gk_perf_data['Total Saves'] = saves
                    
                    if gk_perf_data:
                        st.bar_chart(gk_perf_data)
                
                with col2:
                    st.write("**Match Statistics**")
                    match_data = {
                        'Matches Played': safe_float_display(info.get('MP', 0)),
                        'Starts': safe_float_display(info.get('Starts', 0)),
                        'Wins': safe_float_display(info.get('W', 0)),
                        'Clean Sheets': safe_float_display(info.get('CS', 0))
                    }
                    st.bar_chart(match_data)
        
        st.divider()
        st.header("⚖️ Advanced Player Comparison")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 Select Players to Compare")
            default_comparison = [selected_player] if selected_player else []
            
            comparison_players = st.multiselect(
                "Choose up to 3 players for detailed comparison", 
                player_names, 
                default=default_comparison,
                max_selections=3,
                help="Select multiple players to see their stats side by side"
            )
        
        with col2:
            if len(comparison_players) >= 2:
                st.success(f"✅ Comparing {len(comparison_players)} players")
                for i, player in enumerate(comparison_players, 1):
                    # Récupérer les infos du joueur pour afficher son club
                    player_stats = get_player_stats(player, top5_df, defensive_df, passing_df, keepers_df, positions_df)
                    if player_stats and ('general' in player_stats or 'goalkeeper' in player_stats):
                        info = player_stats.get('general', player_stats.get('goalkeeper', {}))
                        club_name = info.get('Squad', '')
                        club_logo = get_club_logo(club_name)
                        
                        if club_logo:
                            col_num, col_logo, col_text = st.columns([0.3, 0.7, 2])
                            with col_num:
                                st.write(f"**{i}.**")
                            with col_logo:
                                st.image(club_logo, width=20)
                            with col_text:
                                st.write(f"**{player}**")
                        else:
                            st.write(f"**{i}.** {player}")
                    else:
                        st.write(f"**{i}.** {player}")
            else:
                st.info("💡 Select at least 2 players to enable comparison")
        
        if len(comparison_players) > 1:
            players_data = {}
            for player in comparison_players:
                players_data[player] = get_player_stats(player, top5_df, defensive_df, passing_df, keepers_df, positions_df)
            
            st.subheader("📈 Interactive Comparison Chart")
            st.plotly_chart(
                create_comparison_radar(players_data), 
                config={'displayModeBar': True, 'displaylogo': False},
                use_container_width=True
            )
            
            st.subheader("📋 Detailed Stats Comparison")
            
            comparison_data = []
            
            for player in comparison_players:
                if player in players_data:
                    if 'general' in players_data[player]:
                        info = players_data[player]['general']
                        
                        def safe_table_get(key, default=0, round_digits=3):
                            value = info.get(key, default)
                            try:
                                val = float(value) if pd.notna(value) else default
                                return round(val, round_digits) if round_digits > 0 else int(val)
                            except (ValueError, TypeError):
                                return default
                        
                        detailed_pos = info.get('Detailed_Position', info.get('Pos', 'N/A'))
                        base_pos = info.get('Pos', 'N/A')
                        position_display = f"{detailed_pos}" if pd.notna(detailed_pos) and detailed_pos != 'N/A' else base_pos
                        
                        comparison_data.append({
                            'Player': player,
                            'Age': info.get('Age', 'N/A'),
                            'Position': position_display,
                            'Squad': info.get('Squad', 'N/A'),
                            'League': info.get('Comp', 'N/A'),
                            'Goals/90': safe_table_get('Gls_90'),
                            'Assists/90': safe_table_get('Ast_90'),
                            'xG/90': safe_table_get('xG_90'),
                            'xA/90': safe_table_get('xAG_90'),
                            'Tackles': safe_table_get('def_Tkl', 0, 0),
                            'Interceptions': safe_table_get('def_Int', 0, 0),
                            'Pass%': safe_table_get('pass_Cmp%', 0, 1),
                            'Key Passes': safe_table_get('pass_KP', 0, 0),
                            'Progressive': safe_table_get('PrgC', 0, 0),
                            'Minutes': safe_table_get('Min', 0, 0)
                        })
                    elif 'goalkeeper' in players_data[player]:
                        info = players_data[player]['goalkeeper']
                        
                        def safe_float_table(value, default=0):
                            try:
                                if pd.notna(value) and str(value) != 'Unknown':
                                    return float(value)
                                return default
                            except (ValueError, TypeError):
                                return default
                        
                        comparison_data.append({
                            'Player': player,
                            'Age': info.get('Age', 'N/A'),
                            'Position': 'GK',
                            'Squad': info.get('Squad', 'N/A'),
                            'League': info.get('Comp', 'N/A'),
                            'Matches': int(safe_float_table(info.get('MP', 0))),
                            'Clean Sheets': int(safe_float_table(info.get('CS', 0))),
                            'GA/90': round(safe_float_table(info.get('GA90', 0)), 2),
                            'Save%': round(safe_float_table(info.get('Save%', 0)), 1),
                            'CS%': round(safe_float_table(info.get('CS%', 0)), 1),
                            'Saves': int(safe_float_table(info.get('Saves', 0))),
                            'Minutes': int(safe_float_table(info.get('Min', 0)))
                        })
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                
                # Ajouter une section avec les logos avant le tableau
                st.write("### 🏆 Teams & Leagues")
                cols = st.columns(len(comparison_players))
                
                for i, player in enumerate(comparison_players):
                    if player in players_data:
                        if 'general' in players_data[player]:
                            info = players_data[player]['general']
                        elif 'goalkeeper' in players_data[player]:
                            info = players_data[player]['goalkeeper']
                        else:
                            continue
                        
                        with cols[i]:
                            st.write(f"**{player}**")
                            
                            # Logo du club
                            club_name = info.get('Squad', '')
                            club_logo = get_club_logo(club_name)
                            if club_logo:
                                col_logo, col_text = st.columns([1, 2])
                                with col_logo:
                                    st.image(club_logo, width=30)
                                with col_text:
                                    st.write(club_name)
                            else:
                                st.write(f"⚽ {club_name}")
                            
                            # Logo de la ligue
                            league_name = info.get('Comp', '')
                            league_logo = get_league_logo(league_name)
                            if league_logo:
                                col_logo, col_text = st.columns([1, 2])
                                with col_logo:
                                    st.image(league_logo, width=30)
                                with col_text:
                                    st.write(league_name)
                            else:
                                st.write(f"🏆 {league_name}")
                
                st.dataframe(
                    comparison_df, 
                    use_container_width=True,
                    column_config={
                        "Player": st.column_config.TextColumn("👤 Player", width="medium"),
                        "Squad": st.column_config.TextColumn("🏟️ Club", width="medium"),
                        "League": st.column_config.TextColumn("🏆 League", width="medium"),
                        "Goals/90": st.column_config.NumberColumn("⚽ Goals/90", format="%.3f"),
                        "Assists/90": st.column_config.NumberColumn("🎯 Assists/90", format="%.3f"),
                        "xG/90": st.column_config.NumberColumn("🎲 xG/90", format="%.3f"),
                        "xA/90": st.column_config.NumberColumn("🎪 xA/90", format="%.3f"),
                        "Tackles": st.column_config.NumberColumn("🛡️ Tackles", format="%d"),
                        "Interceptions": st.column_config.NumberColumn("🔄 Int", format="%d"),
                        "Pass%": st.column_config.NumberColumn("📊 Pass%", format="%.1f%%"),
                        "Key Passes": st.column_config.NumberColumn("🔑 KP", format="%d"),
                        "Progressive": st.column_config.NumberColumn("⚡ Prog", format="%d"),
                        "Save%": st.column_config.NumberColumn("🧤 Save%", format="%.1f%%"),
                        "Minutes": st.column_config.NumberColumn("⏱️ Minutes", format="%d")
                    }
                )
    
    else:
        st.warning("🚫 No players found with the current filters. Please adjust your search criteria.")
    
    with st.sidebar:
        st.header("📈 Dataset Statistics")
        st.metric("Total Players", len(all_players_df))
        st.metric("Field Players", len(top5_df))
        st.metric("Goalkeepers", len(keepers_df))
        st.metric("Leagues", len(all_players_df['Comp'].unique()))
        st.metric("Teams", len(all_players_df['Squad'].unique()))
        
        st.divider()
        st.subheader("🎯 Position Breakdown")
        
        if 'Detailed_Position' in all_players_df.columns:
            detailed_pos_counts = all_players_df['Detailed_Position'].value_counts().head(8)
            for pos, count in detailed_pos_counts.items():
                if pd.notna(pos) and pos != 'Unknown':
                    st.metric(f"{pos}", count)
        
        st.divider()
        st.subheader("🏆 League Distribution")
        league_counts = all_players_df['Comp'].value_counts()
        for league, count in league_counts.items():
            if pd.notna(league) and league != 'Comp':
                st.metric(f"{league}", count)

if __name__ == "__main__":
    show_players()
