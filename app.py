import streamlit as st
import pandas as pd
import sys
import os

st.set_page_config(
    page_title="Football Stats",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard')
if dashboard_path not in sys.path:
    sys.path.insert(0, dashboard_path)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        color: #ffffff;
    }
    
    .main {
        padding-top: 1rem;
        background-color: #ffffff;
    }
    
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    [data-testid="metric-container"] {
        background-color: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        background: #ffffff;
        background-clip: text;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .page-header {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        text-align: center;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    
    .stDataFrame {
        background-color: rgba(0, 0, 0, 0.03);
        border-radius: 10px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(0,0,0,0.1) !important;
        color: #ffffff !important;
        border-radius: 8px;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
    }
    
    .nav-link {
        display: block;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        text-decoration: none;
        color: #ffffff;
        background-color: rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
    }
    
    .nav-link:hover {
        background-color: rgba(0, 0, 0, 0.1);
        transform: translateX(5px);
    }
    
    .nav-link.active {
        background-color: #667eea;
        border-color: #667eea;
        font-weight: 600;
        color: #ffffff;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: #FFFFFF !important;
    }
    
    .stMarkdown p, .stText, .stSelectbox label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        line-height: 1.5 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-title">Soccer Stats</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        page = st.selectbox(
            "Choisir une page",
            ["🏠 Accueil", "👤 Joueurs"],
            index=0
        )
        
        st.divider()
        
        st.markdown("### 📈 Stats rapides")
        try:
            df = pd.read_csv("datas_cleaned/All_Stats_Field_Player.csv")
            st.metric("Total Joueurs", len(df))
            st.metric("Ligues", len(df['Comp'].unique()))
            st.metric("Équipes", len(df['Squad'].unique()))
        except:
            st.info("Données en cours de chargement...")
    
    if page == "🏠 Accueil":
        show_home_page()
    elif page == "👤 Joueurs":
        show_players_page()

def show_home_page():
    try:
        from accueil import show_accueil
        show_accueil()
        
    except ImportError as e:
        st.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        st.markdown("""
        ### 🏠 Page d'accueil
        
        Bienvenue sur SoccerStats Dashboard !
        
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

if __name__ == "__main__":
    main()