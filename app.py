import streamlit as st
import pandas as pd
import sys
import os

st.set_page_config(
    page_title="SoccerStats",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard')
if dashboard_path not in sys.path:
    sys.path.insert(0, dashboard_path)

st.markdown("""
    <style>
    * {
        font-family: Arial, sans-serif;
        color: #ffffff;
    }
    
    .main {
        padding-top: 1rem;
        background-color: #0e1117;
    }
    
    .css-1d391kg {
        background-color: #0e1117;
    }
    
    [data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        font-family: Arial, sans-serif;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 2rem;
    }
    
    .page-header {
        font-family: Arial, sans-serif;
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: Arial, sans-serif !important;
        color: #ffffff !important;
    }
    
    .stMarkdown p, .stText, .stSelectbox label {
        font-family: Arial, sans-serif !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-title">SoccerStats</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        page = st.selectbox(
            "Choisir une page",
            ["🏠 Accueil", "📊 Général", "👤 Joueurs"],
            index=0
        )
        
        st.divider()
        
        st.markdown("### 📈 Stats rapides")
        try:
            df = pd.read_csv("datas_cleaned/top5-players.csv")
            st.metric("Total Joueurs", len(df))
            st.metric("Ligues", len(df['Comp'].unique()))
            st.metric("Équipes", len(df['Squad'].unique()))
        except:
            st.info("Données en cours de chargement...")
    
    if page == "🏠 Accueil":
        show_home_page()
    elif page == "👤 Joueurs":
        show_players_page()
    elif page == "📊 Général":
        show_general_dashboard_page()

def show_home_page():
    try:
        from accueil import show_accueil
        show_accueil()
        
    except ImportError as e:
        st.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        st.markdown("""
        ### 🏠 Page d'accueil
        
        Bienvenue sur Football Stats Dashboard !
        
        Cette page affiche normalement :
        - 📊 Classements par ligues
        - 🏆 Top 3 des meilleurs joueurs par catégorie
        - 📈 Graphiques interactifs
        
        Veuillez vérifier que le fichier `dashboard/accueil.py` existe.
        """)
    except Exception as e:
        st.error(f"Erreur inattendue: {e}")

def show_players_page():
    try:
        from players import show_players
        show_players()
        
    except ImportError as e:
        st.error(f"Erreur lors du chargement de la page des joueurs: {e}")
        st.markdown("""
        ### 👤 Page des joueurs
        
        Cette page affiche normalement :
        - 🔍 Recherche et filtres avancés
        - 📊 Statistiques détaillées des joueurs
        - ⚖️ Comparaisons entre joueurs
        - 📈 Graphiques radar et visualisations
        
        Veuillez vérifier que le fichier `dashboard/players.py` existe.
        """)
    except Exception as e:
        st.error(f"Erreur inattendue: {e}")

def show_general_dashboard_page():
    try:
        from General_Dashboard import show_general_dashboard
        show_general_dashboard()
        
    except ImportError as e:
        st.error(f"Erreur lors du chargement du dashboard général: {e}")
        st.markdown("""
        ### 📊 Dashboard Général
        
        Cette page affiche normalement :
        - 📈 Statistiques générales par ligue
        - 🏆 Classements et comparaisons
        - 📊 Visualisations interactives des données
        - ⚽ Analyses approfondies des performances
        
        Veuillez vérifier que le fichier `dashboard/General_Dashboard.py` existe.
        """)
    except Exception as e:
        st.error(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    main()