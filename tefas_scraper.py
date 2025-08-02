import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_tefas_data(date_str):
    url = "https://www.tefas.gov.tr/api/DB/ExchangeTradedFunds"
    payload = {
        "date": date_str
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        data = r.json()
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            df = df[["code", "title", "date", "unitPrice"]]
            return df
    except Exception as e:
        print(f"{date_str} için veri alınamadı. Hata: {e}")
    return None

# Bugün + geri günler (maksimum 5 gün geriye dön)
for i in range(5):
    date_try = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
    df = fetch_tefas_data(date_try)
    if df is not None:
        df.to_csv("tefas_gunluk.csv", index=False)
        print(f"Veri bulundu: {date_try} ({len(df)} satır)")
        break
else:
    print("Hiçbir günde veri bulunamadı.")
