import pandas as pd
import unicodedata
import re
import difflib

# 1. Charger les deux fichiers CSV
liga_df = pd.read_csv("./datas/liga_players_positions.csv")
serie_a_df = pd.read_csv("./datas/serie_a_players_positions.csv")
ligue_1_df = pd.read_csv("./datas/ligue_1_players_positions.csv")
bundesliga_df = pd.read_csv("./datas/bundesliga_players_positions.csv")
premier_league_df = pd.read_csv("./datas/premier_league_players_positions.csv")

# 2. Fusionner les deux DataFrames
merged_df = pd.concat([liga_df, serie_a_df, ligue_1_df, bundesliga_df, premier_league_df], ignore_index=True)

# 3. Sauvegarder le résultat dans un nouveau fichier CSV
merged_df.to_csv("./datas/players_positions.csv", index=False)

print("✅ Fusion terminée ! Le fichier 'players_positions_merged.csv' a été créé.")

def normalize_name(name):
    """Normalise un nom :
       - NFKD pour séparer accents,
       - suppression des caractères combinants,
       - casefold() (meilleur que lower pour Unicode),
       - suppression de la ponctuation, normalisation des espaces."""
    if pd.isna(name):
        return ""
    s = str(name).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = re.sub(r"[^\w\s-]", "", s)       # garde lettres, chiffres, underscore, espaces et tiret
    s = re.sub(r"\s+", " ", s)          # collapse espaces multiples
    return s

# ---------- Chargement ----------
top5_df = pd.read_csv("./datas/top5-players.csv")
positions_df = pd.read_csv("./datas/players_positions.csv")  # colonnes attendues : Name,Position

# On travaille sur une copie (le fichier original reste intact)
top5_copy = top5_df.copy()

# ---------- Normalisation ----------
positions_df['name_norm'] = positions_df['Name'].apply(normalize_name)
top5_copy['name_norm'] = top5_copy['Player'].apply(normalize_name)

# Vérifier doublons potentiels dans players_positions
dups = positions_df[positions_df['name_norm'].duplicated(keep=False)]
if not dups.empty:
    print("ATTENTION: doublons détectés dans players_positions.csv (noms normalisés) :")
    print(dups[['Name', 'name_norm']].to_string(index=False))
    # On continue quand même (la dernière occurrence prendra le dessus si dict)

# Création du mapping normalisé -> Position
pos_map = dict(zip(positions_df['name_norm'], positions_df['Position']))
pos_keys = list(pos_map.keys())

# ---------- Fonction de recherche avec fallback ----------
def find_position_for(norm_name, fuzzy_cutoff=0.85):
    """Retourne (position, match_type) ou (None, None)."""
    if not norm_name:
        return None, None
    # 1) match exact
    if norm_name in pos_map:
        return pos_map[norm_name], 'exact'
    # 2) fuzzy (difflib)
    match = difflib.get_close_matches(norm_name, pos_keys, n=1, cutoff=fuzzy_cutoff)
    if match:
        return pos_map[match[0]], f'fuzzy:{match[0]}'
    # 3) fallback par nom de famille (dernier token) si unique dans la base
    last = norm_name.split()[-1]
    candidates = [k for k in pos_keys if k.split()[-1] == last]
    if len(candidates) == 1:
        return pos_map[candidates[0]], f'lastname:{candidates[0]}'
    return None, None

# ---------- Application du mapping ----------
new_positions = []
match_types = []
for _, row in top5_copy.iterrows():
    norm = row['name_norm']
    pos, mtype = find_position_for(norm, fuzzy_cutoff=0.85)  # ajuste cutoff si besoin
    if pos:
        new_positions.append(pos)
        match_types.append(mtype)
    else:
        # conserver l'ancien poste si pas de correspondance
        new_positions.append(row['Pos'])
        match_types.append('original')

top5_copy['Pos'] = new_positions
top5_copy['match_type'] = match_types

# ---------- Rapport ----------
# comparer avec l'original pour connaître ce qui a changé
changed_idx = top5_copy.index[top5_copy['Pos'] != top5_df['Pos']].tolist()
print(f"\n✅ {len(changed_idx)} postes remplacés sur {len(top5_copy)} joueurs.\n")
if changed_idx:
    changed = top5_copy.loc[changed_idx].copy()
    changed['old_Pos'] = top5_df.loc[changed_idx, 'Pos'].values
    print("Remplacements (Player | ancien -> nouveau | méthode) :")
    for _, r in changed.iterrows():
        print(f"- {r['Player']} | {r['old_Pos']} -> {r['Pos']} | {r['match_type']}")

unmatched = top5_copy[top5_copy['match_type'] == 'original']
print(f"\nℹ️ {len(unmatched)} joueurs non appariés (poste d'origine conservé).")
if len(unmatched) > 0:
    print("Liste des non-appariés (extrait) :")
    print(unmatched['Player'].tolist()[:20])  # montre jusqu'à 20

# ---------- Sauvegarde ----------
out_path = "./datas_cleaned/top5_players_with_positions.csv"
top5_copy.to_csv(out_path, index=False)
print(f"\nFichier sauvegardé : {out_path}")
print("📄 Nouveau fichier créé : top5_players_with_positions.csv")

def normalize_name(name):
    """Nettoie et normalise un nom pour de meilleurs appariements."""
    if pd.isna(name):
        return ""
    s = str(name).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

# 1. Charger les fichiers
defensive_df = pd.read_csv("./datas/Defensive.csv", skiprows=1)
positions_df = pd.read_csv("./datas/players_positions.csv")

# 2. Travailler sur une copie
defensive_copy = defensive_df.copy()

