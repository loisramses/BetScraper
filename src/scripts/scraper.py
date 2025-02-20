import zendriver as zd
import asyncio
import logging
from casinopt.CasinoPortugal_Sportrequest import CasinoPT_Request
from lebull.Lebull_Sportrequest import Lebull_Request
from betano.Betano_Sportrequest import Betano_Request
from bwin.Bwin_Sportrequest import Bwin_Request

async def retry(task, name, retries=2):
    for attempt in range(retries):
        try:
            await task()
            logging.info(f"{name} finished scraping")
            return
        except Exception:
            logging.exception(f"{name} attempt {attempt + 1} failed")
    logging.error(f"{name} failed after {retries} attempts")

async def main():
    logging.basicConfig(filename="logs/log.log", filemode='a', format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    browser = await zd.start(browser_executable_path="/snap/bin/chromium", headless=True)
    page = await browser.get('about:blank')
    
    casino = CasinoPT_Request(page)
    betano = Betano_Request(page)
    lebull = Lebull_Request(page)
    bwin = Bwin_Request(page)

    await retry(lebull.run, "Lebull")
    await retry(casino.run, "Casino")
    await retry(bwin.run, "Bwin")
    await retry(betano.run, "Betano")
  
    await browser.stop()
    logging.info("Scraping Done.")

if __name__ == "__main__":
    asyncio.run(main())