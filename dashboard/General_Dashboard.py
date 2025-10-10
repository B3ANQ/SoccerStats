import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image {image_path}: {e}")
        return ""

@st.cache_data
def load_data():
    data_dir = "datas_cleaned"
    files_to_use = [
        ("Defensive.csv", 1),
        ("keepers.csv", 0),
        ("Passing.csv", 1),
        ("top5-players.csv", 0)
    ]
    dfs = []
    for file, header_row in files_to_use:
        path = os.path.join(data_dir, file)
        if os.path.exists(path):
            df = pd.read_csv(path, header=header_row)
            dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    return data

def show_general_dashboard():
    
    df = load_data()

    st.title("📊 Dashboard Général des Ligues de Football")

    st.header("⚽ Statistiques Générales par Ligue")

    col1, col2 = st.columns(2)

    league_col = 'Comp' if 'Comp' in df.columns else None
    club_col = 'Squad' if 'Squad' in df.columns else None
    position_col = 'Pos' if 'Pos' in df.columns else None
    goals_col = 'Gls' if 'Gls' in df.columns else None
    assists_col = 'Ast' if 'Ast' in df.columns else None
    minutes_col = 'Min' if 'Min' in df.columns else None

    if not all([league_col, club_col, position_col]):
        st.error("Colonnes principales manquantes dans les fichiers CSV. Vérifiez les noms de colonnes.")
        st.stop()

    st.subheader("Buts par match en moyenne par championnat")
    if goals_col and club_col and league_col:
        buts_par_club = df.groupby([league_col, club_col])[goals_col].sum().reset_index()

        total_buts_par_ligue = buts_par_club.groupby(league_col)[goals_col].sum()

        nb_clubs_par_ligue = buts_par_club.groupby(league_col)[club_col].nunique()

        nb_matchs_par_ligue = (nb_clubs_par_ligue * 2) - 2

        buts_par_journée = total_buts_par_ligue / nb_matchs_par_ligue

        buts_par_match = buts_par_journée / (nb_clubs_par_ligue/2)

        buts_par_match = buts_par_match.sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(6,4))
        buts_par_match.plot(kind='barh', ax=ax, color='salmon')
        ax.set_xlabel("Buts par match (moyenne)")
        ax.set_ylabel("Ligue")
        ax.set_title("Moyenne de buts par match par championnat")

        for i, v in enumerate(buts_par_match):
            ax.text(v + 0.02, i, f"{v:.2f}", va='center')

        st.pyplot(fig)
    else:
        st.info("Colonnes nécessaires manquantes pour le calcul.")

    st.markdown("---")

    st.header("Recherche Avancée")

    league_logos = {
        "PL.png": ("eng Premier League", "premier_league"),
        "L1.png": ("fr Ligue 1", "ligue_1"),
        "Bundesliga.png": ("de Bundesliga", "bundesliga"),
        "Liga.png": ("es La Liga", "liga"),
        "Serie_A.png": ("it Serie A", "serie_a")
    }
    logo_dir = "logos"

    if "selected_leagues" not in st.session_state:
        st.session_state.selected_leagues = list(league_logos.values())

    if "selected_clubs" not in st.session_state:
        st.session_state.selected_clubs = []

    st.subheader("Sélectionne une ou plusieurs ligues en cliquant sur leur logo :")
    logo_cols = st.columns(len(league_logos))

    for i, (logo_file, (comp_value, folder_name)) in enumerate(league_logos.items()):
        selected = (comp_value, folder_name) in st.session_state.selected_leagues
        with logo_cols[i]:
            if st.button(
                comp_value,
                key=f"league_btn_{logo_file}",
                use_container_width=True,
                type="primary" if selected else "secondary"
            ):
                if selected:
                    st.session_state.selected_leagues.remove((comp_value, folder_name))
                else:
                    st.session_state.selected_leagues.append((comp_value, folder_name))
                st.rerun()
            
            border_color = "#0074D9" if selected else "#DDD"
            border_width = "5px" if selected else "2px"
            st.markdown(
                f"""
                <div style="border:{border_width} solid {border_color};
                            border-radius:10px;
                            padding:5px;
                            text-align:center;
                            margin-top:-10px;">
                    <img src="data:image/png;base64,{get_base64_image(os.path.join(logo_dir, logo_file))}" 
                         width="80" style="display:block;margin:auto;">
                </div>
                """,
                unsafe_allow_html=True
            )

    selected_league_folders = [folder for comp, folder in st.session_state.selected_leagues]
    selected_leagues = [comp for comp, folder in st.session_state.selected_leagues]
    filtered_df = df[df[league_col].isin(selected_leagues)]

    club_logo_map = {}
    for folder_name in selected_league_folders:
        club_logo_dir = os.path.join(logo_dir, folder_name)
        for file in os.listdir(club_logo_dir):
            if file.endswith(".png"):
                club_name = file.replace(".png", "")
                if club_name in set(filtered_df[club_col].dropna().unique()):
                    logo_path = os.path.join(club_logo_dir, file)
                    club_logo_map[club_name] = logo_path

    if not st.session_state.selected_clubs or not all(club in club_logo_map for club in st.session_state.selected_clubs):
        st.session_state.selected_clubs = list(club_logo_map.keys())

    st.subheader("Sélectionne un ou plusieurs clubs en cliquant sur leur logo :")

    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        if st.button("✅ Tout sélectionner"):
            st.session_state.selected_clubs = list(club_logo_map.keys())
            st.rerun()
    with col_sel2:
        if st.button("❌ Tout désélectionner"):
            st.session_state.selected_clubs = []
            st.rerun()

    def chunk_list(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    club_items = sorted(club_logo_map.items())
    for row_idx, club_row in enumerate(chunk_list(club_items, 10)):
        club_cols = st.columns(10)
        for col_idx, (club, logo_path) in enumerate(club_row):
            with club_cols[col_idx]:
                selected = club in st.session_state.selected_clubs
                
                if st.button(
                    "✓" if selected else "○",
                    key=f"club_btn_{club}_{row_idx}_{col_idx}",
                    use_container_width=True
                ):
                    if selected:
                        st.session_state.selected_clubs.remove(club)
                    else:
                        st.session_state.selected_clubs.append(club)
                    st.rerun()
                
                border_color = "#0074D9" if selected else "#DDD"
                border_width = "4px" if selected else "2px"
                st.markdown(
                    f"""
                    <div style="border:{border_width} solid {border_color};
                                border-radius:8px;
                                padding:3px;
                                height:80px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                margin-top:-10px;">
                        <img src="data:image/png;base64,{get_base64_image(logo_path)}" 
                             style="max-width:70px;max-height:70px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.caption(club, help=club)

    if st.session_state.selected_clubs:
        filtered_df = filtered_df[filtered_df[club_col].isin(st.session_state.selected_clubs)]
    else:
        st.warning("⚠️ Aucun club sélectionné. Sélectionnez au moins un club.")
        filtered_df = filtered_df[filtered_df[club_col].isin([])]

    if not filtered_df.empty:
        st.subheader("Catégorie de statistiques")
        
        stats_categories = {
            "Attaque": {
                "stats": ["Gls", "Sh", "SoT", "SoT%", "Sh/90", "SoT/90", "G/Sh", "G/SoT", "Dist", "FK", "PK", "PKatt"],
                "description": "Statistiques offensives (buts, tirs, penalties)"
            },
            "Création de jeu": {
                "stats": ["Ast", "xAG", "xA", "KP", "1/3", "PPA", "CrsPA", "PrgP", "Cmp", "Att", "Cmp%", "TotDist", "PrgDist"],
                "description": "Statistiques de création et de passes"
            },
            "Défense": {
                "stats": ["Tkl", "TklW", "Def 3rd", "Mid 3rd", "Att 3rd", "Blocks", "Int", "Clr", "Err"],
                "description": "Statistiques défensives (tacles, interceptions, blocks)"
            },
            "Gardiens": {
                "stats": ["GA", "GA90", "SoTA", "Saves", "Save%", "W", "D", "L", "CS", "CS%", "PKA", "PKsv", "PKm"],
                "description": "Statistiques spécifiques aux gardiens"
            }
        }
        
        selected_category = st.selectbox(
            "Choisir une catégorie",
            list(stats_categories.keys()),
            help="Sélectionnez le type de statistiques à analyser"
        )
        
        st.info(f"📊 {stats_categories[selected_category]['description']}")
        
        available_stats = [stat for stat in stats_categories[selected_category]["stats"] if stat in filtered_df.columns]
        
        if not available_stats:
            st.warning(f"⚠️ Aucune statistique de la catégorie '{selected_category}' n'est disponible dans les données.")
        else:
            postes = filtered_df[position_col].dropna().unique()
            selected_poste = st.selectbox("Poste", postes, index=list(postes).index('BU') if 'BU' in postes else 0)
            filtered_df = filtered_df[filtered_df[position_col] == selected_poste]
            
            selected_stats = st.multiselect(
                "Statistiques à observer",
                available_stats,
                default=available_stats[:3] if len(available_stats) >= 3 else available_stats,
                help="Choisissez les statistiques spécifiques à afficher"
            )
            
            if selected_stats:
                st.subheader(f"📋 Stats {selected_category} des joueurs filtrés")
                player_cols = ['Player'] if 'Player' in filtered_df.columns else []
                display_cols = player_cols + [league_col, club_col, position_col] + selected_stats
                
                sorted_df = filtered_df[display_cols].sort_values(by=selected_stats[0], ascending=False)
                st.dataframe(sorted_df, use_container_width=True)
                
                st.subheader(f"📊 Visualisations - {selected_category}")
                
                nb_players = st.slider("Nombre de joueurs à afficher dans les graphiques", 5, 20, 10)
                
                if selected_category == "Attaque":
                    if "Gls" in selected_stats and "Gls" in filtered_df.columns:
                        st.markdown("**🎯 Top Buteurs**")
                        top_players = filtered_df.nlargest(nb_players, "Gls")[["Player", "Gls", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Reds(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Gls"], color=colors)
                        ax.set_xlabel("Nombre de buts")
                        ax.set_title(f"Top {nb_players} Buteurs")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Gls"] + 0.1, i, f"{int(row['Gls'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    if "Sh" in selected_stats and "Gls" in selected_stats:
                        st.markdown("**📈 Relation Tirs / Buts par joueur**")
                        fig, ax = plt.subplots(figsize=(10, 6))
                        scatter = ax.scatter(filtered_df["Sh"], filtered_df["Gls"], 
                                           s=100, alpha=0.6, c=filtered_df["Gls"], 
                                           cmap='YlOrRd', edgecolors='black', linewidth=0.5)
                        ax.set_xlabel("Nombre de tirs")
                        ax.set_ylabel("Nombre de buts")
                        ax.set_title("Efficacité offensive des joueurs")
                        plt.colorbar(scatter, label='Buts')
                        
                        top_5 = filtered_df.nlargest(5, "Gls")
                        for idx, row in top_5.iterrows():
                            if pd.notna(row["Sh"]) and pd.notna(row["Gls"]):
                                ax.annotate(row["Player"], 
                                          (row["Sh"], row["Gls"]),
                                          xytext=(5, 5), textcoords='offset points',
                                          fontsize=8, alpha=0.7)
                        plt.tight_layout()
                        st.pyplot(fig)
                
                elif selected_category == "Création de jeu":
                    if "Ast" in selected_stats and "Ast" in filtered_df.columns:
                        st.markdown("**🎯 Top Passeurs décisifs**")
                        top_players = filtered_df.nlargest(nb_players, "Ast")[["Player", "Ast", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Greens(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Ast"], color=colors)
                        ax.set_xlabel("Nombre de passes décisives")
                        ax.set_title(f"Top {nb_players} Passeurs décisifs")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Ast"] + 0.1, i, f"{int(row['Ast'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    if "Cmp" in selected_stats:
                        st.markdown("**📈 Top joueurs - Passes complétées**")
                        top_players = filtered_df.nlargest(nb_players, "Cmp")[["Player", "Cmp", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Purples(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Cmp"], color=colors)
                        ax.set_xlabel("Passes complétées")
                        ax.set_title(f"Top {nb_players} - Passes complétées")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Cmp"] + 5, i, f"{int(row['Cmp'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                
                elif selected_category == "Défense":
                    if "Tkl" in selected_stats and "Tkl" in filtered_df.columns:
                        st.markdown("**🛡️ Top Tackleurs**")
                        top_players = filtered_df.nlargest(nb_players, "Tkl")[["Player", "Tkl", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Oranges(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Tkl"], color=colors)
                        ax.set_xlabel("Nombre de tacles")
                        ax.set_title(f"Top {nb_players} Tackleurs")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Tkl"] + 0.5, i, f"{int(row['Tkl'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    if "Int" in selected_stats:
                        st.markdown("**🚫 Top joueurs - Interceptions**")
                        top_players = filtered_df.nlargest(nb_players, "Int")[["Player", "Int", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Reds(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Int"], color=colors)
                        ax.set_xlabel("Nombre d'interceptions")
                        ax.set_title(f"Top {nb_players} - Interceptions")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Int"] + 0.5, i, f"{int(row['Int'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                
                elif selected_category == "Gardiens":
                    if "Saves" in selected_stats and "Saves" in filtered_df.columns:
                        st.markdown("**🧤 Top Gardiens (Arrêts)**")
                        top_players = filtered_df.nlargest(nb_players, "Saves")[["Player", "Saves", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Blues(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["Saves"], color=colors)
                        ax.set_xlabel("Nombre d'arrêts")
                        ax.set_title(f"Top {nb_players} Gardiens - Arrêts")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["Saves"] + 1, i, f"{int(row['Saves'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                    
                    # Graphique 2 : Clean Sheets
                    if "CS" in filtered_df.columns:
                        st.markdown("**🏆 Top Gardiens - Clean Sheets**")
                        top_players = filtered_df.nlargest(nb_players, "CS")[["Player", "CS", club_col]]
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.Greens(range(len(top_players)))
                        ax.barh(top_players["Player"], top_players["CS"], color=colors)
                        ax.set_xlabel("Clean Sheets")
                        ax.set_title(f"Top {nb_players} Gardiens - Clean Sheets")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_players.iterrows()):
                            ax.text(row["CS"] + 0.1, i, f"{int(row['CS'])} ({row[club_col]})", va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
                
                if len(selected_stats) >= 2:
                    st.markdown("---")
                    st.markdown("**📊 Comparaisons multi-statistiques**")
                    
                    st.markdown(f"**🏅 Top {nb_players} joueurs (moyenne des stats sélectionnées)**")
                    
                    normalized_df = filtered_df.copy()
                    for stat in selected_stats:
                        if stat in normalized_df.columns and normalized_df[stat].max() > 0:
                            normalized_df[f"{stat}_norm"] = normalized_df[stat] / normalized_df[stat].max()
                    
                    norm_cols = [f"{stat}_norm" for stat in selected_stats if f"{stat}_norm" in normalized_df.columns]
                    if norm_cols:
                        normalized_df["avg_performance"] = normalized_df[norm_cols].mean(axis=1)
                        top_overall = normalized_df.nlargest(nb_players, "avg_performance")[["Player", "avg_performance", club_col]]
                        
                        fig, ax = plt.subplots(figsize=(10, 6))
                        colors = plt.cm.viridis(range(len(top_overall)))
                        ax.barh(top_overall["Player"], top_overall["avg_performance"] * 100, color=colors)
                        ax.set_xlabel("Score de performance (%)")
                        ax.set_title(f"Top {nb_players} joueurs - Performance globale")
                        ax.invert_yaxis()
                        for i, (idx, row) in enumerate(top_overall.iterrows()):
                            ax.text(row["avg_performance"] * 100 + 0.5, i, 
                                   f"{row['avg_performance']*100:.1f}% ({row[club_col]})", 
                                   va='center', fontsize=9)
                        plt.tight_layout()
                        st.pyplot(fig)
            else:
                st.info("👆 Sélectionnez au moins une statistique à observer")