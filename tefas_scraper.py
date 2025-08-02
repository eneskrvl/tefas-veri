import requests
import pandas as pd
import datetime
import os
import subprocess

# 📅 Bugün hafta sonuysa Cuma'ya çek
bugun = datetime.date.today()
if bugun.weekday() == 5:  # Cumartesi
    bugun -= datetime.timedelta(days=1)
elif bugun.weekday() == 6:  # Pazar
    bugun -= datetime.timedelta(days=2)

tarih = bugun.strftime("%Y%m%d")
url = f"https://www.tefas.gov.tr/api/DB/BindFundData?date={tarih}"

try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data)

    # Beklenen sütunlar var mı kontrol et
    expected_cols = {"code", "title", "date", "unitPrice"}
    if expected_cols.issubset(df.columns):
        df = df[["code", "title", "date", "unitPrice"]]
        df.columns = ["Kod", "Fon Ünvanı", "Tarih", "Birim Pay Değeri"]
        df.to_csv("tefas_gunluk.csv", index=False, encoding="utf-8-sig")
        print("✅ Veri başarıyla kaydedildi.")
    else:
        print("⚠️ TEFAS verisi geldi ama beklenen sütunlar yok.")
        open("tefas_gunluk.csv", "w").close()  # boş dosya
        exit(0)

except Exception as e:
    print(f"❌ Veri çekilirken hata oluştu: {e}")
    open("tefas_gunluk.csv", "w").close()
    exit(0)

# ✅ Dosya varsa ve boş değilse commit + push
if os.path.exists("tefas_gunluk.csv") and os.path.getsize("tefas_gunluk.csv") > 0:
    try:
        subprocess.run("git config --global user.name 'GitHub Action'", shell=True, check=True)
        subprocess.run("git config --global user.email 'action@github.com'", shell=True, check=True)
        subprocess.run("git add tefas_gunluk.csv", shell=True, check=True)
        subprocess.run(f'git commit -m "TEFAS verisi güncellendi: {datetime.datetime.utcnow()}"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        print("✅ GitHub'a yüklendi.")
    except subprocess.CalledProcessError:
        print("ℹ️ Dosya değişmemiş olabilir, commit yapılmadı.")
else:
    print("⚠️ tefas_gunluk.csv dosyası boş, push yapılmadı.")
