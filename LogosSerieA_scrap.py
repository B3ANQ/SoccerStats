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

# --- Configuration ---
URL = "https://www.footmercato.net/italie/serie-a/2023-2024/classement"
OUTDIR = os.path.join("logos", "serie_a")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; LogoScraper/1.0)"}
RATE_LIMIT_SEC = 0.4
SCROLL_PAUSE = 0.5
MAX_SCROLLS = 10

def safe_filename(name: str) -> str:
    """Nettoie un nom d’équipe pour l’utiliser en nom de fichier."""
    name = re.sub(r"[^\w\-_\. ]", "_", name or "inconnu")
    return name.strip()[:120]

def ext_from_content_type(ct: str) -> str:
    """Retourne une extension de fichier à partir du Content-Type HTTP."""
    if not ct:
        return ".img"
    c = ct.lower()
    if "svg" in c:
        return ".svg"
    if "png" in c:
        return ".png"
    if "jpeg" in c or "jpg" in c:
        return ".jpg"
    if "gif" in c:
        return ".gif"
    if "webp" in c:
        return ".webp"
    return ".img"

def download_image(url: str, outpath: str) -> bool:
    """Télécharge l’image à l’URL donnée dans le fichier outpath."""
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
    """Prend la meilleure URL dans un attribut srcset."""
    if not srcset:
        return ""
    parts = [p.strip() for p in srcset.split(",") if p.strip()]
    last = parts[-1]
    url = last.split()[0]
    return url

def extract_logos_with_selenium(page_url: str):
    """Charge la page via Selenium, scroll, et extrait les logos des clubs."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(page_url)
        # attendre que la table ou un élément de club apparaisse
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "td.team img"))
            )
        except Exception:
            pass

        # scroll progressif pour déclencher le lazy load
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(MAX_SCROLLS):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(SCROLL_PAUSE)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        time.sleep(1.0)

        found = []
        seen = set()

        # essayer des sélecteurs pertinents
        selectors = [
            "td.team img",        # cible dans la cellule club
            "img.team-logo",      # class team-logo
            "table img",          # toutes images dans le tableau
            ".club img",
            "img"
        ]

        for sel in selectors:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in elems:
                try:
                    src = el.get_attribute("src") or el.get_attribute("data-src")
                    if not src:
                        srcset = el.get_attribute("srcset")
                        if srcset:
                            src = choose_from_srcset(srcset)
                    if not src:
                        continue
                    if src.startswith("data:"):
                        continue

                    src_abs = urljoin(page_url, src)
                    if src_abs in seen:
                        continue
                    seen.add(src_abs)

                    # déterminer le nom de l’équipe
                    team_name = ""
                    try:
                        td = el.find_element(By.XPATH, "./ancestor::td")
                        if td:
                            try:
                                nm = td.find_element(By.CSS_SELECTOR, ".team-name")
                                team_name = nm.text.strip()
                            except:
                                a = td.find_element(By.CSS_SELECTOR, "a")
                                team_name = a.text.strip() if a else td.text.strip()
                    except:
                        try:
                            a = el.find_element(By.XPATH, "./ancestor::a")
                            team_name = a.text.strip()
                        except:
                            team_name = el.get_attribute("alt") or el.get_attribute("title") or ""

                    found.append({"team": team_name or "Inconnu", "src": src_abs})
                except:
                    continue
            # si on a suffisamment de logos (≈20), on peut arrêter
            if len(found) >= 20:
                break

        return found
    finally:
        driver.quit()

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    print("🔍 Chargement de la page Liga avec Selenium…")
    logos = extract_logos_with_selenium(URL)

    if not logos:
        print("⚠️ Aucun logo détecté même avec Selenium.")
        return

    print(f"✅ {len(logos)} images candidates trouvées. Lancement du téléchargement...\n")

    for idx, item in enumerate(logos, 1):
        team = safe_filename(item["team"])
        src = item["src"]

        parsed = urlparse(src)
        ext = os.path.splitext(parsed.path)[1]
        if not ext or len(ext) > 5:
            # essayer HEAD pour deviner extension
            try:
                h = requests.head(src, headers=HEADERS, allow_redirects=True, timeout=10)
                ext = ext_from_content_type(h.headers.get("Content-Type", ""))
            except:
                ext = ".png"

        fname = f"{team}{ext}"
        outpath = os.path.join(OUTDIR, fname)
        base, extension = os.path.splitext(outpath)
        counter = 1
        while os.path.exists(outpath):
            outpath = f"{base}_{counter}{extension}"
            counter += 1

        print(f"[{idx}/{len(logos)}] {team} → {src}")
        download_image(src, outpath)
        time.sleep(RATE_LIMIT_SEC)

    print("\n🎉 Terminé. Les logos de la Liga sont dans :", os.path.abspath(OUTDIR))

main()