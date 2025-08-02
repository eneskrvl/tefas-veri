import requests
import pandas as pd
import datetime
import os
import subprocess

# 📅 Bugün hafta sonuysa son iş gününü (Cuma) bul
bugun = datetime.date.today()
if bugun.weekday() == 5:  # Cumartesi
    bugun = bugun - datetime.timedelta(days=1)
elif bugun.weekday() == 6:  # Pazar
    bugun = bugun - datetime.timedelta(days=2)

# 📆 Formatla: 20250802 gibi (yıl + ay + gün)
tarih = bugun.strftime("%Y%m%d")

# 🔗 TEFAS API URL (tarihe göre veri çeker)
url = f"https://www.tefas.gov.tr/api/DB/BindFundData?date={tarih}"

try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()  # HTTP hatası varsa fırlat

    data = r.json()
    df = pd.DataFrame(data)

    # 📌 Sadece şu sütunları al
    df = df[["code", "title", "date", "unitPrice"]]

    # 💾 CSV'ye yaz
    df.to_csv("tefas_gunluk.csv", index=False)
    print("✅ Veri başarıyla çekildi ve kaydedildi.")

except Exception as e:
    print(f"❌ Veri çekilirken hata oluştu: {e}")
    open("tefas_gunluk.csv", "w").close()  # boş dosya oluştur
    exit(1)

# ✅ Dosya varsa ve boş değilse git işlemlerini yap
if os.path.exists("tefas_gunluk.csv") and os.path.getsize("tefas_gunluk.csv") > 0:
    try:
        subprocess.run("git config --global user.name 'GitHub Action'", shell=True, check=True)
        subprocess.run("git config --global user.email 'action@github.com'", shell=True, check=True)
        subprocess.run("git add tefas_gunluk.csv", shell=True, check=True)
        subprocess.run(f'git commit -m "TEFAS verisi güncellendi: {datetime.datetime.utcnow()}"', shell=True, check=True)
        subprocess.run("git push", shell=True, check=True)
        print("✅ Değişiklikler GitHub'a yüklendi.")
    except subprocess.CalledProcessError:
        print("⚠️ Dosyada değişiklik yok, git commit yapılmadı.")
else:
    print("⚠️ tefas_gunluk.csv dosyası boş, push yapılmadı.")
