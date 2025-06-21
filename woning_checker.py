import requests
from bs4 import BeautifulSoup
import json
import os

# === CONFIG ===
BOT_TOKEN = "7752107069:AAEUKRofwVVDBKdRef14ZKbSoCpD5v6bFc4"
CHAT_ID = "7990264716"

# === Telegram-bericht sturen ===
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Fout bij verzenden Telegram:", e)

# === Data laden en opslaan ===
def load_seen(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_seen(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

# === Funda scraper ===
def check_funda():
    print("▶ Funda controleren...")
    URL = "https://www.funda.nl/zoeken/koop?selected_area=[%22drunen%22]&sort=%22date_down%22"
    DATA_FILE = "seen_funda.json"
    seen = load_seen(DATA_FILE)
    current = []
    new_items = []

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for listing in soup.select("a[data-test-id='object-card-link']"):
        title = listing.get_text(strip=True)
        href = listing.get("href").split("?")[0]
        url = "https://www.funda.nl" + href
        current.append(url)

        if url not in seen:
            new_items.append((title, url))

    for title, url in new_items:
        send_telegram(f"🏡 <b>Nieuw op Funda:</b>\n{title}\n🔗 {url}")

    save_seen(DATA_FILE, current)
    print(f"🔍 Funda: {len(new_items)} nieuw(e) woning(en) gevonden.")

# === AMB scraper ===
def check_amb():
    print("▶ AMB Makelaars controleren...")
    URL = "https://www.amb-makelaars.nl/aanbod/woningaanbod/DRUNEN/koop-huur/"
    DATA_FILE = "seen_amb.json"
    seen = load_seen(DATA_FILE)
    current = []
    new_items = []

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for div in soup.select("div.object-title > a"):
        title = div.get_text(strip=True)
        url = "https://www.amb-makelaars.nl" + div.get("href")
        current.append(url)

        if url not in seen:
            new_items.append((title, url))

    for title, url in new_items:
        send_telegram(f"🏘️ <b>Nieuw bij AMB:</b>\n{title}\n🔗 {url}")

    save_seen(DATA_FILE, current)
    print(f"🔍 AMB: {len(new_items)} nieuw(e) woning(en) gevonden.")

# === Staete scraper ===
def check_staete():
    print("▶ Staete Makelaars controleren...")
    URL = "https://www.staete.nl/aanbod/?Woonplaats=drunen"
    DATA_FILE = "seen_staete.json"
    seen = load_seen(DATA_FILE)
    current = []
    new_items = []

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for card in soup.select("a.property-card"):
        title = card.get_text(strip=True).split("€")[0]
        url = "https://www.staete.nl" + card.get("href")
        current.append(url)

        if url not in seen:
            new_items.append((title.strip(), url))

    for title, url in new_items:
        send_telegram(f"🏠 <b>Nieuw bij Staete:</b>\n{title}\n🔗 {url}")

    save_seen(DATA_FILE, current)
    print(f"🔍 Staete: {len(new_items)} nieuw(e) woning(en) gevonden.")

# === Main-run ===
if __name__ == "__main__":
    check_funda()
    check_amb()
    check_staete()
