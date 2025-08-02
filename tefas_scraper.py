import pandas as pd
import requests
import datetime

# En yakın iş gününü döner (bugün, dün, önceki gün diye gider)
def get_last_business_day():
    today = datetime.date.today()
    while today.weekday() >= 5:  # Cumartesi (5) veya Pazar (6) ise geri git
        today -= datetime.timedelta(days=1)
    return today

# Tarihi string formatına çevir (örnek: 20250802)
def date_to_str(date_obj):
    return date_obj.strftime('%Y%m%d')

# En son iş günü tarihi
date = get_last_business_day()
date_str = date_to_str(date)

# TEFAS API uç noktası
url = f"https://www.tefas.gov.tr/api/DB/OnlineFundData?date={date_str}"

# Veri isteği
r = requests.get(url)
try:
    data = r.json()
except:
    print("Veri alınamadı veya JSON hatası!")
    data = []

# Veriyi DataFrame’e çevir
df = pd.DataFrame(data)

# Eğer veri boşsa, CSV oluşturma
if df.empty:
    print(f"❌ Uyarı: TEFAS verisi alınamadı veya veri boş geldi ({date_str})")
else:
    # Eğer beklenen sütunlar varsa sadece o sütunları al
    expected_columns = {"code", "title", "date", "unitPrice"}
    if expected_columns.issubset(df.columns):
        df = df[["code", "title", "date", "unitPrice"]]
        df.columns = ["Kod", "Fon Ünvanı", "Tarih", "Birim Pay Değeri"]
        df.to_csv("tefas_gunluk.csv", index=False, encoding="utf-8-sig")
        print("✅ TEFAS verisi başarıyla kaydedildi.")
    else:
        print(f"⚠️ Beklenen sütunlar yok, veri formatı değişmiş olabilir.")
