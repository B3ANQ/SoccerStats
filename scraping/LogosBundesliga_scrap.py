#!/usr/bin/env python3
"""
scrape_ligue1_logos_selenium.py
Usage: python scrape_ligue1_logos_selenium.py
Dépendances:
  pip install selenium webdriver-manager requests
(Si échec avec Chrome, tu peux remplacer par Firefox/geckodriver)
"""
import os
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Config ---
URL = "https://www.footmercato.net/allemagne/bundesliga/2023-2024/classement"
OUTDIR = os.path.join("logos", "bundesliga")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LogoScraper/1.0)"}
RATE_LIMIT_SEC = 0.4
SCROLL_PAUSE = 0.6  # temps entre scrolls
MAX_SCROLLS = 12

# --- Helpers ---
def safe_filename(name: str) -> str:
    name = re.sub(r"[^\w\-_\. ]", "_", name or "inconnu")
    return name.strip()[:120]

def ext_from_content_type(ct: str) -> str:
    if not ct:
        return ".img"
    ct = ct.lower()
    if "svg" in ct:
        return ".svg"
    if "png" in ct:
        return ".png"
    if "jpeg" in ct or "jpg" in ct:
        return ".jpg"
    if "gif" in ct:
        return ".gif"
    if "webp" in ct:
        return ".webp"
    return ".img"

def download_image(url: str, outpath: str) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=20)
        r.raise_for_status()
        with open(outpath, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ! Erreur téléchargement {url}: {e}")
        return False

def choose_from_srcset(srcset: str) -> str:
    # prend l'URL la plus haute résolution dans srcset
    if not srcset:
        return ""
    parts = [p.strip() for p in srcset.split(",") if p.strip()]
    # chaque part: "url [Nw]" ou "url"
    last = parts[-1]
    url = last.split()[0]
    return url

# --- Extraction via Selenium ---
def extract_logos_with_selenium(page_url: str):
    options = Options()
    # headless stable mode (Chrome >= 109). Si problème, enlever "--headless=new"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1366,1200")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(page_url)

        # attendre que le tableau (ou un élément central) soit présent
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table, .table, tr"))
            )
        except Exception:
            # on continue quand même, la page peut prendre plus longtemps
            pass

        # Scroll progressif pour forcer lazy-loading
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(MAX_SCROLLS):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(SCROLL_PAUSE)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(1.0)  # petit buffer après scrolls

        # Sélecteurs candidats (essayer plusieurs)
        selectors = [
            "td.team img",        # ancien selector
            "img.team-logo",      # classes fréquentes
            "table img",          # toutes les images dans le tableau
            ".team img",
            ".club img",
            "img"
        ]

        found = []
        seen_srcs = set()

        for sel in selectors:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in elems:
                try:
                    # obtenir src / data-src / srcset
                    src = el.get_attribute("src") or el.get_attribute("data-src") or el.get_attribute("data-lazy")
                    if not src:
                        srcset = el.get_attribute("srcset")
                        if srcset:
                            src = choose_from_srcset(srcset)
                    # si src reste vide, essayer style background-image du parent
                    if not src:
                        parent = el.find_element(By.XPATH, "./ancestor::td | ./ancestor::div | ./ancestor::a")
                        if parent:
                            bg = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundImage", parent)
                            if bg and bg != "none":
                                # bg = 'url("https://...")'
                                m = re.search(r'url\\([\"\']?(.*?)[\"\']?\\)', bg) or re.search(r'url\\((.*?)\\)', bg)
                                if m:
                                    src = m.group(1)
                                else:
                                    # simple strip url(...)
                                    src = bg.replace('url(', '').replace(')', '').replace('"', '').replace("'", "")
                    if not src:
                        continue

                    # ignorer images inline base64 (optionnel)
                    if src.startswith("data:"):
                        continue

                    # rendre absolue
                    src_abs = urljoin(page_url, src)

                    if src_abs in seen_srcs:
                        continue
                    seen_srcs.add(src_abs)

                    # trouver le nom de l'équipe : chercher texte du lien parent ou un élément .team-name
                    team_name = ""
                    try:
                        td = el.find_element(By.XPATH, "./ancestor::td")
                        if td:
                            try:
                                name_el = td.find_element(By.CSS_SELECTOR, ".team-name")
                                team_name = name_el.text.strip()
                            except Exception:
                                # fallback : texte du lien s'il existe
                                try:
                                    a = td.find_element(By.CSS_SELECTOR, "a")
                                    team_name = a.text.strip()
                                except Exception:
                                    team_name = td.text.strip()
                    except Exception:
                        # autre fallback : texte du parent a/ div
                        try:
                            a = el.find_element(By.XPATH, "./ancestor::a")
                            team_name = a.text.strip()
                        except Exception:
                            team_name = el.get_attribute("alt") or el.get_attribute("title") or ""

                    found.append({"team": team_name or "Inconnu", "src": src_abs})
                except Exception:
                    # ignore element issues
                    continue
            # si on a trouvé des logos plausibles, ne pas continuer à chercher tous les sélecteurs
            if len(found) >= 18:  # il y a 18-20 équipes; on limite quand on a assez
                break

        return found
    finally:
        driver.quit()


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    print("Chargement et rendu de la page (Selenium)...")
    logos = extract_logos_with_selenium(URL)

    if not logos:
        print("⚠️ Aucun logo détecté — même avec Selenium. Deux options :")
        print("  1) Je te fournis une version qui visite chaque page d'équipe pour récupérer le logo.")
        print("  2) Tu peux me donner un extrait du HTML rendu (ou m'autoriser à essayer d'extraire ici).")
        return

    print(f"✅ {len(logos)} images candidates trouvées. Démarrage du téléchargement...\n")
    for i, item in enumerate(logos, 1):
        team = safe_filename(item["team"])
        src = item["src"]

        # deviner extension
        parsed = urlparse(src)
        ext = os.path.splitext(parsed.path)[1]
        if not ext or len(ext) > 5:
            # HEAD request rapide
            try:
                h = requests.head(src, headers=HEADERS, timeout=10, allow_redirects=True)
                ext = ext_from_content_type(h.headers.get("Content-Type", ""))
            except Exception:
                ext = ".png"

        outpath = os.path.join(OUTDIR, f"{team}{ext}")
        base, extension = os.path.splitext(outpath)
        j = 1
        while os.path.exists(outpath):
            outpath = f"{base}_{j}{extension}"
            j += 1

        print(f"[{i}/{len(logos)}] {team} -> {outpath}")
        if download_image(src, outpath):
            time.sleep(RATE_LIMIT_SEC)

    print("\nTerminé. Les logos sont dans :", os.path.abspath(OUTDIR))


main()