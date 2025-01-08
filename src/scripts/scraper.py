import zendriver as zd
import asyncio
import logging
from scripts.casinopt import CasinoPortugal_Sportrequest
from scripts.lebull import Lebull_Sportrequest
from scripts.betano import Betano_Sportrequest
from scripts.bwin import Bwin_Sportrequest

async def main():
    logging.basicConfig(filename="logs/log.log", filemode='a', format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    browser = await zd.start()
    page = await browser.get('about:blank')
    
    casino = CasinoPortugal_Sportrequest.CasinoPT_Request(page)
    betano = Betano_Sportrequest.Betano_Request(page)
    lebull = Lebull_Sportrequest.Lebull_Request(page)
    bwin = Bwin_Sportrequest.Bwin_Request(page)

    try:
        await lebull.run()
    except Exception:
        logging.exception("Lebull")
    logging.info("Lebull finished scraping")
        
    try:
        await casino.run()
    except Exception:
        logging.exception("Casino")
    logging.info("CasinoPT finished scraping")
        
    try:
        await bwin.run()
    except Exception:
        logging.exception("Bwin")
    logging.info("Bwin finished scraping")
        
    try:
        await betano.run()
    except Exception:
        logging.exception("Betano")
    logging.info("Betano finished scraping")
  
    await browser.stop()
    logging.info("Scraping Done.")

if __name__ == "__main__":
    asyncio.run(main())