# 3. Normaliser les noms
defensive_copy['name_norm'] = defensive_copy['Player'].apply(normalize_name)
positions_df['name_norm'] = positions_df['Name'].apply(normalize_name)

# 4. Créer un mapping nom_normalisé -> position
pos_map = dict(zip(positions_df['name_norm'], positions_df['Position']))
pos_keys = list(pos_map.keys())

# 5. Fonction de recherche avec fallback
def find_position_for(norm_name, fuzzy_cutoff=0.85):
    if not norm_name:
        return None, None
    # exact match
    if norm_name in pos_map:
        return pos_map[norm_name], 'exact'
    # fuzzy match
    match = difflib.get_close_matches(norm_name, pos_keys, n=1, cutoff=fuzzy_cutoff)
    if match:
        return pos_map[match[0]], f'fuzzy:{match[0]}'
    # fallback par nom de famille
    last = norm_name.split()[-1]
    candidates = [k for k in pos_keys if k.split()[-1] == last]
    if len(candidates) == 1:
        return pos_map[candidates[0]], f'lastname:{candidates[0]}'
    return None, None

# 6. Remplacement des postes
new_positions = []
match_types = []

for _, row in defensive_copy.iterrows():
    norm = row['name_norm']
    pos, mtype = find_position_for(norm)
    if pos:
        new_positions.append(pos)
        match_types.append(mtype)
    else:
        new_positions.append(row['Pos'])
        match_types.append('original')

defensive_copy['Pos'] = new_positions
defensive_copy['match_type'] = match_types

# 7. Rapport des changements
changed_idx = defensive_copy.index[defensive_copy['Pos'] != defensive_df['Pos']].tolist()
print(f"\n✅ {len(changed_idx)} postes remplacés sur {len(defensive_copy)} joueurs.\n")

if changed_idx:
    changed = defensive_copy.loc[changed_idx].copy()
    changed['old_Pos'] = defensive_df.loc[changed_idx, 'Pos'].values
    print("Remplacements (Player | ancien -> nouveau | méthode) :")
    for _, r in changed.iterrows():
        print(f"- {r['Player']} | {r['old_Pos']} -> {r['Pos']} | {r['match_type']}")

unmatched = defensive_copy[defensive_copy['match_type'] == 'original']
print(f"\nℹ️ {len(unmatched)} joueurs non appariés (poste d'origine conservé).")
if len(unmatched) > 0:
    print("Liste des non-appariés (extrait) :")
    print(unmatched['Player'].tolist()[:20])

# 8. Sauvegarde
output_file = "./datas_cleaned/Defensive_with_positions.csv"
defensive_copy.to_csv(output_file, index=False)
print(f"\n📄 Nouveau fichier créé : {output_file}")




import unicodedata
import re
import difflib

def normalize_name(name):
    if pd.isna(name):
        return ""
    s = str(name).strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

# 1. Charger Defensive.csv correctement
defensive_df = pd.read_csv("./datas/Passing.csv", skiprows=1)
positions_df = pd.read_csv("./datas/players_positions.csv")

# 2. Copier pour travailler sans toucher à l’original
defensive_copy = defensive_df.copy()

# 3. Normaliser les noms
defensive_copy['name_norm'] = defensive_copy['Player'].apply(normalize_name)
positions_df['name_norm'] = positions_df['Name'].apply(normalize_name)

# 4. Créer mapping
pos_map = dict(zip(positions_df['name_norm'], positions_df['Position']))
pos_keys = list(pos_map.keys())

def find_position_for(norm_name, fuzzy_cutoff=0.85):
    if not norm_name:
        return None, None
    if norm_name in pos_map:
        return pos_map[norm_name], 'exact'
    match = difflib.get_close_matches(norm_name, pos_keys, n=1, cutoff=fuzzy_cutoff)
    if match:
        return pos_map[match[0]], f'fuzzy:{match[0]}'
    last = norm_name.split()[-1]
    candidates = [k for k in pos_keys if k.split()[-1] == last]
    if len(candidates) == 1:
        return pos_map[candidates[0]], f'lastname:{candidates[0]}'
    return None, None

# 5. Remplacement
new_positions = []
match_types = []

for _, row in defensive_copy.iterrows():
    norm = row['name_norm']
    pos, mtype = find_position_for(norm)
    if pos:
        new_positions.append(pos)
        match_types.append(mtype)
    else:
        new_positions.append(row['Pos'])
        match_types.append('original')

defensive_copy['Pos'] = new_positions
defensive_copy['match_type'] = match_types

# 6. Rapport
changed_idx = defensive_copy.index[defensive_copy['Pos'] != defensive_df['Pos']].tolist()
print(f"\n✅ {len(changed_idx)} postes remplacés sur {len(defensive_copy)} joueurs.\n")

if changed_idx:
    changed = defensive_copy.loc[changed_idx].copy()
    changed['old_Pos'] = defensive_df.loc[changed_idx, 'Pos'].values
    for _, r in changed.iterrows():
        print(f"- {r['Player']} | {r['old_Pos']} -> {r['Pos']} | {r['match_type']}")

unmatched = defensive_copy[defensive_copy['match_type'] == 'original']
print(f"\nℹ️ {len(unmatched)} joueurs non appariés (poste d'origine conservé).")
if len(unmatched) > 0:
    print(unmatched['Player'].tolist()[:20])

# 7. Sauvegarde
output_file = "./datas_cleaned/Passing_with_positions.csv"
defensive_copy.to_csv(output_file, index=False)
print(f"\n📄 Nouveau fichier créé : {output_file}")