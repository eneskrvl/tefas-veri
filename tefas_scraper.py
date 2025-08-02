import pandas as pd
import requests
from datetime import datetime

fon_kodlari = []  # Boşsa tüm fonları çeker; istersen ["HKH", "AFT"] gibi sınırlayabilirsin

tefas_url = "https://www.tefas.gov.tr/api/DB/ExportFundHistoricalData"

today = datetime.today().strftime('%Y-%m-%d')

payload = {
    "startDate": today,
    "endDate": today,
    "fundCode": "",
}

r = requests.post(tefas_url, json=payload)
df = pd.DataFrame(r.json())

if fon_kodlari:
    df = df[df['Fon Kodu'].isin(fon_kodlari)]

df.to_csv("tefas_gunluk.csv", index=False)
