import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Soccer Stats Players", layout="wide")

@st.cache_data
def load_data():
    top5_players = pd.read_csv('datas_cleaned/top5-players.csv')
    defensive = pd.read_csv('datas_cleaned/Defensive.csv')
    passing = pd.read_csv('datas_cleaned/Passing.csv')
    keepers = pd.read_csv('datas_cleaned/keepers.csv')
    
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
    
    return top5_players, defensive, passing, keepers

def get_player_stats(player_name, top5_df, defensive_df, passing_df, keepers_df):
    player_data = {}
    
    if 'Player' in keepers_df.columns:
        keepers_match = keepers_df[keepers_df['Player'] == player_name]
        if not keepers_match.empty:
            player_data['goalkeeper'] = keepers_match.iloc[0]
            return player_data
    
    top5_match = top5_df[top5_df['Player'] == player_name]
    if not top5_match.empty:
        player_data['general'] = top5_match.iloc[0]
    
    defensive_match = defensive_df[defensive_df['Player'] == player_name]
    if not defensive_match.empty:
        player_data['defensive'] = defensive_match.iloc[0]
    
    passing_match = passing_df[passing_df['Player'] == player_name]
    if not passing_match.empty:
        player_data['passing'] = passing_match.iloc[0]
    
    return player_data

def display_player_info(player_data):
    if 'general' in player_data:
        info = player_data['general']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{info.get('Age', 'N/A')}")
            st.metric("Nation", info.get('Nation', 'N/A'))
        
        with col2:
            st.metric("Position", info.get('Pos', 'N/A'))
            st.metric("Squad", info.get('Squad', 'N/A'))
        
        with col3:
            st.metric("Competition", info.get('Comp', 'N/A'))
            st.metric("Minutes Played", f"{info.get('Min', 0)}")
        
        with col4:
            st.metric("Goals", f"{info.get('Gls', 0)}")
            st.metric("Assists", f"{info.get('Ast', 0)}")
    
    elif 'goalkeeper' in player_data:
        info = player_data['goalkeeper']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Age", f"{info.get('Age', 'N/A')}")
            st.metric("Nation", info.get('Nation', 'N/A'))
        
        with col2:
            st.metric("Position", "GK")
            st.metric("Squad", info.get('Squad', 'N/A'))
        
        with col3:
            st.metric("Competition", info.get('Comp', 'N/A'))
            st.metric("Minutes Played", f"{info.get('Min', 0)}")
        
        with col4:
            st.metric("Saves", f"{info.get('Saves', 0)}")
            st.metric("Save %", f"{info.get('Save%', 0)}%")

