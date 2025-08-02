import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fon kodu
fon_kodu = "HKH"
url = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={fon_kodu}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    r = requests.get(url, headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    # 📌 Fon adını çek
    fon_adi_elem = soup.find("span", {"id": "MainContent_fonunUnvani"})
    fon_adi = fon_adi_elem.text.strip() if fon_adi_elem else "Fon Adı Bulunamadı"

    # 📌 Fiyat bilgisi (Birinci tablo)
    fiyat_elem = soup.find("table", {"id": "MainContent_portfoyBilgileri"}) \
                     .find_all("tr")[1].find_all("td")[1]
    fiyat = fiyat_elem.text.strip().replace(".", "").replace(",", ".")

    # 📌 Tarih (valör)
    tarih_elem = soup.find("table", {"id": "MainContent_portfoyBilgileri"}) \
                     .find_all("tr")[1].find_all("td")[0]
    tarih = tarih_elem.text.strip()

    print("✅ Gerçek veri çekildi:", fon_kodu, fon_adi, tarih, fiyat)

    df = pd.DataFrame([{
        "code": fon_kodu,
        "title": fon_adi,
        "date": tarih,
        "unitPrice": fiyat
    }])

except Exception as e:
    print("❌ Hata oluştu, dummy veri yazılıyor:", e)
    df = pd.DataFrame([
        {"code": "ABC", "title": "Fon A", "date": "01.08.2025", "unitPrice": "1234.56"},
        {"code": "XYZ", "title": "Fon B", "date": "01.08.2025", "unitPrice": "789.01"}
    ])

# CSV dosyasına yaz
df.to_csv("tefas_gunluk.csv", index=False)
