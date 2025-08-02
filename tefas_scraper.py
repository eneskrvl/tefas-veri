# tefas_scraper.py

import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime

async def get_fund_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod=HKH"
        await page.goto(url, timeout=60000)

        # Sayfa tamamen yüklensin diye bekle
        await page.wait_for_selector("#MainContent_PanelPortfoy", timeout=30000)

        try:
            title = await page.inner_text("#MainContent_lblFonUnvani")
            price = await page.inner_text("#MainContent_FonFiyatBilgi1_lblFiyat")
            date = await page.inner_text("#MainContent_FonFiyatBilgi1_lblTarih")
        except Exception as e:
            print("Veri alınamadı:", e)
            await browser.close()
            return

        df = pd.DataFrame([{
            "code": "HKH",
            "title": title.strip(),
            "date": date.strip(),
            "unitPrice": price.strip()
        }])

        df.to_csv("tefas_gunluk.csv", index=False)
        print("✅ Veri kaydedildi.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_fund_data())
