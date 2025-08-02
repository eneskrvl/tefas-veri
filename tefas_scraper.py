import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def get_hkh_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.tefas.gov.tr/FonAnaliz.aspx?FonKod=HKH")

        try:
            # Kritik verilerin geldiğinden emin ol
            await page.wait_for_selector("#MainContent_lblTarih", timeout=60000)
            await page.wait_for_selector("#MainContent_lblBirimPayDegeri", timeout=60000)

            tarih = await page.inner_text("#MainContent_lblTarih")
            fiyat = await page.inner_text("#MainContent_lblBirimPayDegeri")

            # Veriyi hazırlayıp CSV'ye yaz
            data = {
                "code": ["HKH"],
                "title": ["Hedef Portföy Değişken Fon"],
                "date": [tarih],
                "unitPrice": [fiyat.replace(",", ".")]
            }

            df = pd.DataFrame(data)
            df.to_csv("tefas_gunluk.csv", index=False)

            print("✅ tefas_gunluk.csv başarıyla oluşturuldu.")
        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(get_hkh_data())
