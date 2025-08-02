import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime
import os

OUTPUT_FILE = "tefas_gunluk.csv"
FUND_CODE = "HKH"
TEFAS_URL = f"https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod={FUND_CODE}"

async def get_fund_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print(f"Sayfa açılıyor: {TEFAS_URL}")
        await page.goto(TEFAS_URL, timeout=60000)

        try:
            await page.wait_for_selector("#MainContent_PanelPortfoy", timeout=60000)
            print("Sayfa yüklendi.")
        except Exception as e:
            print(f"Sayfa yüklenemedi: {e}")
            await browser.close()
            raise

        try:
            price = await page.inner_text("#MainContent_lblFonFiyat")
            date = await page.inner_text("#MainContent_lblFiyatTarih")
            name = await page.inner_text("#MainContent_lblFonUnvan")

            df = pd.DataFrame([{
                "code": FUND_CODE,
                "title": name.strip(),
                "date": date.strip(),
                "unitPrice": price.strip()
            }])

            df.to_csv(OUTPUT_FILE, index=False)
            print("Veri başarıyla CSV'ye yazıldı.")

        except Exception as e:
            print(f"Veri çekme hatası: {e}")
            await browser.close()
            raise

        await browser.close()

if __name__ == "__main__":
    try:
        asyncio.run(get_fund_data())
    except Exception as e:
        print(f"❌ TEFAS verisi alınamadı: {e}")
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
