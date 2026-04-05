import requests
import time

BOT_TOKEN = "8632434112:AAEFcPN2Ggk8aeKJlGFxaRYbFZWNDD6-_OQ"
CHAT_ID = "6217314338"

def mesaj_gonder(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def maclari_cek():
    url = "https://www.fotmob.com/api/matches?timezone=Europe/Istanbul"
    data = requests.get(url).json()
    
    maclar = []
    
    for lig in data["leagues"]:
        for mac in lig["matches"]:
            if mac.get("status", {}).get("finished") == False:
                
                ev = mac["home"]["name"]
                dep = mac["away"]["name"]
                skor = mac["score"]
                dakika = mac["status"].get("liveTime", {}).get("short", "")
                
                maclar.append({
                    "ev": ev,
                    "dep": dep,
                    "skor": skor,
                    "dk": dakika
                })
    
    return maclar

def analiz(mac):
    try:
        gol = int(mac["skor"].split("-")[0]) + int(mac["skor"].split("-")[1])
    except:
        return None

    # DÜŞÜK KRİTER (HER MAÇ)
    if gol >= 1:
        mesaj = f"""
⚽ {mac['ev']} vs {mac['dep']}
⏱ {mac['dk']} | {mac['skor']}

🔥 GOL BEKLENİYOR!

📊 ANALİZ:
🏠 Ev sahibi gol atar
🚗 Deplasman gol atar
🚩 Korner gelebilir
🏆 Kazanan çıkabilir

📈 Güven: %{50 + gol}
"""
        return mesaj
    
    return None

def main():
    gonderilen = set()
    
    while True:
        try:
            maclar = maclari_cek()
            
            for mac in maclar:
                key = mac["ev"] + mac["dep"] + mac["skor"]
                
                if key not in gonderilen:
                    mesaj = analiz(mac)
                    
                    if mesaj:
                        mesaj_gonder(mesaj)
                        gonderilen.add(key)
            
            time.sleep(60)

        except Exception as e:
            print("HATA:", e)
            time.sleep(60)

if __name__ == "__main__":
    mesaj_gonder("🚀 CANLI MAÇ BOTU AKTİF")
    main()
