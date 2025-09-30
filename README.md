# SoccerStats ⚽📊

## Présentation du projet
KO SoccerStats est un projet d’analyse de données sportives appliqué au football, centré sur les cinq grands championnats européens (saison 2023/2024).  
L’objectif est de transformer un dataset brut de joueurs en un outil d’exploration dynamique permettant d’analyser et de comparer les performances selon différents critères (poste, ligue, âge, expérience, etc.).

Le projet combine **data cleaning**, **indicateurs statistiques avancés** et **visualisation interactive** pour fournir une vision claire et exploitable des performances des joueurs.

---

## Objectifs
- Explorer et nettoyer les données pour assurer leur fiabilité.  
- Construire des indicateurs de performance avancés (ex. *expected goals*, passes clés, ratios par 90 min).  
- Concevoir un **dashboard interactif** pour explorer les performances des joueurs.  
- Comparer les performances entre ligues, postes et profils.  
- Développer une analyse critique sur la qualité et les limites des données.  

---

## Méthodologie
1. **Vérification et nettoyage des données**  
   - Gestion des doublons, valeurs manquantes et aberrantes.  
   - Création de variables utiles (âge, ratios buts/minute, etc.).  

2. **Analyse exploratoire**  
   - Visualisations descriptives (par poste, nationalité, ligue).  
   - Ratios normalisés (par 90 minutes).  
   - Corrélations (expérience ↔ performance).  

3. **Indicateurs avancés**  
   - Offensifs : xG, xA, % tirs cadrés, efficacité offensive.  
   - Défensifs : tacles réussis, interceptions, duels gagnés.  
   - Création : passes clés, progressive passes.  
   - Élaboration de KPI composites.  

4. **Dashboard interactif avec Streamlit**  
   - Filtres interactifs (poste, ligue, âge, nationalité, expérience).  
   - Comparaison de joueurs (radar chart, fiches type *profil FIFA*).  
   - Interface claire et ergonomique, pensée pour l’exploration dynamique.  

5. **Restitution et analyse critique**  
   - Présentation orale (soutenance).  
   - Rapport écrit (5 à 10 pages).  

---

## Installation du projet

1. Cloner le dépôt GitHub :  
```bash
git clone https://github.com/votre-utilisateur/SoccerStats.git
cd SoccerStats
```

2. Créer un environnement virtuel (optionnel mais recommandé) :  
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :  
```bash
pip install -r requirements.txt
```

---

## Dashboard avec Streamlit
Le dashboard est développé avec **[Streamlit](https://streamlit.io/)**, une librairie Python permettant de créer rapidement des applications web interactives.  
Grâce à Streamlit, nous avons pu :  
- Créer des filtres interactifs pour explorer les joueurs.  
- Intégrer des graphiques dynamiques (bar charts, scatter plots, radar charts).  
- Générer des fiches individuelles par joueur, inspirées des cartes FIFA.  
- Offrir une navigation fluide et un storytelling accessible à tous.  

👉 Pour lancer le dashboard :  
```bash
streamlit run "fichier_dashboard.py"
```

---

## 📦 Livrables
- Dataset nettoyé + script Python de nettoyage.  
- Rapport exploratoire avec visualisations commentées.  
- Tableau d’indicateurs avancés.  
- Dashboard Streamlit interactif.  
- Rapport critique final + soutenance.  

---

## 👥 Équipe du projet
- **Fatima FALL**
- **Alexandre COURTET**
- **Victor SANSON**
