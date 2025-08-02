import pandas as pd
import requests
from datetime import datetime, timedelta

# Bugün hangi gün?
bugun = datetime.today()
hafta_gunu = bugun.weekday()  # Pazartesi=0, Pazar=6

# Eğer Cumartesi (5) ise 1 gün geri git → Cuma
# Eğer Pazar (6) ise 2 gün geri git → Cuma
if hafta_gunu == 5:
    hedef_gun = bugun - timedelta(days=1)
elif hafta_gunu == 6:
    hedef_gun = bugun - timedelta(days=2)
else:
    hedef_gun = bugun

tarih_str = hedef_gun.strftime("%Y-%m-%d")

# TEFAS API ayarları
url = "https://www.tefas.gov.tr/api/DB/ExportFundHistoricalData"
payload = {
    "startDate": tarih_str,
    "endDate": tarih_str,
    "fundCode": ""  # Tüm fonlar
}
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

try:
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 200 and r.text.strip():
        df = pd.DataFrame(r.json())
        if df.empty:
            print("⚠️ Veri boş geldi, yine de CSV oluşturuluyor.")
        df.to_csv("tefas_gunluk.csv", index=False)
        print(f"✅ {tarih_str} verisi başarıyla kaydedildi.")
    else:
        print(f"❌ Yanıt hatalı: {r.status_code}, içerik: {r.text[:100]}")
        pd.DataFrame().to_csv("tefas_gunluk.csv", index=False)
except Exception as e:
    print("❌ Beklenmeyen hata:", e)
    pd.DataFrame().to_csv("tefas_gunluk.csv", index=False)
