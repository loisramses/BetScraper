# import nodriver as uc
import zendriver
from rich import print
import asyncio

async def get_option(element: zendriver.Element) -> tuple[str, str]:
    option_name = element.children[0].text
    option_odd = element.children[1].text
    return (option_name, option_odd)

async def get_all_options(element: zendriver.Element):
    options = []
    for col in element.children:
        for child in col.children:
            options.append(await get_option(child))
    return options

async def get_all_bets(page: zendriver.Tab):
    event = {}
    await (await page.select('.filters__list', timeout=20)).children[1].click()
    event_name = (await page.select('.breadcrumb')).children[1].children[-2].children[-2].text
    event[event_name] = {
        'url': page.url,
        'bets': []
    }
    all_bets_e = await page.select_all('div[id^="MarketId"]')
    for bet in all_bets_e:
        bet_name = bet.children[0].children[1].text
        event[event_name]['bets'].append((bet_name, await get_all_options(bet.children[1])))
    return event

async def get_event_bets(url: str, browser: zendriver.Browser, semaphore: asyncio.Semaphore) -> list:
    async with semaphore:    
        page = await browser.get(url, new_window=True)
        bets = await get_all_bets(page)
        await page.close()
        return bets

async def get_all_events_bets(events: list) -> list:
    browser = await zendriver.start(browser_args=['--start-maximized'])
    semaphore = asyncio.Semaphore(2)
    tasks = [get_event_bets(event[1], browser, semaphore) for event in events]
    all_bets = await asyncio.gather(*tasks)
    browser.stop()
    flattened_bets = []
    for bets in all_bets:
        flattened_bets.append(bets)
    return flattened_bets

async def main():
    data = [
        ('11190812', 'https://www.estorilsolcasinos.pt/pt/apostas/event/846/0/610/11190812'),
        ('11190813', 'https://www.estorilsolcasinos.pt/pt/apostas/event/846/0/610/11190813'),
        ('11190814', 'https://www.estorilsolcasinos.pt/pt/apostas/event/846/0/610/11190814'),
        ('11190815', 'https://www.estorilsolcasinos.pt/pt/apostas/event/846/0/610/11190815'),
        ('11190816', 'https://www.estorilsolcasinos.pt/pt/apostas/event/846/0/610/11190816')
    ]
    bets = await get_all_events_bets(data)
    print(bets)

if __name__ == "__main__":
    # data = {
    #     'Futebol': {
    #         'CAN 2025 - qualif.': [
    #             ('5144410301', 'https://www.estorilsolcasinos.pt/pt/apostas/event/844/0/220/5144410301'),
    #             ('5144349101', 'https://www.estorilsolcasinos.pt/pt/apostas/event/844/0/220/5144349101'),
    #             ('11593501', 'https://www.estorilsolcasinos.pt/pt/apostas/event/844/0/220/11593501')
    #          ],
    #     }
    # }
    # print(data)
    asyncio.run(main())
