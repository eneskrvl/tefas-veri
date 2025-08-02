import pandas as pd
import requests
from datetime import datetime

# TEFAS API URL'si
tefas_url = "https://www.tefas.gov.tr/api/DB/ExportFundHistoricalData"

# Bugünün tarihi (başlangıç ve bitiş için aynı gün)
bugun = datetime.today().strftime("%Y-%m-%d")

# API isteği için veri
payload = {
    "startDate": bugun,
    "endDate": bugun,
    "fundCode": ""  # Boş bırakınca tüm fonlar gelir
}

# Bot olarak algılanmamak için başlık bilgileri
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# POST isteği gönder
r = requests.post(tefas_url, json=payload, headers=headers)

# Yanıt başarılıysa ve boş değilse veriyi işle
if r.status_code == 200 and r.text.strip():
    try:
        df = pd.DataFrame(r.json())
        df.to_csv("tefas_gunluk.csv", index=False)
        print("✅ Veri başarıyla çekildi ve tefas_gunluk.csv dosyasına kaydedildi.")
    except Exception as e:
        print("⚠️ JSON verisi çözümlenemedi:", e)
else:
    print(f"❌ Hatalı yanıt: {r.status_code}, içerik: {r.text[:100]}")
