import requests

def is_website_alive(url):
    try:
        resp = requests.head(url, timeout=3, allow_redirects=True)
        return resp.status_code < 400
    except Exception:
        return False

def load_wordlist(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception as e:
        print(f"[dirb] Erreur chargement wordlist : {e}")
        return []

def scan_dirb(base_url, wordlist):
    found = []
    print(f"[dirb] Scan en cours sur {base_url} avec {len(wordlist)} mots...")
    for word in wordlist:
        url = f"{base_url.rstrip('/')}/{word}"
        try:
            resp = requests.get(url, timeout=5, allow_redirects=True)
            if resp.status_code < 400:
                print(f"[dirb] {url} (HTTP {resp.status_code})")
                found.append((url, resp.status_code))
        except requests.RequestException:
            pass
    return found

def run(target):
    if not target.startswith("http://") and not target.startswith("https://"):
        base_url = "http://" + target
    else:
        base_url = target

    if not is_website_alive(base_url):
        print(f"[dirb] Le site {base_url} ne semble pas accessible, scan annulé.")
        return []

    wordlist_path = input("Entrez le chemin vers la wordlist à utiliser : ").strip()
    if not wordlist_path:
        print("[dirb] Aucun chemin fourni, scan annulé.")
        return []

    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        print("[dirb] Wordlist vide ou introuvable, scan annulé.")
        return []

    return scan_dirb(base_url, wordlist)
