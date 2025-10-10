# SoccerStats ⚽📊

Une application d'analyse de données de football pour explorer les performances des joueurs des 5 grands championnats européens.

## 🎯 Objectif du projet

**SoccerStats** est un dashboard interactif développé avec Streamlit qui permet d'analyser et de comparer les performances des joueurs de football des cinq grands championnats européens (Premier League, La Liga, Serie A, Bundesliga, Ligue 1) pour la saison 2023/2024.

### Fonctionnalités principales

- 📊 **Visualisations interactives** des statistiques des joueurs
- 🔍 **Filtres avancés** par poste, ligue, âge, nationalité
- ⚖️ **Comparaisons de joueurs** avec des graphiques radar
- 🏆 **Classements** et analyses par catégorie
- 📈 **Indicateurs de performance** normalisés par 90 minutes
- 🎨 **Interface moderne** avec design sombre

---

## 📥 Installation et Configuration

### 1. Télécharger le projet

```bash
# Cloner le dépôt GitHub
git clone https://github.com/B3ANQ/SoccerStats.git
cd SoccerStats
```

### 2. Initialiser l'environnement

```bash
# Créer un environnement virtuel (recommandé)
python3 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source venv/bin/activate
# Sur Windows :
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Vérifier les données

Assurez-vous que les dossiers `datas/` et `datas_cleaned/` contiennent les fichiers CSV nécessaires :

- `top5-players.csv`
- `Defensive.csv`
- `Passing.csv`
- `keepers.csv`
- Fichiers par ligue (`premier_league_players_positions.csv`, etc.)

---

## 🚀 Lancement de l'application

```bash
# Lancer le dashboard Streamlit
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

---

## 🎮 Comment utiliser SoccerStats

### Interface principale

L'application est organisée en **3 pages principales** :

#### 🏠 **Page d'Accueil**

- Vue d'ensemble des statistiques générales
- Classements par ligue
- Top 3 des meilleurs joueurs par catégorie
- Métriques clés du dataset

#### 📊 **Dashboard Général**

- Analyses globales par ligue et par poste
- Comparaisons entre championnats
- Visualisations des tendances générales
- Statistiques agrégées

#### 👤 **Page Joueurs**

- Recherche et filtrage avancé des joueurs
- Fiches détaillées individuelles
- Comparaisons entre joueurs (graphiques radar)
- Statistiques personnalisées

### Navigation

- **Barre latérale** : Navigation entre les pages + stats rapides
- **Filtres interactifs** : Position, ligue, âge, nationalité
- **Graphiques dynamiques** : Clic et survol pour plus de détails
- **Comparaisons** : Sélection multiple de joueurs

---

## 🛠️ Structure du projet

```text
SoccerStats/
├── app.py                    # Application principale Streamlit
├── requirements.txt          # Dépendances Python
├── README.md                 # Documentation
├── dashboard/                # Modules du dashboard
│   ├── accueil.py           # Page d'accueil
│   ├── General_Dashboard.py  # Dashboard général
│   └── players.py           # Page des joueurs
├── datas/                   # Données brutes
├── datas_cleaned/          # Données nettoyées
├── logos/                  # Logos des équipes par ligue
└── scraping/              # Scripts de scraping
    ├── Scraping.py
    ├── Positions_scrap.py
    └── Logos*_scrap.py
```

### Technologies utilisées

- **Streamlit** : Framework web pour l'interface
- **Pandas** : Manipulation et analyse des données
- **Plotly** : Graphiques interactifs
- **Matplotlib/Seaborn** : Visualisations statiques
- **NumPy** : Calculs numériques
- **Scikit-learn** : Analyses statistiques

---

## 📊 Données et Sources

Le projet utilise des données de football provenant de diverses sources :

- Statistiques des joueurs des 5 grands championnats européens
- Données de performance normalisées par 90 minutes
- Informations sur les postes et clubs
- Logos et métadonnées des équipes

### Indicateurs analysés

- **Offensifs** : Buts, assists, expected goals (xG), tirs cadrés
- **Défensifs** : Tacles, interceptions, duels gagnés
- **Création** : Passes clés, passes progressives
- **Généraux** : Minutes jouées, cartons, âge

---

## 🤝 Équipe du projet

- **Fatima FALL**
- **Alexandre COURTET**  
- **Victor SANSON**

---

## 📄 License

Ce projet est développé dans le cadre d'un projet étudiant à Epitech Digital School.
