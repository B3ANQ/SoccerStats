import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_fbref_keeper_stats(season="2023-2024"):
    url = f"https://fbref.com/en/comps/Big5/{season}/keepers/players/{season}-Big-5-European-Leagues-Stats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Erreur HTTP {resp.status_code} pour l’URL {url}")

    soup = BeautifulSoup(resp.text, "lxml")

    # Récupérer directement le tableau avec id="stats_keeper"
    table = soup.find("table", {"id": "stats_keeper"})
    if table is None:
        raise Exception("Impossible de trouver le tableau des gardiens (id=stats_keeper).")

    # Conversion en DataFrame
    df = pd.read_html(str(table))[0]

    return df

def fetch_fbref_defensive_stats(season="2023-2024"):
    url = f"https://fbref.com/en/comps/Big5/{season}/defense/players/{season}-Big-5-European-Leagues-Stats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Erreur HTTP {resp.status_code} pour l’URL {url}")

    soup = BeautifulSoup(resp.text, "lxml")

    # Récupération directe du tableau
    table = soup.find("table", {"id": "stats_defense"})
    if table is None:
        raise Exception("Impossible de trouver le tableau des stats défensives (id=stats_defense).")

    df = pd.read_html(str(table))[0]
    return df

def flatten_multiindex_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aplati les colonnes si elles sont en MultiIndex."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([c for c in col if c and c != ""]) for col in df.columns]
    return df

def fetch_fbref_passing_stats(season="2023-2024"):
    url = f"https://fbref.com/en/comps/Big5/{season}/passing/players/{season}-Big-5-European-Leagues-Stats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com"
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Erreur HTTP {resp.status_code} pour l’URL {url}")

    soup = BeautifulSoup(resp.text, "lxml")

    # Récupération du tableau des passes
    table = soup.find("table", {"id": "stats_passing"})
    if table is None:
        raise Exception("Impossible de trouver le tableau des stats de passes (id=stats_passing).")

    df = pd.read_html(str(table))[0]
    return df

def flatten_multiindex_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aplati les colonnes si elles sont en MultiIndex."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([c for c in col if c and c != ""]) for col in df.columns]
    return df

def load_and_flatten_csv(path):
    # Lire avec 2 lignes d'entêtes
    df = pd.read_csv(path, header=[0, 1])
    
    # Prendre le 2ème niveau s’il existe, sinon le 1er
    df.columns = [
        col[1] if not col[1].startswith("Unnamed") else col[0] 
        for col in df.columns.values
    ]
    
    return df

def merge_defense_passing(def_csv="Defensive.csv", pass_csv="Passing.csv", output_csv=None):
    df_def = load_and_flatten_csv(def_csv)
    df_pass = load_and_flatten_csv(pass_csv)

    print("Colonnes DEF:", df_def.columns[:10].tolist())
    print("Colonnes PASS:", df_pass.columns[:10].tolist())

    # Clés de merge
    keys = [c for c in ["Player", "Squad", "Nation", "Pos", "Comp", "Age", "Born", "90s"] 
            if c in df_def.columns and c in df_pass.columns]

    if not keys:
        raise Exception("Aucune colonne commune trouvée pour fusionner.")

    merged = pd.merge(df_def, df_pass, on=keys, how="inner", suffixes=("_def", "_pass"))

    if output_csv:
        merged.to_csv(output_csv, index=False)
        print(f"✅ Fichier fusionné sauvegardé dans {output_csv}")

    return merged

df_merged = merge_defense_passing("Defensive.csv", "Passing.csv", "Merged.csv")
