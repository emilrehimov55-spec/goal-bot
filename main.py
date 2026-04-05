import requests
import time

BOT_TOKEN = "8632434112:AAEFcPN2Ggk8aeKJlGFxaRYbFZWNDD6-_OQ"
CHAT_ID = "6217314338"

gonderilen = set()

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mesaj
    })

def maclari_getir():
    url = "https://www.fotmob.com/api/matches?date=today"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        data = res.json()
        return data.get("leagues", [])
    except:
        return []

def kontrol_et():
    ligler = maclari_getir()

    for lig in ligler:
        for mac in lig.get("matches", []):
            try:
                mac_id = mac["id"]

                if mac_id in gonderilen:
                    continue

                if mac["status"]["finished"]:
                    continue

                ev = mac["home"]["name"]
                dep = mac["away"]["name"]
                skor = mac["status"].get("scoreStr", "0-0")
                dk = mac["status"].get("liveTime", {}).get("short", "")

                if skor == "1-1":
                    mesaj = f"""
🔥 CANLI MAÇ

⚽ {ev} vs {dep}
⏱ {dk}
📊 Skor: {skor}

🚀 GOL BEKLENİYOR!
"""
                    mesaj_gonder(mesaj)
                    gonderilen.add(mac_id)

            except:
                continue

if __name__ == "__main__":
    mesaj_gonder("🚀 BOT AKTİF")

    while True:
        kontrol_et()
        time.sleep(60)