def create_fifa_style_radar(player_data, player_name):
    fig = go.Figure()
    
    if 'general' in player_data:
        info = player_data['general']
        
        stats = {
            'Pace': min(100, (info.get('PrgR', 0) + info.get('PrgC', 0)) / 2),
            'Shooting': min(100, info.get('Gls_90', 0) * 50 + info.get('xG_90', 0) * 30),
            'Passing': min(100, info.get('Ast_90', 0) * 40 + info.get('PrgP', 0) / 2),
            'Dribbling': min(100, info.get('PrgR', 0) / 2 + info.get('PrgC', 0) / 2),
            'Defending': min(100, (info.get('CrdY', 0) + info.get('CrdR', 0)) / 2),
            'Physical': min(100, info.get('Min', 0) / 50)
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
            stats = {
                'Goals/90': round(info.get('Gls_90', 0), 2),
                'Assists/90': round(info.get('Ast_90', 0), 2),
                'xG/90': round(info.get('xG_90', 0), 2),
                'xA/90': round(info.get('xAG_90', 0), 2),
                'Progressive': round(info.get('PrgC', 0) / 10, 2),
                'Cards': round((info.get('CrdY', 0) + info.get('CrdR', 0) * 2) / 10, 2)
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

def main():
    st.title("⚽ Soccer Stats Players Dashboard")
    
    top5_df, defensive_df, passing_df, keepers_df = load_data()
    
    all_players_df = top5_df[['Player', 'Nation', 'Pos', 'Squad', 'Comp']].copy()
    
    if 'Player' in keepers_df.columns:
        keepers_for_filter = keepers_df[['Player', 'Nation', 'Squad', 'Comp']].copy()
        keepers_for_filter['Pos'] = 'GK'
        all_players_df = pd.concat([all_players_df, keepers_for_filter], ignore_index=True)
    
    all_players_df = all_players_df.drop_duplicates(subset=['Player'])
    
    st.header("🔍 Filters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        leagues = ["all"] + sorted([league for league in all_players_df['Comp'].dropna().unique().tolist() if league != 'Comp'])
        selected_league = st.selectbox("🏆 League", leagues, index=0)
    
    with col2:
        positions = ["all"] + sorted(all_players_df['Pos'].dropna().unique().tolist())
        selected_position = st.selectbox("⚽ Position", positions, index=0)
    
    with col3:
        nations = ["all"] + sorted(all_players_df['Nation'].dropna().unique().tolist())
        selected_nation = st.selectbox("🌍 Nationality", nations, index=0)
    
    filtered_df = all_players_df.copy()
    
    if selected_league != "all":
        filtered_df = filtered_df[filtered_df['Comp'] == selected_league]
    
    if selected_position != "all":
        filtered_df = filtered_df[filtered_df['Pos'] == selected_position]
    
    if selected_nation != "all":
        filtered_df = filtered_df[filtered_df['Nation'] == selected_nation]
    
    if not filtered_df.empty:
        player_names = filtered_df['Player'].tolist()
        
        st.header("👤 Player Selection")
        selected_player = st.selectbox("Select a player to analyze", [""] + player_names)
        
        if selected_player:
            player_data = get_player_stats(selected_player, top5_df, defensive_df, passing_df, keepers_df)
            
            st.header(f"📊 {selected_player} - Player Analysis")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                display_player_info(player_data)
            
            with col2:
                st.plotly_chart(create_fifa_style_radar(player_data, selected_player), use_container_width=True)
            
            st.divider()
            
            if 'general' in player_data:
                info = player_data['general']
                
                st.subheader("⚡ Performance Statistics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Offensive Stats**")
                    perf_data = {
                        'Goals per 90': info.get('Gls_90', 0),
                        'Assists per 90': info.get('Ast_90', 0),
                        'xG per 90': info.get('xG_90', 0),
                        'xA per 90': info.get('xAG_90', 0)
                    }
                    st.bar_chart(perf_data)
                
                with col2:
                    st.write("**Progressive Play**")
                    add_data = {
                        'Progressive Carries': info.get('PrgC', 0),
                        'Progressive Passes': info.get('PrgP', 0),
                        'Progressive Runs': info.get('PrgR', 0)
                    }
                    st.bar_chart(add_data)
            
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
                    st.write(f"**{i}.** {player}")
            else:
                st.info("💡 Select at least 2 players to enable comparison")
        
        if len(comparison_players) > 1:
            players_data = {}
            for player in comparison_players:
                players_data[player] = get_player_stats(player, top5_df, defensive_df, passing_df, keepers_df)
            
            st.subheader("📈 Interactive Comparison Chart")
            st.plotly_chart(create_comparison_radar(players_data), use_container_width=True)
            
            st.subheader("📋 Detailed Stats Comparison")
            
            comparison_data = []
            
            for player in comparison_players:
                if player in players_data:
                    if 'general' in players_data[player]:
                        info = players_data[player]['general']
                        comparison_data.append({
                            'Player': player,
                            'Age': info.get('Age', 'N/A'),
                            'Position': info.get('Pos', 'N/A'),
                            'Squad': info.get('Squad', 'N/A'),
                            'League': info.get('Comp', 'N/A'),
                            'Goals/90': round(info.get('Gls_90', 0), 3),
                            'Assists/90': round(info.get('Ast_90', 0), 3),
                            'xG/90': round(info.get('xG_90', 0), 3),
                            'xA/90': round(info.get('xAG_90', 0), 3),
                            'Minutes': info.get('Min', 0)
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
                st.dataframe(
                    comparison_df, 
                    use_container_width=True,
                    column_config={
                        "Player": st.column_config.TextColumn("👤 Player", width="medium"),
                        "Squad": st.column_config.TextColumn("🏟️ Club", width="medium"),
                        "League": st.column_config.TextColumn("🏆 League", width="medium"),
                        "Goals/90": st.column_config.NumberColumn("⚽ Goals/90", format="%.3f"),
                        "Assists/90": st.column_config.NumberColumn("🎯 Assists/90", format="%.3f"),
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

if __name__ == "__main__":
    main()
