import pandas as pd
import requests
from datetime import datetime

fon_kodlari = []  # ["HKH", "AFT"] gibi kısıtlayabilirsin

tefas_url = "https://www.tefas.gov.tr/api/DB/ExportFundHistoricalData"
today = datetime.today().strftime('%Y-%m-%d')

payload = {
    "startDate": today,
    "endDate": today,
    "fundCode": "",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.post(tefas_url, json=payload, headers=headers)

# Eğer TEFAS'tan veri gelmezse hata verme
try:
    data = r.json()
    df = pd.DataFrame(data)
except Exception as e:
    df = pd.DataFrame(columns=["Fon Kodu", "Fon Ünvanı", "Tarih", "Fiyat"])
    print("TEFAS verisi alınamadı:", e)

if fon_kodlari:
    df = df[df['Fon Kodu'].isin(fon_kodlari)]

df.to_csv("tefas_gunluk.csv", index=False)
