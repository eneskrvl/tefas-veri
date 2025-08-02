import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv

def fetch_tefas_html(date_str):
    try:
        url = f"https://www.tefas.gov.tr/FonKarsilastirma.aspx?tarih={date_str}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and "dataTable" in r.text:
            return r.text
    except Exception as e:
        print(f"Hata oluştu: {e}")
    return None

def parse_html_and_save(html, fallback=False):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one(".dataTable tbody")
    if not table:
        return False

    rows = table.select("tr")
    if len(rows) == 0:
        return False

    data = []
    for row in rows:
        try:
            code = row.select_one("td.fonkodu").text.strip()
            title = row.select_one("td.fonunvani").text.strip()
            date = row.select_one("td.tarih").text.strip()
            unit_price = row.select_one("td.tutar").text.strip().replace(".", "").replace(",", ".")
            data.append([code, title, date, unit_price])
        except:
            continue

    if data:
        with open("tefas_gunluk.csv", mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["code", "title", "date", "unitPrice"])
            writer.writerows(data)
        print("✅ Veri kaydedildi.")
        return True
    return False

# 1. Gerçek veriyi dene (bugünden geriye doğru 5 gün dene)
for i in range(0, 5):
    target_date = (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d.%m.%Y")
    print(f"⏳ Veri deneniyor: {target_date}")
    html = fetch_tefas_html(target_date)
    if html and parse_html_and_save(html):
        break
else:
    print("⚠️ Gerçek veri yok, örnek veri yazılıyor...")
    # Dummy HTML kullan
    dummy_html = """
    <table class="dataTable">
        <tbody>
            <tr>
                <td class="fonkodu">ABC</td>
                <td class="fonunvani">Fon A</td>
                <td class="tarih">01.08.2025</td>
                <td class="tutar">1.234,56</td>
            </tr>
            <tr>
                <td class="fonkodu">XYZ</td>
                <td class="fonunvani">Fon B</td>
                <td class="tarih">01.08.2025</td>
                <td class="tutar">789,01</td>
            </tr>
        </tbody>
    </table>
    """
    parse_html_and_save(dummy_html, fallback=True)
