import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# TEFAS API URL
url = "https://www.tefas.gov.tr/api/DB/AllFundDailyValues"

# En son veri tarihini bulmak için denenecek maksimum gün sayısı
max_days = 5
success = False

for i in range(max_days):
    tarih = (datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d")
    print(f"🔄 Veri deneniyor: {tarih}")
    
    try:
        response = requests.get(url, params={"date": tarih}, timeout=30)
        
        if response.status_code == 200 and response.content.strip():
            try:
                data = response.json()
                df = pd.DataFrame(data)
                
                if not df.empty:
                    df = df[["code", "title", "date", "unitPrice"]]
                    df.to_csv("tefas_gunluk.csv", index=False)
                    print(f"✅ Veri başarıyla kaydedildi: {tarih}")
                    success = True
                    break
                else:
                    print(f"⚠️ {tarih} için veri boş geldi.")
            except Exception as e:
                print(f"❌ JSON hatası ({tarih}): {e}")
        else:
            print(f"⚠️ HTTP Yanıtı boş veya hatalı ({response.status_code})")
    
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
    
    time.sleep(1)

if not success:
    print("❌ Son 5 güne ait veri bulunamadı. Yine de başlıklar yazılıyor.")
    with open("tefas_gunluk.csv", "w") as f:
        f.write("code,title,date,unitPrice\n")
