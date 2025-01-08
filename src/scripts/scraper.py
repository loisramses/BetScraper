import zendriver as zd
import asyncio
import logging
from casinopt.CasinoPortugal_Sportrequest import CasinoPT_Request
from lebull.Lebull_Sportrequest import Lebull_Request
from betano.Betano_Sportrequest import Betano_Request
from bwin.Bwin_Sportrequest import Bwin_Request

async def main():
    logging.basicConfig(filename="logs/log.log", filemode='a', format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
    browser = await zd.start()
    page = await browser.get('about:blank')
    
    casino = CasinoPT_Request(page)
    betano = Betano_Request(page)
    lebull = Lebull_Request(page)
    bwin = Bwin_Request(page)

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