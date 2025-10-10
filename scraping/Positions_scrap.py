import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Config ---
URL = "https://www.footmercato.net/angleterre/premier-league/2023-2024/joueur"
OUTDIR = "datas"
os.makedirs(OUTDIR, exist_ok=True)
CSV_PATH = os.path.join(OUTDIR, "premier_league_players_positions.csv")

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(5)

players_data = []

while True:
    # --- Récupérer les joueurs visibles ---
    players = driver.find_elements(By.CSS_SELECTOR, "span.personCardCell__infos")
    for p in players:
        try:
            name = p.find_element(By.CSS_SELECTOR, "span.personCardCell__name").text.strip()
            position = p.find_element(By.CSS_SELECTOR, "span.personCardCell__description").text.strip()
            if {"Name": name, "Position": position} not in players_data:
                players_data.append({"Name": name, "Position": position})
        except:
            continue

    # --- Chercher le bouton "Afficher plus" par texte ---
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Afficher plus')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)
        load_more.click()
        time.sleep(2)  # attendre le chargement
    except TimeoutException:
        break  # plus de bouton → tous les joueurs sont chargés

driver.quit()

# --- Sauvegarder CSV ---
df = pd.DataFrame(players_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Extraction terminée. {len(players_data)} joueurs enregistrés dans '{CSV_PATH}'")







# --- Config ---
URL = "https://www.footmercato.net/allemagne/bundesliga/2023-2024/joueur"
OUTDIR = "datas"
os.makedirs(OUTDIR, exist_ok=True)
CSV_PATH = os.path.join(OUTDIR, "bundesliga_players_positions.csv")

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(5)

players_data = []

while True:
    # --- Récupérer les joueurs visibles ---
    players = driver.find_elements(By.CSS_SELECTOR, "span.personCardCell__infos")
    for p in players:
        try:
            name = p.find_element(By.CSS_SELECTOR, "span.personCardCell__name").text.strip()
            position = p.find_element(By.CSS_SELECTOR, "span.personCardCell__description").text.strip()
            if {"Name": name, "Position": position} not in players_data:
                players_data.append({"Name": name, "Position": position})
        except:
            continue

    # --- Chercher le bouton "Afficher plus" par texte ---
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Afficher plus')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)
        load_more.click()
        time.sleep(2)  # attendre le chargement
    except TimeoutException:
        break  # plus de bouton → tous les joueurs sont chargés

driver.quit()

# --- Sauvegarder CSV ---
df = pd.DataFrame(players_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Extraction terminée. {len(players_data)} joueurs enregistrés dans '{CSV_PATH}'")






# --- Config ---
URL = "https://www.footmercato.net/france/ligue-1/2023-2024/joueur"
OUTDIR = "datas"
os.makedirs(OUTDIR, exist_ok=True)
CSV_PATH = os.path.join(OUTDIR, "ligue_1_players_positions.csv")

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(5)

players_data = []

while True:
    # --- Récupérer les joueurs visibles ---
    players = driver.find_elements(By.CSS_SELECTOR, "span.personCardCell__infos")
    for p in players:
        try:
            name = p.find_element(By.CSS_SELECTOR, "span.personCardCell__name").text.strip()
            position = p.find_element(By.CSS_SELECTOR, "span.personCardCell__description").text.strip()
            if {"Name": name, "Position": position} not in players_data:
                players_data.append({"Name": name, "Position": position})
        except:
            continue

    # --- Chercher le bouton "Afficher plus" par texte ---
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Afficher plus')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)
        load_more.click()
        time.sleep(2)  # attendre le chargement
    except TimeoutException:
        break  # plus de bouton → tous les joueurs sont chargés

driver.quit()

# --- Sauvegarder CSV ---
df = pd.DataFrame(players_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Extraction terminée. {len(players_data)} joueurs enregistrés dans '{CSV_PATH}'")





# --- Config ---
URL = "https://www.footmercato.net/italie/serie-a/2023-2024/joueur"
OUTDIR = "datas"
os.makedirs(OUTDIR, exist_ok=True)
CSV_PATH = os.path.join(OUTDIR, "serie_a_players_positions.csv")

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(5)

players_data = []

while True:
    # --- Récupérer les joueurs visibles ---
    players = driver.find_elements(By.CSS_SELECTOR, "span.personCardCell__infos")
    for p in players:
        try:
            name = p.find_element(By.CSS_SELECTOR, "span.personCardCell__name").text.strip()
            position = p.find_element(By.CSS_SELECTOR, "span.personCardCell__description").text.strip()
            if {"Name": name, "Position": position} not in players_data:
                players_data.append({"Name": name, "Position": position})
        except:
            continue

    # --- Chercher le bouton "Afficher plus" par texte ---
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Afficher plus')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)
        load_more.click()
        time.sleep(2)  # attendre le chargement
    except TimeoutException:
        break  # plus de bouton → tous les joueurs sont chargés

driver.quit()

# --- Sauvegarder CSV ---
df = pd.DataFrame(players_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Extraction terminée. {len(players_data)} joueurs enregistrés dans '{CSV_PATH}'")






# --- Config ---
URL = "https://www.footmercato.net/espagne/liga/2023-2024/joueur"
OUTDIR = "datas"
os.makedirs(OUTDIR, exist_ok=True)
CSV_PATH = os.path.join(OUTDIR, "liga_players_positions.csv")

# --- Selenium Setup ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1366,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL)
time.sleep(5)

players_data = []

while True:
    # --- Récupérer les joueurs visibles ---
    players = driver.find_elements(By.CSS_SELECTOR, "span.personCardCell__infos")
    for p in players:
        try:
            name = p.find_element(By.CSS_SELECTOR, "span.personCardCell__name").text.strip()
            position = p.find_element(By.CSS_SELECTOR, "span.personCardCell__description").text.strip()
            if {"Name": name, "Position": position} not in players_data:
                players_data.append({"Name": name, "Position": position})
        except:
            continue

    # --- Chercher le bouton "Afficher plus" par texte ---
    try:
        load_more = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Afficher plus')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more)
        time.sleep(1)
        load_more.click()
        time.sleep(2)  # attendre le chargement
    except TimeoutException:
        break  # plus de bouton → tous les joueurs sont chargés

driver.quit()

# --- Sauvegarder CSV ---
df = pd.DataFrame(players_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Extraction terminée. {len(players_data)} joueurs enregistrés dans '{CSV_PATH}'")