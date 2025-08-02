import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os

async def get_hkh_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod=HKH")

        try:
            await page.wait_for_selector("#MainContent_portfoyBilgileri", timeout=60000)

            tarih = await page.inner_text("#MainContent_lblTarih")
            fiyat = await page.inner_text("#MainContent_lblBirimPayDegeri")

            data = {
                "code": ["HKH"],
                "title": ["Hedef Portföy Değişken Fon"],
                "date": [tarih],
                "unitPrice": [fiyat.replace(",", ".")]
            }

            df = pd.DataFrame(data)
            df.to_csv("tefas_gunluk.csv", index=False)

            print("✅ CSV oluşturuldu.")
            print("📄 Dosya var mı?:", os.path.exists("tefas_gunluk.csv"))

        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_hkh_data())
