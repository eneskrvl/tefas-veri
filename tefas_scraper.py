import requests
import pandas as pd
from datetime import datetime, timedelta

# En fazla kaç gün geriye gidelim
MAX_GUN_GERI = 5

# Bugünden başlayarak geriye doğru deneyelim
bugun = datetime.now()
basarili = False

for i in range(MAX_GUN_GERI):
    tarih = (bugun - timedelta(days=i)).strftime("%Y-%m-%d")
    print(f"🔍 {tarih} için veri isteniyor...")

    url = f"https://www.tefas.gov.tr/api/DB/OnemliVeriler/GetFonBilgiListe/{tarih}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) == 0:
            print(f"⚠️ {tarih} için veri listesi boş. Bir gün geri gidiliyor...")
            continue

        df = pd.DataFrame(data)

        if not df.empty:
            df_filtered = df[["code", "title", "date", "unitPrice"]]
            df_filtered.to_csv("tefas_gunluk.csv", index=False)
            print(f"✅ {tarih} verisi başarıyla kaydedildi.")
            basarili = True
            break
        else:
            print(f"⚠️ {tarih} için DataFrame boş. Devam ediliyor...")
    except Exception as e:
        print(f"⛔ {tarih} verisi çekilirken hata oluştu: {e}")

if not basarili:
    print(f"❌ Son {MAX_GUN_GERI} günde veri bulunamadı.")
