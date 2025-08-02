from tefas import Crawler
import pandas as pd
import datetime
import os
import subprocess

try:
    crawl = Crawler()
    data = crawl.fetch()
    df = pd.DataFrame(data)

    if df.empty:
        print("❌ TEFAS verisi tamamen boş.")
        open("tefas_gunluk.csv", "w").close()
        exit(0)

    # 🧠 Son işlem günü verilerini filtrele
    df["date"] = pd.to_datetime(df["date"])
    son_tarih = df["date"].max()
    df = df[df["date"] == son_tarih]

    df.to_csv("tefas_gunluk.csv", index=False, encoding="utf-8-sig")
    print(f"✅ TEFAS verisi yazıldı: {son_tarih.date()}")

except Exception as e:
    print(f"❌ Hata oluştu: {e}")
    open("tefas_gunluk.csv", "w").close()
    exit(0)

# 🔁 Git işlemleri
if os.path.exists("tefas_gunluk.csv") and os.path.getsize("tefas_gunluk.csv") > 0:
    try:
        subprocess.run("git config --global user.name 'GitHub Action'", shell=True, check=True)
        subprocess.run("git config --global user.email 'action@github.com'", shell=True, check=True)
        subprocess.run("git add tefas_gunluk.csv", shell=True, check=True)
        subprocess.run(f'git commit -m "TEFAS verisi güncellendi: {datetime.datetime.utcnow()}"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        print("✅ GitHub'a yüklendi.")
    except subprocess.CalledProcessError:
        print("ℹ️ Dosyada değişiklik yok.")
else:
    print("⚠️ CSV dosyası boş, push yapılmadı.")
